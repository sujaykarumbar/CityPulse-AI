from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

EventType = Literal[
    "TRAFFIC_UPDATE", "WEATHER_UPDATE", "TRANSIT_UPDATE", "ENERGY_UPDATE",
    "MOBILITY_UPDATE", "ROAD_NETWORK_UPDATE", "RISK_UPDATE", "MODEL_PREDICTION",
    "ANOMALY_DETECTED", "SCENARIO_UPDATE", "SYSTEM_EVENT",
]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class UrbanEvent(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    event_type: EventType
    source: str = Field(min_length=1)
    timestamp: datetime
    ingestion_timestamp: datetime = Field(default_factory=utc_now)
    schema_version: int = Field(default=1, ge=1)
    city_id: str | None = None
    entity_type: str | None = None
    entity_id: str | None = None
    payload: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DeadLetterRecord(BaseModel):
    event_id: str
    original_topic: str
    error_code: str
    error_message: str
    attempt_count: int = Field(ge=1)
    timestamp: datetime = Field(default_factory=utc_now)
    payload_reference: str | None = None


class ReplayRequest(BaseModel):
    topic: str
    start_time: datetime | None = None
    end_time: datetime | None = None
    event_type: EventType | None = None
    entity_id: str | None = None
    speed: float = Field(default=1.0, gt=0)
    destination: str | None = None
    dry_run: bool = True


class StreamStatus(BaseModel):
    broker: str
    connected: bool
    status: str
    topics: list[str]
    accepted_events: int
    rejected_events: int
    dead_letter_events: int
    processed_event_ids: int
    guarantee: str
