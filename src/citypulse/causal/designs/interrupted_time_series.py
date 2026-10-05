from __future__ import annotations


def interrupted_time_series(pre_period: list[float], post_period: list[float]) -> dict[str, object]:
    if not pre_period or not post_period:
        return {"status": "NOT_IDENTIFIED", "method": "interrupted_time_series", "reason": "ITS requires both pre- and post-intervention periods."}
    pre_mean = sum(pre_period) / len(pre_period)
    post_mean = sum(post_period) / len(post_period)
    return {
        "status": "MEASURED",
        "method": "interrupted_time_series",
        "estimate": float(post_mean - pre_mean),
        "assumptions": ["clear_intervention_date", "sufficient_pre_period", "seasonality_accounted_for"],
    }
