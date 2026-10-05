from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class CityRecord(BaseModel):
    city_id: str = Field(min_length=1)
    city_name: str = Field(min_length=1)
    country: str | None = None
    region: str | None = None
    timezone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    bounding_box: dict[str, float] | None = None
    coordinate_reference_system: str = "WGS84"
    data_sources: list[str] = Field(default_factory=list)
    available_domains: dict[str, bool] = Field(default_factory=dict)
    data_quality: dict[str, Any] = Field(default_factory=dict)
    metadata: dict[str, Any] = Field(default_factory=dict)
