from __future__ import annotations

from typing import Any, Dict, List


def assess_air_quality(city_id: str, pm25_values: List[float], threshold: float = 35.0) -> Dict[str, Any]:
    """Return a conservative air-quality assessment based on pm25 model values."""
    above_threshold = [value for value in pm25_values if value >= threshold]
    mean_pm25 = sum(pm25_values) / len(pm25_values) if pm25_values else 0.0

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "aqi_signal": "ELEVATED" if above_threshold else "STABLE",
        "mean_pm25": round(mean_pm25, 3),
        "threshold_pm25": threshold,
        "exceedances": len(above_threshold),
        "evidence_level": "MODEL_DERIVED",
        "limitations": [
            "This assessment is derived from model inputs and is not a real-time air-monitor reading.",
        ],
    }
