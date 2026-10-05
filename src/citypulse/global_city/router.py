from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.global_city.profile.generator import build_city_profile
from citypulse.global_city.registry import CityRegistry
from citypulse.global_city.similarity import city_similarity

router = APIRouter(prefix="/global", tags=["global-city"])
registry = CityRegistry()


@router.get("/cities")
def list_cities() -> list[dict]:
    return registry.list_cities()


@router.get("/cities/{city_id}")
def get_city(city_id: str) -> dict:
    city = registry.get_city(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail={"code": "CITY_NOT_FOUND"})
    return city


@router.get("/cities/{city_id}/profile")
def city_profile(city_id: str) -> dict:
    city = registry.get_city(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail={"code": "CITY_NOT_FOUND"})
    return build_city_profile(city_id, city.get("data_quality", {}))


@router.post("/cities/compare")
def compare_cities(payload: dict) -> dict:
    left = payload.get("left", {})
    right = payload.get("right", {})
    return city_similarity(left, right)


@router.get("/cities/{city_id}/similar")
def similar_cities(city_id: str) -> dict:
    city = registry.get_city(city_id)
    if city is None:
        raise HTTPException(status_code=404, detail={"code": "CITY_NOT_FOUND"})
    return {
        "city_id": city_id,
        "similar_cities": [],
        "status": "NOT_RUN",
        "limitations": ["No measured city-similarity experiment exists for this city yet."],
    }
