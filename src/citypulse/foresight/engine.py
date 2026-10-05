from __future__ import annotations

from datetime import datetime
from random import Random
from typing import Any

from .schemas import FutureDriver, FutureScenario


def generate_future_scenarios(
    *,
    city_id: str,
    horizon_years: int = 10,
    seed: int = 0,
    policy_assumptions: dict[str, Any] | None = None,
    scenario_count: int = 3,
) -> list[FutureScenario]:
    """Create structured, synthetic future scenarios for long-horizon planning.

    These are not empirical forecasts. They are explicitly scenario-based estimates
    designed to support strategy exploration and planning review.
    """

    rng = Random(seed)
    assumptions = policy_assumptions or {}
    scenarios: list[FutureScenario] = []

    for index in range(scenario_count):
        year_offset = horizon_years * (index + 1)
        base_population = 1.0 + (index * 0.08)
        transit_factor = 1.0 + assumptions.get("transit_investment", 1.0) * 0.15
        charging_factor = 1.0 + assumptions.get("ev_adoption", 0.2) * (index + 1) * 0.08
        drivers = [
            FutureDriver(
                name="population_growth",
                category="demographic",
                value=round(base_population + rng.uniform(-0.03, 0.05), 4),
                lower_bound=0.9,
                upper_bound=1.4,
                unit="index",
            ),
            FutureDriver(
                name="transit_investment",
                category="mobility",
                value=round(transit_factor, 4),
                lower_bound=0.8,
                upper_bound=1.5,
                unit="index",
            ),
            FutureDriver(
                name="ev_adoption",
                category="technology",
                value=round(charging_factor, 4),
                lower_bound=0.8,
                upper_bound=1.7,
                unit="index",
            ),
        ]
        start_year = 2026
        end_year = start_year + year_offset
        scenario = FutureScenario(
            scenario_id=f"{city_id}-future-{index + 1}",
            scenario_name=f"Scenario {index + 1}",
            city_id=city_id,
            start_time=datetime(start_year, 1, 1).isoformat(),
            end_time=datetime(end_year, 1, 1).isoformat(),
            horizon_years=horizon_years,
            assumptions={
                "policy_assumptions": assumptions,
                "status": "SCENARIO_ESTIMATE",
                "model_family": "synthetic_urban_evolution",
            },
            drivers=drivers,
            random_seed=seed + index,
            provenance={
                "status": "SCENARIO_ESTIMATE",
                "data_origin": "SYNTHETIC",
                "notes": "Synthetic futures are used for planning exploration and must be validated against observed data before strategic use.",
            },
        )
        scenarios.append(scenario)

    return scenarios


class UrbanEvolutionEngine:
    """Models simple state evolution under policy and behavioral assumptions."""

    def __init__(self, *, seed: int = 0) -> None:
        self.seed = seed

    def simulate_future(
        self,
        *,
        baseline: dict[str, float],
        policy: dict[str, float] | None = None,
        horizon_years: int = 5,
    ) -> dict[str, Any]:
        policy = policy or {}
        state = dict(baseline)
        states: list[dict[str, float]] = [state.copy()]

        for year in range(1, horizon_years + 1):
            transit_factor = float(policy.get("transit_investment", 1.0))
            demand_growth = 1.0 + (0.04 * year) + (0.02 * max(0.0, transit_factor - 1.0))
            energy_growth = 1.0 + (0.02 * year) + (0.03 * max(0.0, policy.get("ev_adoption", 0.2) - 0.1))
            next_state = {
                "population": round(float(state.get("population", 1.0)) * (1.0 + 0.02 * year), 6),
                "mobility": round(float(state.get("mobility", 1.0)) * demand_growth, 6),
                "energy": round(float(state.get("energy", 1.0)) * energy_growth, 6),
                "risk": round(float(state.get("risk", 0.1)) + (0.02 * year * (1.0 / max(1.0, transit_factor))), 6),
                "policy_pressure": round(float(policy.get("policy_pressure", 0.5)) + (0.05 * year), 6),
            }
            states.append(next_state)
            state = next_state

        return {
            "status": "SCENARIO_ESTIMATE",
            "horizon_years": horizon_years,
            "states": states,
            "assumptions": {
                "policy": policy,
                "mode": "synthetic_urban_evolution",
                "note": "This is a model-based future-state estimate and not a verified forecast.",
            },
        }
