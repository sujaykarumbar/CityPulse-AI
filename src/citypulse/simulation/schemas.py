from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


ScenarioType = Literal[
    "traffic_demand_change",
    "road_closure",
    "lane_reduction",
    "road_addition",
    "transit_station_addition",
    "transit_disruption",
    "demand_change",
    "weather_change",
    "energy_demand_change",
    "traffic_incident",
]


class ScenarioChange(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: ScenarioType
    parameters: dict[str, Any] = Field(default_factory=dict)


class Scenario(BaseModel):
    model_config = ConfigDict(extra="forbid")
    scenario_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    changes: list[ScenarioChange] = Field(min_length=1, max_length=20)
    seed: int = 42
    metadata: dict[str, Any] = Field(default_factory=dict)


class UrbanState(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    timestamp: datetime | None = None
    traffic_state: dict[str, Any] = Field(default_factory=dict)
    mobility_state: dict[str, Any] = Field(default_factory=dict)
    energy_state: dict[str, Any] = Field(default_factory=dict)
    weather_state: dict[str, Any] = Field(default_factory=dict)
    graph_state: dict[str, Any] = Field(default_factory=dict)
    risk_state: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class MetricDelta(BaseModel):
    metric: str
    baseline_value: float
    scenario_value: float
    absolute_delta: float
    percentage_delta: float | None


class SimulationResult(BaseModel):
    scenario_id: str
    scenario_name: str
    status: Literal["completed", "invalid", "data_unavailable"]
    baseline: UrbanState
    scenario: UrbanState
    deltas: list[MetricDelta] = Field(default_factory=list)
    affected_regions: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    uncertainty_status: str = "UNCERTAINTY_NOT_ESTIMATED"
