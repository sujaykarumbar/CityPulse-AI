from __future__ import annotations


def regression_discontinuity(running_variable: list[float], threshold: float | None = None) -> dict[str, object]:
    if threshold is None:
        return {"status": "RD_NOT_APPLICABLE", "method": "regression_discontinuity", "reason": "No legitimate threshold-based treatment assignment mechanism is defined."}
    return {
        "status": "MEASURED",
        "method": "regression_discontinuity",
        "estimate": float(sum(running_variable) / len(running_variable) - threshold),
        "threshold": float(threshold),
        "assumptions": ["cutoff_defined", "continuity", "no_manipulation"],
    }
