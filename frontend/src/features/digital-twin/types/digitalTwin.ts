export type TwinLayerId =
  | "terrain"
  | "buildings"
  | "roads"
  | "traffic"
  | "mobility"
  | "energy"
  | "risk"
  | "transit"
  | "scenario";

export type TwinTimeMode = "observed" | "forecast" | "simulated";
export type TwinVisualizationMode = "baseline" | "scenario" | "difference";
export type PerformanceMode = "performance" | "balanced" | "quality";

export interface TwinLayerDefinition {
  id: TwinLayerId;
  label: string;
  group: "base" | "intelligence" | "scenario";
  color: string;
  available: boolean;
}

export interface SelectedEntity {
  entityType: "building" | "road" | "zone" | "risk" | "transit" | "scenario";
  entityId: string;
  properties: Record<string, unknown>;
}
