from __future__ import annotations

from pydantic import BaseModel, Field


class UrbanStrategyState(BaseModel):
    """Represents a strategy within the adaptive urban loop."""

    strategy_id: str
    city_id: str
    version: str
    status: str = "DRAFT"
    objectives: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    policies: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    expected_outcomes: dict[str, float] = Field(default_factory=dict)
    signposts: list[str] = Field(default_factory=list)
    trigger_rules: list[str] = Field(default_factory=list)
    validity_period: str | None = None
    evidence: dict[str, str] = Field(default_factory=dict)
    model_versions: dict[str, str] = Field(default_factory=dict)
    created_at: str | None = None
    updated_at: str | None = None
