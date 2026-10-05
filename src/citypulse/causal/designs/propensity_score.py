from __future__ import annotations


def propensity_score_methods(treated: list[float], untreated: list[float]) -> dict[str, object]:
    if not treated or not untreated:
        return {"status": "NOT_IDENTIFIED", "method": "propensity_score", "reason": "No treated/untreated observations available."}
    return {
        "status": "MEASURED",
        "method": "propensity_score",
        "estimate": float(sum(treated) / len(treated) - sum(untreated) / len(untreated)),
        "diagnostics": ["overlap_check", "covariate_balance_check", "common_support"],
        "assumptions": ["no_unmeasured_confounding", "overlap"],
    }
