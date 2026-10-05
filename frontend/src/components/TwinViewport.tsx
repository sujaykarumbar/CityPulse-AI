import { useEffect, useRef } from "react";
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";

interface TwinViewportProps { layers: Record<string, boolean> }

export function TwinViewport({ layers }: TwinViewportProps) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const layersRef = useRef(layers);
  layersRef.current = layers;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    if (typeof window.WebGLRenderingContext === "undefined") return;
    const renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true });
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.setClearColor(0x10181c, 1);
    const scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x10181c, 24, 58);
    const camera = new THREE.PerspectiveCamera(34, 1, 0.1, 100);
    camera.position.set(13, 11, 15);
    const controls = new OrbitControls(camera, canvas);
    controls.enableDamping = true;
    controls.target.set(0, 0, 0);
    controls.minDistance = 7;
    controls.maxDistance = 35;
    controls.maxPolarAngle = Math.PI / 2.05;

    const ambient = new THREE.HemisphereLight(0xb9d6d2, 0x182226, 1.8);
    scene.add(ambient);
    const key = new THREE.DirectionalLight(0xffd5a3, 2.1);
    key.position.set(-8, 14, 9);
    scene.add(key);

    const twinScene = new THREE.Group();
    scene.add(twinScene);
    const ground = new THREE.Mesh(new THREE.PlaneGeometry(46, 46), new THREE.MeshStandardMaterial({ color: 0x172326, roughness: 1 }));
    ground.rotation.x = -Math.PI / 2;
    twinScene.add(ground);
    const grid = new THREE.GridHelper(46, 23, 0x31545a, 0x1c3539);
    grid.position.y = 0.01;
    twinScene.add(grid);
    const ring = new THREE.Mesh(new THREE.RingGeometry(5.2, 5.24, 64), new THREE.MeshBasicMaterial({ color: 0x3d7072, transparent: true, opacity: 0.45, side: THREE.DoubleSide }));
    ring.rotation.x = -Math.PI / 2;
    ring.position.y = 0.03;
    twinScene.add(ring);

    let animationFrame = 0;
    const resize = () => { const { width, height } = canvas.getBoundingClientRect(); renderer.setSize(width, height, false); camera.aspect = width / Math.max(height, 1); camera.updateProjectionMatrix(); };
    const animate = () => { animationFrame = requestAnimationFrame(animate); controls.update(); renderer.render(scene, camera); };
    const observer = new ResizeObserver(resize);
    observer.observe(canvas);
    resize();
    animate();
    return () => { cancelAnimationFrame(animationFrame); observer.disconnect(); controls.dispose(); renderer.dispose(); ground.geometry.dispose(); (ground.material as THREE.Material).dispose(); grid.geometry.dispose(); (grid.material as THREE.Material).dispose(); ring.geometry.dispose(); (ring.material as THREE.Material).dispose(); };
  }, []);

  useEffect(() => {
    // Layers remain an explicit contract for the future GeoJSON renderer. No fake city objects are added here.
    void layersRef.current;
  }, [layers]);

  return <canvas ref={canvasRef} className="twin-canvas" role="img" aria-label="Interactive 3D city viewport preview" />;
}
