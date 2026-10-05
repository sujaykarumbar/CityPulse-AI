from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, Field


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class BenchmarkRequest(BaseModel):
    task: str = Field(default="urban-benchmark")
    domain: str = Field(default="urban")
    observed: list[float] = Field(default_factory=list)
    predicted: list[float] = Field(default_factory=list)
    dataset_version: str | None = None
    model_version: str | None = None
    result_type: str = "FORECAST"


class SyntheticScenarioRequest(BaseModel):
    domain: str = Field(default="traffic")
    config: dict[str, Any] = Field(default_factory=dict)
    sample_count: int = Field(default=100, ge=1, le=10000)
    seed: int = 0


class ExperimentRecord(BaseModel):
    experiment_id: str = Field(default_factory=lambda: f"eval-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}")
    task: str
    domain: str = "urban"
    status: Literal["NOT_RUN", "RUNNING", "MEASURED", "SYNTHETIC_ONLY", "NOT_AVAILABLE"] = "NOT_RUN"
    ground_truth_status: Literal["GROUND_TRUTH_NOT_AVAILABLE", "AVAILABLE", "PARTIALLY_AVAILABLE"] = "GROUND_TRUTH_NOT_AVAILABLE"
    benchmark_status: Literal["NOT_RUN", "MEASURED", "NOT_AVAILABLE", "SYNTHETIC_ONLY"] = "NOT_RUN"
    metrics: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
    limitations: list[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=utc_now)
