from __future__ import annotations

from citypulse.simulation.comparison import compare_states
from citypulse.simulation.scenario_validator import validate_scenario
from citypulse.simulation.schemas import Scenario, SimulationResult, UrbanState
from citypulse.simulation.transformations import apply_change


def run_scenario(scenario: Scenario, baseline: UrbanState) -> SimulationResult:
    validate_scenario(scenario, baseline)
    current = baseline.model_copy(deep=True)
    affected: list[str] = []
    assumptions: list[str] = []
    for change in scenario.changes:
        current, change_affected, change_assumptions = apply_change(current, change)
        affected.extend(change_affected)
        assumptions.extend(change_assumptions)
    current.metadata.update(
        {
            "scenario_id": scenario.scenario_id,
            "scenario_mode": "SIMULATED",
            "causal_effect": "CAUSAL_EFFECT_NOT_ESTABLISHED",
        }
    )
    return SimulationResult(
        scenario_id=scenario.scenario_id,
        scenario_name=scenario.name,
        status="completed",
        baseline=baseline,
        scenario=current,
        deltas=compare_states(baseline, current),
        affected_regions=sorted(set(affected)),
        assumptions=sorted(set(assumptions)),
        limitations=[
            "Scenario outputs are model-based counterfactual estimates, not guarantees.",
            "Risk recalculation is NOT_AVAILABLE because no Phase 10 risk engine exists in this checkout.",
        ],
    )
