from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


IntentName = Literal[
    "TRAFFIC_STATUS", "ENERGY_STATUS", "MOBILITY_STATUS", "RISK_STATUS",
    "SCENARIO_CREATE", "DECISION_ANALYSIS", "MODEL_INFORMATION", "VALIDATION_STATUS", "STREAM_STATUS", "SYSTEM_STATUS", "GENERAL_PROJECT_QUERY",
    "UNKNOWN",
]


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    conversation_id: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class Entity(BaseModel):
    kind: str
    value: str
    confidence: float | None = None


class Citation(BaseModel):
    source_type: str
    source_id: str
    label: str
    endpoint: str | None = None
    timestamp: str | None = None


class AssistantResponse(BaseModel):
    answer: str
    intent: IntentName
    entities: list[Entity] = Field(default_factory=list)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    citations: list[Citation] = Field(default_factory=list)
    actions: list[dict[str, Any]] = Field(default_factory=list)
    uncertainty: str | None = None
    data_freshness: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)
    status: Literal["completed", "unavailable", "clarification", "blocked"] = "completed"


class ToolDefinition(BaseModel):
    name: str
    description: str
    required_role: str = "viewer"
    timeout_seconds: float = 5.0
    version: str = "1.0.0"


class ToolResult(BaseModel):
    tool: str
    status: Literal["success", "unavailable", "error", "forbidden"]
    data: dict[str, Any] = Field(default_factory=dict)
    error: str | None = None
    evidence: list[dict[str, Any]] = Field(default_factory=list)
