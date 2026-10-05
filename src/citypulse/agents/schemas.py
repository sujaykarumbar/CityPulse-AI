from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Literal
from uuid import uuid4

from pydantic import BaseModel, Field

TaskStatus = Literal["CREATED", "PLANNING", "RUNNING", "WAITING", "VERIFYING", "SYNTHESIZING", "COMPLETED", "PARTIALLY_COMPLETED", "FAILED", "CANCELLED", "TIMEOUT"]
AgentStatus = Literal["PENDING", "RUNNING", "COMPLETED", "UNAVAILABLE", "FAILED", "TIMEOUT", "DENIED"]


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


class ExecutionBudget(BaseModel):
    max_execution_time: float = Field(default=20.0, gt=0, le=120)
    max_agents: int = Field(default=6, gt=0, le=12)
    max_tool_calls: int = Field(default=12, gt=0, le=50)
    max_tokens: int = Field(default=0, ge=0, le=10000)
    max_cost: float = Field(default=0.0, ge=0)
    max_retries: int = Field(default=1, ge=0, le=3)


class ResearchTaskRequest(BaseModel):
    user_request: str = Field(min_length=4, max_length=4000)
    mode: Literal["AUTO", "SINGLE", "PARALLEL", "RESEARCH", "VERIFICATION"] = "AUTO"
    domains: list[str] = Field(default_factory=list, max_length=10)
    budget: ExecutionBudget = Field(default_factory=ExecutionBudget)
    context: dict[str, Any] = Field(default_factory=dict)


class TaskNode(BaseModel):
    node_id: str
    agent_id: str
    domain: str
    dependencies: list[str] = Field(default_factory=list)
    tool_id: str


class TaskPlan(BaseModel):
    workflow_type: str
    nodes: list[TaskNode]
    max_tool_calls: int
    rationale: str


class Evidence(BaseModel):
    evidence_id: str = Field(default_factory=lambda: str(uuid4()))
    source_type: str
    source_id: str
    timestamp: datetime = Field(default_factory=utc_now)
    claim: str
    value: Any = None
    entity_type: str | None = None
    entity_id: str | None = None
    provenance: dict[str, Any] = Field(default_factory=dict)
    epistemic_state: Literal["OBSERVED", "FORECAST", "SIMULATED", "INFERRED", "HYPOTHESIS", "UNKNOWN"] = "UNKNOWN"


class AgentRunState(BaseModel):
    agent_id: str
    task_id: str
    status: AgentStatus
    started_at: datetime = Field(default_factory=utc_now)
    completed_at: datetime | None = None
    tool_calls: int = 0
    evidence_refs: list[str] = Field(default_factory=list)
    output: dict[str, Any] = Field(default_factory=dict)
    error_code: str | None = None
    latency_seconds: float | None = None


class AgentTaskResult(BaseModel):
    task_id: str
    run_id: str
    status: TaskStatus
    request: str
    plan: TaskPlan
    agent_states: list[AgentRunState]
    evidence: list[Evidence]
    verification: dict[str, Any]
    conflicts: list[dict[str, Any]] = Field(default_factory=list)
    answer: str
    reproducibility: dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=utc_now)
