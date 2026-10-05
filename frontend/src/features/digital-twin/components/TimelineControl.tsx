import { Pause, Play, StepBack, StepForward } from "lucide-react";
import { useState } from "react";
import { useDigitalTwinStore } from "../store/digitalTwinStore";

export function TimelineControl() {
  const [playing, setPlaying] = useState(false);
  const { timeMode, setTimeMode, visualizationMode, setVisualizationMode } = useDigitalTwinStore();

  return (
    <div className="timeline-control" aria-label="Digital twin time controls">
      <div className="timeline-modes" role="group" aria-label="Data mode">
        {(["observed", "forecast", "simulated"] as const).map((mode) => (
          <button key={mode} className={`mode-pill ${timeMode === mode ? "active" : ""}`} onClick={() => setTimeMode(mode)}>
            {mode.toUpperCase()}
          </button>
        ))}
      </div>
      <div className="timeline-playback">
        <button className="timeline-icon" aria-label="Previous time step"><StepBack size={14} /></button>
        <button className="timeline-icon play" aria-label={playing ? "Pause playback" : "Play playback"} onClick={() => setPlaying((value) => !value)}>
          {playing ? <Pause size={14} /> : <Play size={14} />}
        </button>
        <button className="timeline-icon" aria-label="Next time step"><StepForward size={14} /></button>
        <div className="timeline-track"><span className="timeline-progress" /></div>
        <span className="timeline-time">Time unavailable</span>
      </div>
      <div className="timeline-modes" role="group" aria-label="Scenario display mode">
        {(["baseline", "scenario", "difference"] as const).map((mode) => (
          <button key={mode} className={`mode-pill ${visualizationMode === mode ? "active" : ""}`} onClick={() => setVisualizationMode(mode)}>
            {mode}
          </button>
        ))}
      </div>
    </div>
  );
}
