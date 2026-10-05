from __future__ import annotations

from typing import Dict, Optional


def simulate_service_resilience(
    city_id: str,
    service_type: str,
    baseline_accessibility: float,
    shock_accessibility: float,
    recovery_accessibility: Optional[float] = None,
) -> Dict[str, Any]:
    """Model resilience as the retention of accessibility under a shock."""
    delta = baseline_accessibility - shock_accessibility
    resilience_score = max(0.0, 1.0 - delta) if baseline_accessibility > 0 else 0.0

    return {
        "city_id": city_id,
        "service_type": service_type,
        "status": "MODEL_DERIVED",
        "baseline_accessibility": baseline_accessibility,
        "shock_accessibility": shock_accessibility,
        "recovery_accessibility": recovery_accessibility,
        "accessibility_loss": round(delta, 3),
        "resilience_score": round(resilience_score, 3),
        "method": "shock_to_baseline_accessibility_delta",
        "limitations": [
            "Recovery and resilience are modeled indicators only; they are not empirically validated service outcomes.",
        ],
    }
