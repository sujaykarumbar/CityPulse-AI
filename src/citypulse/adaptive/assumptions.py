from __future__ import annotations

from typing import Any


def check_assumption(
    *,
    assumption_id: str,
    description: str,
    variable: str,
    expected_range: tuple[float, float] | None = None,
    observed_value: float | None = None,
    status: str = "UNKNOWN",
) -> dict[str, Any]:
    """Evaluate whether an assumption remains consistent with observed conditions."""

    if observed_value is None:
        return {
            "assumption_id": assumption_id,
            "variable": variable,
            "status": "UNKNOWN",
            "triggered": False,
            "description": description,
            "provenance": {"source": "assumption_registry", "status": "INSUFFICIENT_DATA"},
        }

    if expected_range is not None:
        lower, upper = expected_range
        triggered = not (lower <= observed_value <= upper)
        status_value = "DRIFTING" if triggered else "VALID"
    else:
        triggered = False
        status_value = status

    return {
        "assumption_id": assumption_id,
        "variable": variable,
        "status": status_value,
        "triggered": triggered,
        "description": description,
        "expected_range": expected_range,
        "observed_value": observed_value,
        "provenance": {"source": "assumption_registry", "status": "MODEL_DERIVED"},
    }
