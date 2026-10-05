from __future__ import annotations

from typing import Any


def build_city_profile(city_id: str, metrics: dict[str, Any] | None = None) -> dict[str, Any]:
    profile = {
        "city_id": city_id,
        "status": "PROFILE_BUILT",
        "metrics": metrics or {},
        "coverage": {
            "traffic": "NOT_AVAILABLE",
            "mobility": "NOT_AVAILABLE",
            "energy": "NOT_AVAILABLE",
            "weather": "NOT_AVAILABLE",
        },
        "limitations": ["City profile is generated only from available measured metadata and never from fabricated statistics."],
    }
    for key, value in (metrics or {}).items():
        if value is not None:
            profile["coverage"][key] = "MEASURED"
    return profile
