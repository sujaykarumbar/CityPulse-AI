from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class FutureDriver(BaseModel):
    name: str
    category: str
    value: float
    lower_bound: float | None = None
    upper_bound: float | None = None
    unit: str | None = None
    provenance: str = "SCENARIO_ESTIMATE"


class FutureScenario(BaseModel):
    scenario_id: str
    scenario_name: str
    city_id: str
    start_time: str
    end_time: str
    horizon_years: int
    assumptions: dict[str, Any] = Field(default_factory=dict)
    drivers: list[FutureDriver] = Field(default_factory=list)
    random_seed: int = 0
    provenance: dict[str, Any] = Field(
        default_factory=lambda: {
            "status": "SCENARIO_ESTIMATE",
            "data_origin": "SYNTHETIC",
            "notes": "Scenario assumptions are synthetic and must be reviewed by a human planner before use.",
        }
    )


class Signpost(BaseModel):
    name: str
    metric: str
    source: str = "model"
    baseline: float | None = None
    current_value: float | None = None
    threshold: float | None = None
    direction: str = "above"
    confidence: float = 0.5
    freshness: str = "NOT_AVAILABLE"


class TriggerResult(BaseModel):
    metric_name: str
    current_value: float
    threshold: float
    direction: str
    triggered: bool
    signal: str
    status: str = "MODEL_DERIVED"


class PolicyPathway(BaseModel):
    initial_strategy: str
    monitoring: list[str]
    thresholds: dict[str, float] = Field(default_factory=dict)
    alternative_strategy: str | None = None
    next_action: str = "MONITOR"
    provenance: dict[str, Any] = Field(default_factory=dict)


class ForesightReport(BaseModel):
    report_id: str
    city_id: str
    horizon_years: int
    scenarios: list[FutureScenario] = Field(default_factory=list)
    status: str = "SCENARIO_ESTIMATE"
    assumptions: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
