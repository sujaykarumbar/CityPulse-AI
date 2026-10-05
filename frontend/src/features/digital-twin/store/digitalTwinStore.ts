import { create } from "zustand";
import type { PerformanceMode, SelectedEntity, TwinLayerId, TwinTimeMode, TwinVisualizationMode } from "../types/digitalTwin";

interface DigitalTwinState {
  activeLayers: Record<TwinLayerId, boolean>;
  selectedEntity: SelectedEntity | null;
  timeMode: TwinTimeMode;
  visualizationMode: TwinVisualizationMode;
  performanceMode: PerformanceMode;
  currentTimestamp: string | null;
  setLayerVisible: (layer: TwinLayerId, visible: boolean) => void;
  selectEntity: (entity: SelectedEntity | null) => void;
  setTimeMode: (mode: TwinTimeMode) => void;
  setVisualizationMode: (mode: TwinVisualizationMode) => void;
  setPerformanceMode: (mode: PerformanceMode) => void;
  setCurrentTimestamp: (timestamp: string | null) => void;
}

const initialLayers: Record<TwinLayerId, boolean> = {
  terrain: true,
  buildings: false,
  roads: false,
  traffic: false,
  mobility: false,
  energy: false,
  risk: false,
  transit: false,
  scenario: false,
};

export const useDigitalTwinStore = create<DigitalTwinState>((set) => ({
  activeLayers: initialLayers,
  selectedEntity: null,
  timeMode: "observed",
  visualizationMode: "baseline",
  performanceMode: "balanced",
  currentTimestamp: null,
  setLayerVisible: (layer, visible) => set((state) => ({ activeLayers: { ...state.activeLayers, [layer]: visible } })),
  selectEntity: (selectedEntity) => set({ selectedEntity }),
  setTimeMode: (timeMode) => set({ timeMode }),
  setVisualizationMode: (visualizationMode) => set({ visualizationMode }),
  setPerformanceMode: (performanceMode) => set({ performanceMode }),
  setCurrentTimestamp: (currentTimestamp) => set({ currentTimestamp }),
}));
