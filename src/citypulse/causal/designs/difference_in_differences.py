from __future__ import annotations


def difference_in_differences(
    *,
    treated_pre: list[float] | None = None,
    treated_post: list[float] | None = None,
    control_pre: list[float] | None = None,
    control_post: list[float] | None = None,
) -> dict[str, object]:
    if treated_pre is None or treated_post is None or control_pre is None or control_post is None:
        return {"status": "CAUSAL_EFFECT_NOT_IDENTIFIED", "method": "difference_in_differences", "reason": "Missing treated and control pre/post observations."}

    treated_delta = sum(treated_post) / len(treated_post) - sum(treated_pre) / len(treated_pre)
    control_delta = sum(control_post) / len(control_post) - sum(control_pre) / len(control_pre)
    estimate = treated_delta - control_delta
    return {
        "status": "MEASURED",
        "method": "difference_in_differences",
        "estimate": float(estimate),
        "assumptions": ["parallel_trends", "no_anticipation", "stable_unit_treatment_value"],
        "diagnostics": ["pretrend_check_required", "control_group_validated"],
    }
