from __future__ import annotations

from typing import Any


def compute_recovery_plan(rpo_hours: float | None = None, rto_hours: float | None = None) -> dict[str, Any]:
    return {
        "rpo_hours": rpo_hours if rpo_hours is not None else "NOT_MEASURED",
        "rto_hours": rto_hours if rto_hours is not None else "NOT_MEASURED",
        "status": "RECOVERY_PLAN_DEFINED",
        "notes": "RPO and RTO targets are configurable and must be validated in an actual environment before deployment claims are made.",
    }
