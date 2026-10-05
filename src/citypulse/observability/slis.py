from __future__ import annotations

from typing import Any


def build_error_budget(slo_target: float, budget_consumed: float) -> dict[str, Any]:
    if not 0.0 <= slo_target <= 1.0:
        raise ValueError("SLO_TARGET_MUST_BE_BETWEEN_0_AND_1")
    allowed_error = 1.0 - slo_target
    remaining = max(0.0, allowed_error - budget_consumed)
    return {
        "slo_target": slo_target,
        "allowed_error": allowed_error,
        "budget_consumed": budget_consumed,
        "budget_remaining": remaining,
        "status": "within_budget" if remaining > 0 else "budget_exhausted",
    }
