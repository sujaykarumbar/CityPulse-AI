from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field, ConfigDict


class DecisionObjective(BaseModel):
    name: str
    metric: str
    direction: Literal["minimize", "maximize"]
    weight: float = Field(gt=0, le=1)
    source: str = "measured"


class DecisionConstraint(BaseModel):
    name: str
    metric: str
    direction: Literal["maximum", "minimum"]
    value: float | None = None


class DecisionCandidate(BaseModel):
    candidate_id: str
    scenario: dict[str, Any] = Field(default_factory=dict)
    metrics: dict[str, float] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)


class DecisionProblem(BaseModel):
    model_config = ConfigDict(extra="forbid")
    problem_id: str
    objectives: list[DecisionObjective] = Field(min_length=1)
    constraints: list[DecisionConstraint] = Field(default_factory=list)
    candidates: list[DecisionCandidate] = Field(min_length=1)
    seed: int = 42
    metadata: dict[str, Any] = Field(default_factory=dict)


class ConstraintResult(BaseModel):
    constraint: str
    metric: str
    threshold: float | None
    actual_value: float | None
    feasible: bool
    status: str


class CandidateResult(BaseModel):
    candidate_id: str
    objective_values: dict[str, float]
    constraints: list[ConstraintResult]
    feasible: bool
    weighted_score: float | None
    status: Literal["measured", "not_run", "not_available"]


class SensitivityResult(BaseModel):
    parameter: str
    values: list[float]
    objective_values: list[float]
    status: str = "measured"


class DecisionResult(BaseModel):
    problem_id: str
    candidates: list[CandidateResult]
    pareto_candidate_ids: list[str]
    limitations: list[str] = Field(default_factory=list)
