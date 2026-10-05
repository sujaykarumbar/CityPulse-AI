from __future__ import annotations


def synthetic_control_estimate(treated: list[float], controls: list[list[float]]) -> dict[str, object]:
    if not treated or not controls:
        return {"status": "NOT_IDENTIFIED", "method": "synthetic_control", "reason": "Donor pool is insufficient for a synthetic counterfactual."}

    donor_averages = [sum(series) / len(series) for series in controls]
    synthetic_counterfactual = sum(donor_averages) / len(donor_averages)
    estimate = sum(treated) / len(treated) - synthetic_counterfactual
    return {
        "status": "MEASURED",
        "method": "synthetic_control",
        "estimate": float(estimate),
        "synthetic_counterfactual": float(synthetic_counterfactual),
        "assumptions": ["stable_donor_pool", "pre_period_fit"],
    }
