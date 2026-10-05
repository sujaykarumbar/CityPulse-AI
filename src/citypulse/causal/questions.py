from __future__ import annotations

from typing import Any


def build_causal_question(
    *,
    question_id: str,
    city_id: str,
    treatment: str,
    outcome: str,
    population: str,
    time_window: str,
    geographic_scope: str,
    estimand: str = "ATE",
    covariates: list[str] | None = None,
    assumptions: list[str] | None = None,
    causal_design: str = "difference_in_differences",
) -> dict[str, Any]:
    if not question_id or not city_id or not treatment or not outcome:
        raise ValueError("Causal questions require question_id, city_id, treatment, and outcome.")

    return {
        "question_id": question_id,
        "city_id": city_id,
        "treatment": treatment,
        "outcome": outcome,
        "population": population,
        "time_window": time_window,
        "geographic_scope": geographic_scope,
        "estimand": estimand,
        "covariates": covariates or [],
        "assumptions": assumptions or ["identification_assumptions_not_verified"],
        "causal_design": causal_design,
        "status": "QUESTION_BUILT",
    }
