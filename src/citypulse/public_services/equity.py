from __future__ import annotations

from typing import Any, Dict, List


def analyze_service_equity(city_id: str, service_type: str, accessibility_scores: List[float]) -> Dict[str, Any]:
    """Compute a distribution-based equity summary using only the provided values."""
    if not accessibility_scores:
        return {
            "city_id": city_id,
            "service_type": service_type,
            "status": "MODEL_DERIVED",
            "distribution": {},
            "method": "NOT_RUN",
            "limitations": ["Accessibility scores are required to analyze equity."],
        }

    sorted_scores = sorted(accessibility_scores)
    n = len(sorted_scores)

    def percentile(p: float) -> float:
        index = min(max(int((n - 1) * p), 0), n - 1)
        return sorted_scores[index]

    return {
        "city_id": city_id,
        "service_type": service_type,
        "status": "MODEL_DERIVED",
        "distribution": {
            "mean": round(sum(accessibility_scores) / n, 3),
            "median": round(percentile(0.5), 3),
            "p10": round(percentile(0.10), 3),
            "p25": round(percentile(0.25), 3),
            "p50": round(percentile(0.50), 3),
            "p75": round(percentile(0.75), 3),
            "p90": round(percentile(0.90), 3),
        },
        "method": "DISTRIBUTIONAL_ACCESSIBILITY_ANALYSIS",
        "limitations": [
            "This is a distributional summary only and does not establish causal inequity or discrimination.",
        ],
    }
