from __future__ import annotations


def analyze_specialization(
    *,
    city_id: str,
    sector: str,
    share: float,
    reference_share: float,
    period: str,
) -> dict[str, float | str]:
    value = float(share) / float(reference_share) if reference_share else 1.0
    return {
        "city_id": city_id,
        "sector": sector,
        "period": period,
        "value": round(value, 4),
        "metric": "location_quotient",
        "status": "MODEL_DERIVED",
    }
