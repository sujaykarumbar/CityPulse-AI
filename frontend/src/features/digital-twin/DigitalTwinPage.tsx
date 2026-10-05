import { Box, Home, PanelRight, RotateCcw } from "lucide-react";
import { TwinViewport } from "../../components/TwinViewport";
import { LayerPanel } from "./components/LayerPanel";
import { TimelineControl } from "./components/TimelineControl";
import { useDigitalTwinStore } from "./store/digitalTwinStore";

export function DigitalTwinPage() {
  const { activeLayers, selectedEntity, selectEntity, performanceMode, setPerformanceMode } = useDigitalTwinStore();
  return (
    <div className="digital-twin-page">
      <div className="digital-twin-toolbar">
        <div><span className="panel-label">DIGITAL TWIN / 3D VIEW</span><h1>City spatial context</h1></div>
        <div className="digital-twin-actions">
          <span className="data-badge simulated">GEOMETRY UNAVAILABLE</span>
          <button className="quiet-button" onClick={() => selectEntity(null)}><Home size={14} /> Home</button>
          <button className="quiet-button"><RotateCcw size={14} /> Reset view</button>
          <select aria-label="Performance mode" value={performanceMode} onChange={(event) => setPerformanceMode(event.target.value as typeof performanceMode)}>
            <option value="performance">Performance</option><option value="balanced">Balanced</option><option value="quality">Quality</option>
          </select>
        </div>
      </div>
      <div className="digital-twin-body">
        <LayerPanel />
        <section className="digital-twin-viewport" aria-label="Digital twin scene">
          <TwinViewport layers={activeLayers} />
          <div className="digital-twin-scene-label"><Box size={14} /> 3D scene preview <span>•</span> no backend geometry</div>
          <div className="digital-twin-empty"><strong>Awaiting geographic API data</strong><span>Connect a verified GeoJSON or 3D Tiles endpoint to populate this scene.</span></div>
        </section>
        <aside className="digital-twin-inspector">
          <div className="inspector-heading"><span className="panel-label">ENTITY INSPECTOR</span><PanelRight size={16} /></div>
          {selectedEntity ? <><h2>{selectedEntity.entityType}</h2><div className="inspector-row"><span>ID</span><strong>{selectedEntity.entityId}</strong></div></> : <div className="inspector-empty"><strong>No entity selected</strong><span>Click a loaded road, building, zone, risk event, or transit object to inspect it.</span></div>}
          <div className="inspector-divider" />
          <div className="inspector-source"><span>Data source</span><strong className="muted-value">Backend unavailable</strong></div>
        </aside>
      </div>
      <TimelineControl />
    </div>
  );
}
