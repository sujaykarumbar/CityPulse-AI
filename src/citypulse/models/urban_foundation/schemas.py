from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ModalityName = Literal["TRAFFIC", "ENERGY", "MOBILITY", "GEOGRAPHY", "SENSING", "TEXT", "IMAGERY"]
ObjectiveName = Literal[
    "masked_modality_prediction",
    "contrastive_cross_modal_alignment",
    "temporal_imputation",
    "spatial_context_prediction",
    "multimodal_trajectory_matching",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UrbanRepresentationRecord(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    record_id: str = Field(min_length=1)
    entity_type: str = Field(min_length=1)
    entity_id: str = Field(min_length=1)
    modality: ModalityName
    embedding: list[float] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)


class UrbanFoundationObjective(BaseModel):
    name: ObjectiveName
    description: str
    enabled: bool = False


class UrbanFoundationStatus(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    status: Literal["NOT TRAINED", "TRAINING", "READY"] = "NOT TRAINED"
    training_ready: bool = False
    modalities: list[str] = Field(default_factory=list)
    objectives: list[UrbanFoundationObjective] = Field(default_factory=list)
    index_size: int = 0
    last_updated: datetime | None = None
    notes: str = "No large-scale pretrained urban foundation model is present in this checkout."


class UrbanFoundationSearchRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)
    top_k: int = Field(default=5, gt=0, le=20)


class UrbanFoundationSearchItem(BaseModel):
    record_id: str
    entity_type: str
    entity_id: str
    modality: str
    score: float
    metadata: dict[str, Any] = Field(default_factory=dict)


class UrbanFoundationSearchResponse(BaseModel):
    query: str
    total: int
    items: list[UrbanFoundationSearchItem] = Field(default_factory=list)


class UrbanResearchExperiment(BaseModel):
    experiment_id: str
    name: str
    objective: ObjectiveName
    description: str
    status: Literal["PLANNED", "RUNNING", "COMPLETED", "SKIPPED"] = "PLANNED"
    created_at: datetime = Field(default_factory=utc_now)
    metadata: dict[str, Any] = Field(default_factory=dict)
