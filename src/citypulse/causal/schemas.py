from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CausalQuestion(BaseModel):
    question_id: str = Field(min_length=1)
    city_id: str = Field(min_length=1)
    treatment: str = Field(min_length=1)
    outcome: str = Field(min_length=1)
    population: str = Field(default="city")
    time_window: str = Field(default="NOT_AVAILABLE")
    geographic_scope: str = Field(default="city")
    estimand: str = Field(default="ATE")
    covariates: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    causal_design: str = Field(default="difference_in_differences")
    data: dict[str, Any] = Field(default_factory=dict)


class CausalEstimate(BaseModel):
    status: str = "NOT_IDENTIFIED"
    estimate: float | None = None
    confidence_interval: list[float] | None = None
    method: str | None = None
    assumptions: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
