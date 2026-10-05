from __future__ import annotations

from typing import Any


def simulate_economic_shock(
    *,
    city_id: str,
    shock_type: str,
    magnitude: float,
    sectors: list[str] | None = None,
    duration_days: int = 7,
) -> dict[str, Any]:
    return {
        "city_id": city_id,
        "shock_type": shock_type,
        "magnitude": float(magnitude),
        "sectors": sectors or [],
        "duration_days": int(duration_days),
        "status": "SIMULATED",
        "evidence_level": "SCENARIO_ESTIMATE",
        "limitations": [
            "This shock is a simulation scenario and does not represent observed economic damage.",
        ],
    }
