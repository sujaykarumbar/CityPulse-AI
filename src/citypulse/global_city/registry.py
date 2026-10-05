from __future__ import annotations

from typing import Any


class CityRegistry:
    def __init__(self) -> None:
        self._cities: dict[str, dict[str, Any]] = {}

    def register_city(self, city_id: str, payload: dict[str, Any]) -> dict[str, Any]:
        city = {
            "city_id": city_id,
            "city_name": payload.get("city_name", city_id),
            "country": payload.get("country", "NOT_AVAILABLE"),
            "region": payload.get("region", "NOT_AVAILABLE"),
            "timezone": payload.get("timezone", "NOT_AVAILABLE"),
            "latitude": payload.get("latitude"),
            "longitude": payload.get("longitude"),
            "bounding_box": payload.get("bounding_box"),
            "coordinate_reference_system": payload.get("coordinate_reference_system", "WGS84"),
            "data_sources": payload.get("data_sources", []),
            "domains": payload.get("domains", {}),
            "data_quality": payload.get("data_quality", {}),
            "metadata": payload.get("metadata", {}),
        }
        self._cities[city_id] = city
        return city

    def get_city(self, city_id: str) -> dict[str, Any] | None:
        return self._cities.get(city_id)

    def list_cities(self) -> list[dict[str, Any]]:
        return list(self._cities.values())
