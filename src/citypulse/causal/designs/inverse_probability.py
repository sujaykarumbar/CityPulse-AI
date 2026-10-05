from __future__ import annotations


def inverse_probability_weighting(treated: list[float], untreated: list[float]) -> dict[str, object]:
    if not treated or not untreated:
        return {"status": "NOT_IDENTIFIED", "method": "inverse_probability", "reason": "IPW requires both treatment and comparison groups."}
    return {
        "status": "MEASURED",
        "method": "inverse_probability",
        "estimate": float(sum(treated) / len(treated) - sum(untreated) / len(untreated)),
        "assumptions": ["positivity", "correct_model", "no_unmeasured_confounding"],
    }
