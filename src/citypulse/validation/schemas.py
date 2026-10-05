from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class MetricResult(BaseModel):
    name: str
    value: float | None
    status: str = "MEASURED"
    units: str | None = None


class ValidationResult(BaseModel):
    validation_id: str = Field(default_factory=lambda: str(uuid4()))
    task: str
    dataset_version: str | None = None
    feature_version: str | None = None
    model_version: str | None = None
    graph_version: str | None = None
    simulation_version: str | None = None
    timestamp: datetime = Field(default_factory=utc_now)
    population: str | None = None
    geographic_scope: str | None = None
    temporal_scope: dict[str, str] = Field(default_factory=dict)
    metric_results: list[MetricResult] = Field(default_factory=list)
    uncertainty: dict[str, Any] = Field(default_factory=dict)
    robustness: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
    status: Literal["VALIDATED", "VALIDATION_NOT_AVAILABLE", "FAILED"] = "VALIDATION_NOT_AVAILABLE"
    result_type: Literal["OBSERVED", "FORECAST", "SIMULATED", "SYNTHETIC"] = "OBSERVED"
    lineage: dict[str, str | None] = Field(default_factory=dict)


class BacktestRequest(BaseModel):
    task: str = Field(min_length=1, max_length=100)
    observed: list[float] = Field(min_length=1, max_length=10000)
    predicted: list[float] = Field(min_length=1, max_length=10000)
    dataset_version: str | None = None
    model_version: str | None = None
    result_type: Literal["OBSERVED", "FORECAST", "SIMULATED", "SYNTHETIC"] = "FORECAST"


class SyntheticRequest(BaseModel):
    domain: Literal["traffic", "mobility", "energy", "weather"]
    sample_count: int = Field(default=24, gt=0, le=10000)
    seed: int = 42
    config: dict[str, Any] = Field(default_factory=dict)


class RobustnessRequest(BaseModel):
    values: list[float] = Field(min_length=1, max_length=10000)
    rate: float = Field(gt=0, le=0.8)
    seed: int = 42
    mode: Literal["MCAR", "BLOCK"] = "MCAR"


class SyntheticCompareRequest(BaseModel):
    real_values: list[float] = Field(default_factory=list, max_length=10000)
    synthetic_values: list[float] = Field(min_length=1, max_length=10000)


class CalibrationRequest(BaseModel):
    observed: list[float] = Field(default_factory=list, max_length=10000)
    parameter_grid: dict[str, list[float]] = Field(default_factory=dict)
    simulated_candidates: list[list[float]] = Field(default_factory=list, max_length=500)
