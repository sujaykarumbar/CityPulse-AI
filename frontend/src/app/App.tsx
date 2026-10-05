import { useQuery } from "@tanstack/react-query";
import { Activity, Box, ChevronDown, CircleHelp, Layers3, Map, Radio, RotateCcw, Search, Settings2, Sparkles, WifiOff } from "lucide-react";
import { useState } from "react";
import { getHealth, getSystemInfo } from "../lib/api/system";
import { useAppStore } from "../store/appStore";
import { TwinViewport } from "../components/TwinViewport";
import { DigitalTwinPage } from "../features/digital-twin";
import { AssistantPage } from "../features/assistant";
import { MLOpsPage } from "../features/mlops";
import { RealtimePage } from "../features/realtime";
import { ValidationDashboard } from "../features/validation";

type LayerName = "terrain" | "buildings" | "roads" | "zones";

const layers: { id: LayerName; label: string; color: string }[] = [
  { id: "terrain", label: "Terrain", color: "#587b72" },
  { id: "buildings", label: "Buildings", color: "#d49b61" },
  { id: "roads", label: "Road network", color: "#6fb7c8" },
  { id: "zones", label: "Zones", color: "#b9c46b" },
];

export function App() {
  const [activeLayers, setActiveLayers] = useState<Record<LayerName, boolean>>({
    terrain: true,
    buildings: true,
    roads: true,
    zones: false,
  });
  const [view, setView] = useState(() => window.location.pathname === "/digital-twin" ? "3D city twin" : window.location.pathname === "/assistant" ? "AI assistant" : window.location.pathname === "/mlops" ? "MLOps" : window.location.pathname === "/realtime" ? "Realtime" : window.location.pathname === "/validation" ? "Validation" : "Command center");
  const [showPanel, setShowPanel] = useState(true);
  const { sidebarOpen, toggleSidebar } = useAppStore();
  const health = useQuery({ queryKey: ["health"], queryFn: getHealth });
  const system = useQuery({ queryKey: ["system"], queryFn: getSystemInfo });

  const connectionLabel = health.isSuccess ? "API connected" : health.isError ? "API unavailable" : "Checking API";
  const toggleLayer = (layer: LayerName) => setActiveLayers((state) => ({ ...state, [layer]: !state[layer] }));
  const navigate = (nextView: string) => {
    window.history.pushState({}, "", nextView === "3D city twin" ? "/digital-twin" : nextView === "AI assistant" ? "/assistant" : nextView === "MLOps" ? "/mlops" : nextView === "Realtime" ? "/realtime" : nextView === "Validation" ? "/validation" : "/");
    setView(nextView);
  };
  const statusTone = health.isSuccess ? "online" : health.isError ? "offline" : "pending";

  if (view === "3D city twin") {
    return <DigitalTwinPage />;
  }
  if (view === "AI assistant") {
    return <AssistantPage />;
  }
  if (view === "MLOps") {
    return <MLOpsPage />;
  }
  if (view === "Realtime") {
    return <RealtimePage />;
  }
  if (view === "Validation") {
    return <ValidationDashboard />;
  }

  return (
    <div className="app-shell">
      <header className="topbar">
        <button className="brand" onClick={() => navigate("Command center")} aria-label="Open command center">
          <span className="brand-mark"><Box size={17} strokeWidth={2.5} /></span>
          <span>CITY<span>PULSE</span></span>
        </button>
        <div className="topbar-divider" />
        <button className="city-select" aria-label="Selected city">
          <span className="eyebrow">DIGITAL TWIN</span>
          <span>City not selected <ChevronDown size={14} /></span>
        </button>
        <div className="topbar-spacer" />
        <div className="connection-status">
          <span className={`status-dot ${statusTone}`} />
          <span>{connectionLabel}</span>
        </div>
        <div className="topbar-control"><Radio size={16} /><span>Live feed unavailable</span></div>
        <button className="icon-button" aria-label="Settings"><Settings2 size={18} /></button>
        <button className="avatar" aria-label="User profile">CP</button>
      </header>

      <div className="workspace">
        <aside className={`sidebar ${sidebarOpen ? "open" : "closed"}`}>
          <div className="sidebar-caption">OPERATIONS</div>
          <nav aria-label="Primary navigation">
            {[
              ["Command center", Activity], ["AI assistant", Sparkles], ["Traffic intelligence", Radio], ["Energy systems", Activity],
              ["Mobility flows", Map], ["Risk signals", CircleHelp], ["Scenarios", Layers3],
              ].map(([label, Icon]) => (
              <button key={label as string} className={`nav-item ${view === label ? "active" : ""}`} onClick={() => navigate(label as string)}>
                <Icon size={17} /><span>{label as string}</span>
              </button>
            ))}
          </nav>
          <div className="sidebar-caption secondary">PLATFORM</div>
          <nav aria-label="Platform navigation">
            {["3D city twin", "AI assistant", "MLOps", "Validation", "Realtime", "Models", "Data quality", "System"].map((label) => (
              <button key={label} className={`nav-item ${view === label ? "active" : ""}`} onClick={() => navigate(label)}>
                <span className="nav-glyph" />{label}
              </button>
            ))}
          </nav>
          <div className="sidebar-bottom">
            <button className="collapse-button" onClick={toggleSidebar}><ChevronDown size={16} className="rotate-90" />{sidebarOpen && "Collapse rail"}</button>
          </div>
        </aside>

        <main className="main-stage">
          <div className="stage-header">
            <div>
              <div className="breadcrumb">CITYPULSE <span>/</span> {view.toUpperCase()}</div>
              <h1>{view === "3D city twin" ? "3D city twin" : "Urban command center"}</h1>
              <p>{view === "3D city twin" ? "Spatial context for observed, forecast, and simulated urban states." : "A spatial view into the city intelligence stack."}</p>
            </div>
            <div className="stage-actions">
              <button className="quiet-button"><RotateCcw size={15} /> Recenter</button>
              <button className="quiet-button"><Search size={15} /> Locate</button>
            </div>
          </div>

          <section className="twin-panel" aria-label="3D digital twin viewport">
            <TwinViewport layers={activeLayers} />
            <div className="viewport-topline"><span className="data-badge simulated">SCENE PREVIEW</span><span className="viewport-note">No city geometry loaded</span></div>
            <div className="viewport-tools"><button className="tool-button active" aria-label="3D view"><Box size={17} /></button><button className="tool-button" aria-label="Map view"><Map size={17} /></button></div>
            <div className="view-compass"><span>N</span><div className="compass-ring"><span>+</span></div></div>
            {showPanel && <div className="inspector-panel">
              <div className="panel-label">SCENE INSPECTOR</div>
              <h2>Awaiting geographic context</h2>
              <p>The backend does not currently expose roads, buildings, zones, or GeoJSON. This viewport is ready for those layers without presenting placeholder geometry as city data.</p>
              <div className="inspector-row"><span>Provider</span><strong>Three.js</strong></div>
              <div className="inspector-row"><span>Data mode</span><strong className="muted-value">Unavailable</strong></div>
              <div className="inspector-row"><span>Last update</span><strong className="muted-value">Unavailable</strong></div>
            </div>}
            <button className="panel-toggle" onClick={() => setShowPanel((value) => !value)}>{showPanel ? "Hide inspector" : "Show inspector"}</button>
          </section>

          <section className="lower-grid">
            <div className="info-panel layer-panel"><div className="panel-heading"><div><span className="panel-label">VISUAL LAYERS</span><h2>Spatial context</h2></div><Layers3 size={18} /></div>
              <div className="layer-list">{layers.map((layer) => <button className="layer-row" key={layer.id} onClick={() => toggleLayer(layer.id)}><span className={`layer-switch ${activeLayers[layer.id] ? "on" : ""}`}><span /></span><span className="layer-color" style={{ background: layer.color }} /><span>{layer.label}</span><span className="layer-state">{activeLayers[layer.id] ? "ON" : "OFF"}</span></button>)}</div>
            </div>
            <div className="info-panel status-panel"><div className="panel-heading"><div><span className="panel-label">SYSTEM CONTEXT</span><h2>Provenance</h2></div><Activity size={18} /></div>
              <div className="provenance-grid"><div><span>API status</span><strong className={health.isSuccess ? "value-online" : "muted-value"}>{health.isSuccess ? "Healthy" : "Unavailable"}</strong></div><div><span>Service</span><strong>{system.data?.name ?? "Unavailable"}</strong></div><div><span>Version</span><strong>{system.data?.version ?? "Unavailable"}</strong></div><div><span>Environment</span><strong>{system.data?.environment ?? "Unavailable"}</strong></div></div>
              {health.isError && <div className="notice"><WifiOff size={15} /> Connect the FastAPI service to populate live system state.</div>}
            </div>
          </section>
        </main>
      </div>
      <footer className="statusbar"><span><span className={`status-dot ${statusTone}`} /> {connectionLabel}</span><span>3D provider <strong>Three.js</strong></span><span>Geometry <strong className="muted-value">Unavailable</strong></span><span className="statusbar-right">CITYPULSE 0.1.0</span></footer>
    </div>
  );
}
