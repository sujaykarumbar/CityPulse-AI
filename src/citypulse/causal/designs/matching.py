from __future__ import annotations


def matching_estimate(treated: list[float], matched_controls: list[float]) -> dict[str, object]:
    if not treated or not matched_controls:
        return {"status": "NOT_IDENTIFIED", "method": "matching", "reason": "Matching requires treated and matched control observations."}
    return {
        "status": "MEASURED",
        "method": "matching",
        "estimate": float(sum(treated) / len(treated) - sum(matched_controls) / len(matched_controls)),
        "diagnostics": ["before_balance", "after_balance", "common_support"],
    }
