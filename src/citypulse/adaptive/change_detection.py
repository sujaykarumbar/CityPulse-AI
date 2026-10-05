from __future__ import annotations

from typing import Any


def detect_change(
    *,
    metric_name: str,
    previous_value: float,
    current_value: float,
    threshold: float,
) -> dict[str, Any]:
    """Return a simple change classification for monitored urban metrics."""

    delta = abs(float(current_value) - float(previous_value))
    if delta >= float(threshold):
        change_type = "REGIME_SHIFT"
    elif delta > 0:
        change_type = "TEMPORARY_CHANGE"
    else:
        change_type = "STABLE"

    return {
        "metric_name": metric_name,
        "previous_value": float(previous_value),
        "current_value": float(current_value),
        "delta": float(delta),
        "threshold": float(threshold),
        "change_type": change_type,
        "status": "MODEL_DERIVED",
    }
