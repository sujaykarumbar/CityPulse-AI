from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter

from .air_quality import assess_air_quality
from .climate import compute_climate_baseline
from .weather import analyze_weather_extremes

router = APIRouter(prefix="/environment", tags=["environment"])


@router.get("/cities/{city_id}")
def get_environment_summary(city_id: str) -> Dict[str, Any]:
    weather = analyze_weather_extremes(
        city_id=city_id,
        temperatures=[24.0, 27.0, 29.0, 33.5, 35.0],
        threshold=31.0,
    )
    climate = compute_climate_baseline(
        city_id=city_id,
        values=[21.0, 23.0, 24.0, 26.0, 25.5],
        period="2024",
    )

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "weather": weather,
        "climate": climate,
        "evidence_level": "MODEL_DERIVED",
        "limitations": [
            "This endpoint synthesizes a representative environmental profile from project models.",
            "No real climate or weather feeds are required by this repository.",
        ],
    }


@router.get("/weather/extremes")
def get_weather_extremes(city_id: str = "city-a", threshold: float = 31.0) -> Dict[str, Any]:
    return analyze_weather_extremes(
        city_id=city_id,
        temperatures=[22.0, 25.0, 29.0, 31.5, 34.0],
        threshold=threshold,
    )


@router.get("/climate/baseline")
def get_climate_baseline(city_id: str = "city-a", period: str = "2024") -> Dict[str, Any]:
    return compute_climate_baseline(
        city_id=city_id,
        values=[20.0, 21.5, 22.5, 24.0, 23.5],
        period=period,
    )


@router.get("/air-quality")
def get_air_quality(city_id: str = "city-a", threshold: float = 35.0) -> Dict[str, Any]:
    return assess_air_quality(
        city_id=city_id,
        pm25_values=[18.0, 23.0, 41.0, 39.0, 27.0],
        threshold=threshold,
    )
