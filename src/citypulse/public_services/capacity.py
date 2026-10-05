from __future__ import annotations

from typing import Any, Dict, Optional


def evaluate_capacity_status(
    demand: Optional[float],
    capacity: Optional[float],
    thresholds: Optional[Dict[str, float]] = None,
) -> Dict[str, Any]:
    """Calculate a conservative capacity utilization signal."""
    thresholds = thresholds or {"underutilized": 0.5, "high": 0.85, "over_capacity": 1.0}
    if demand is None or capacity is None or capacity <= 0:
        return {
            "status": "MODEL_DERIVED",
            "capacity_utilization": None,
            "alert": "UNKNOWN",
            "method": "capacity_missing_or_invalid",
            "limitations": ["Demand and capacity must be valid and compatible before utilization is interpreted."],
        }

    utilization = demand / capacity
    if utilization < thresholds["underutilized"]:
        alert = "UNDERUTILIZED"
    elif utilization < thresholds["high"]:
        alert = "NORMAL"
    elif utilization < thresholds["over_capacity"]:
        alert = "HIGH_UTILIZATION"
    else:
        alert = "OVER_CAPACITY"

    return {
        "status": "MODEL_DERIVED",
        "demand": demand,
        "capacity": capacity,
        "capacity_utilization": round(utilization, 3),
        "alert": alert,
        "thresholds": thresholds,
        "limitations": [
            "Nominal capacity does not imply actual service availability.",
            "Availability depends on staffing, opening hours, and operational conditions.",
        ],
    }
