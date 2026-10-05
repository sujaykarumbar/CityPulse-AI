from __future__ import annotations

from typing import Any, Dict, List


def compute_climate_baseline(city_id: str, values: List[float], period: str) -> Dict[str, Any]:
    """Compute a climate baseline from a model-derived time series."""
    if not values:
        return {
            "city_id": city_id,
            "period": period,
            "status": "MODEL_DERIVED",
            "baseline_mean_c": 0.0,
            "baseline_std_c": 0.0,
            "baseline_min_c": 0.0,
            "baseline_max_c": 0.0,
            "evidence_level": "MODEL_DERIVED",
            "limitations": ["No observed climate feed is available in this environment."],
        }

    mean = sum(values) / len(values)
    variance = sum((value - mean) ** 2 for value in values) / len(values)
    std_dev = variance ** 0.5

    return {
        "city_id": city_id,
        "period": period,
        "status": "MODEL_DERIVED",
        "baseline_mean_c": round(mean, 3),
        "baseline_std_c": round(std_dev, 3),
        "baseline_min_c": min(values),
        "baseline_max_c": max(values),
        "evidence_level": "MODEL_DERIVED",
        "limitations": [
            "This baseline is computationally derived from the available model inputs only.",
            "It is not a claim about observed long-term climate behavior.",
        ],
    }
