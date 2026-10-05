from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


Lifecycle = Literal["EXPERIMENT", "VALIDATING", "VALIDATED", "STAGING", "PRODUCTION", "ARCHIVED", "REJECTED", "FAILED"]


class ModelRecord(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_id: str
    model_name: str
    model_version: str
    model_type: str
    domain: str
    task: str
    framework: str
    dataset_version: str | None = None
    feature_version: str | None = None
    graph_version: str | None = None
    code_commit: str | None = None
    training_run_id: str | None = None
    artifact_uri: str | None = None
    created_at: datetime = Field(default_factory=now_utc)
    parameters: dict[str, Any] = Field(default_factory=dict)
    hyperparameters: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, float] = Field(default_factory=dict)
    validation_status: str = "NOT_RUN"
    deployment_status: str = "NOT_DEPLOYED"
    lifecycle: Lifecycle = "EXPERIMENT"
    environment: str = "local"
    dependencies: dict[str, str] = Field(default_factory=dict)
    owner: str | None = None
    description: str | None = None
    limitations: list[str] = Field(default_factory=list)
    approval_status: str = "NOT_REQUESTED"
    created_by: str | None = None
    updated_at: datetime = Field(default_factory=now_utc)


class ValidationCheck(BaseModel):
    name: str
    status: Literal["PASS", "WARN", "FAIL"]
    message: str
    observed_value: Any = None
    threshold: Any = None


class ValidationResult(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    model_id: str
    status: Literal["PASS", "WARN", "FAIL"]
    checks: list[ValidationCheck]
    created_at: datetime = Field(default_factory=now_utc)


class DriftResult(BaseModel):
    feature: str
    method: str
    reference_statistic: dict[str, float]
    current_statistic: dict[str, float]
    distance: float
    threshold: float | None
    status: Literal["DRIFT", "NO_DRIFT", "NOT_MEASURABLE"]
    sample_size_reference: int
    sample_size_current: int


class RetrainingJob(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    job_id: str
    model_name: str
    trigger_type: str
    trigger_reason: str
    status: Literal["CANDIDATE", "QUEUED", "RUNNING", "COMPLETED", "FAILED"] = "CANDIDATE"
    dataset_version: str | None = None
    feature_version: str | None = None
    graph_version: str | None = None
    training_run_id: str | None = None
    candidate_model_version: str | None = None
    validation_status: str = "NOT_RUN"
    promotion_status: str = "NOT_REQUESTED"
    created_at: datetime = Field(default_factory=now_utc)


class LineageRecord(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    prediction_id: str | None = None
    model_id: str
    model_version: str
    training_run_id: str | None = None
    dataset_version: str | None = None
    feature_version: str | None = None
    graph_version: str | None = None
    code_commit: str | None = None


class PromotionRequest(BaseModel):
    actor: str = Field(min_length=1)
    reason: str = Field(min_length=1)


class RollbackRequest(PromotionRequest):
    to_version: str = Field(min_length=1)
