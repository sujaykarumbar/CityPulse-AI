from __future__ import annotations

from typing import Any


def build_city_economic_profile(city_id: str, profile: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = profile or {}
    employment = float(payload.get("employment", 0.0))
    industry_mix = payload.get("industry_mix", {})
    if isinstance(industry_mix, dict):
        industry_mix = {str(k): float(v) for k, v in industry_mix.items()}
    diversity = float(payload.get("economic_diversity", 0.0))
    return {
        "city_id": city_id,
        "employment": employment,
        "industry_mix": industry_mix,
        "economic_diversity": diversity,
        "status": "MODEL_DERIVED",
        "evidence_level": "MODEL_DERIVED",
        "limitations": [
            "City economic profile is modeled from the available metadata and must not be treated as ground-truth economic output.",
        ],
    }
