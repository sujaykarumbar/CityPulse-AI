from __future__ import annotations

from typing import Any, Dict, List


def analyze_weather_extremes(city_id: str, temperatures: List[float], threshold: float) -> Dict[str, Any]:
    """Return a model-derived weather assessment for a city.

    This is intentionally conservative: it never presents synthetic output as a
    measured atmospheric truth and clearly labels provenance as model-derived.
    """
    counts = [value for value in temperatures if value >= threshold]
    maximum = max(temperatures) if temperatures else 0.0
    mean_temp = sum(temperatures) / len(temperatures) if temperatures else 0.0

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "threshold": threshold,
        "extreme_count": len(counts),
        "maximum_temperature_c": maximum,
        "mean_temperature_c": mean_temp,
        "event_label": "HEAT_EVENT" if counts else "NO_EXTREME_HEAT_SIGNAL",
        "evidence_level": "MODEL_DERIVED",
        "limitations": [
            "Synthetic or model-derived weather conditions only.",
            "No direct observation feed is required or assumed in this repository.",
        ],
    }
