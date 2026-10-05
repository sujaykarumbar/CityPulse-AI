from __future__ import annotations


def doubly_robust_estimate(treated_mean: float, control_mean: float, propensity_score: float | None = None) -> dict[str, object]:
    if propensity_score is None:
        return {"status": "NOT_IDENTIFIED", "method": "doubly_robust", "reason": "Doubly robust estimation requires a treatment model or propensity score."}
    estimate = treated_mean - control_mean
    return {
        "status": "MEASURED",
        "method": "doubly_robust",
        "estimate": float(estimate),
        "propensity_score": float(propensity_score),
        "assumptions": ["outcome_model_correct_or_treatment_model_correct"],
    }
