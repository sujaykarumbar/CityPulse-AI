from __future__ import annotations

from citypulse.environment.climate import compute_climate_baseline
from citypulse.environment.weather import analyze_weather_extremes


def run_environmental_profile(city_id: str) -> dict:
    """Construct a model-derived environmental profile for a city."""
    weather = analyze_weather_extremes(
        city_id=city_id,
        temperatures=[24.0, 27.0, 29.0, 32.0, 35.5],
        threshold=30.0,
    )
    climate = compute_climate_baseline(
        city_id=city_id,
        values=[22.0, 23.0, 24.0, 25.0, 25.5],
        period="2025",
    )

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "weather": weather,
        "climate": climate,
    }
