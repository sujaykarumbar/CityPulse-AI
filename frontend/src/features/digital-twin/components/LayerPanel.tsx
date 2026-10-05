import { Eye, EyeOff } from "lucide-react";
import { useDigitalTwinStore } from "../store/digitalTwinStore";
import type { TwinLayerDefinition } from "../types/digitalTwin";

const definitions: TwinLayerDefinition[] = [
  { id: "terrain", label: "Terrain", group: "base", color: "#587b72", available: false },
  { id: "buildings", label: "Buildings", group: "base", color: "#d49b61", available: false },
  { id: "roads", label: "Road network", group: "base", color: "#6fb7c8", available: false },
  { id: "traffic", label: "Traffic", group: "intelligence", color: "#e2ae6e", available: false },
  { id: "mobility", label: "Mobility", group: "intelligence", color: "#b9c46b", available: false },
  { id: "energy", label: "Energy", group: "intelligence", color: "#d97975", available: false },
  { id: "risk", label: "Risk", group: "intelligence", color: "#c77ce0", available: false },
  { id: "transit", label: "Transit", group: "intelligence", color: "#77c8d1", available: false },
  { id: "scenario", label: "Scenario impact", group: "scenario", color: "#91d1bd", available: false },
];

export function LayerPanel() {
  const { activeLayers, setLayerVisible } = useDigitalTwinStore();
  return (
    <div className="twin-layer-panel" aria-label="Digital twin layers">
      {(["base", "intelligence", "scenario"] as const).map((group) => (
        <div key={group} className="twin-layer-group">
          <div className="twin-layer-heading">{group === "intelligence" ? "INTELLIGENCE" : group.toUpperCase()}</div>
          {definitions.filter((layer) => layer.group === group).map((layer) => (
            <button className="twin-layer-row" key={layer.id} onClick={() => setLayerVisible(layer.id, !activeLayers[layer.id])} aria-label={`${layer.label} ${activeLayers[layer.id] ? "visible" : "hidden"}`}>
              <span className="twin-layer-color" style={{ background: layer.color }} />
              <span>{layer.label}</span>
              {!layer.available && <small>unavailable</small>}
              {activeLayers[layer.id] ? <Eye size={14} /> : <EyeOff size={14} />}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}
