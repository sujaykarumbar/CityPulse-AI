from __future__ import annotations

from numbers import Real
from typing import Any

from citypulse.simulation.schemas import MetricDelta, UrbanState


def _numeric_values(prefix: str, value: Any) -> list[tuple[str, float]]:
    if isinstance(value, Real) and not isinstance(value, bool):
        return [(prefix, float(value))]
    if isinstance(value, dict):
        rows: list[tuple[str, float]] = []
        for key, child in value.items():
            rows.extend(_numeric_values(f"{prefix}.{key}", child))
        return rows
    return []


def compare_states(baseline: UrbanState, scenario: UrbanState) -> list[MetricDelta]:
    baseline_values = dict(_numeric_values("traffic", baseline.traffic_state))
    scenario_values = dict(_numeric_values("traffic", scenario.traffic_state))
    for root, value in (("mobility", baseline.mobility_state), ("energy", baseline.energy_state)):
        baseline_values.update(dict(_numeric_values(root, value)))
    for root, value in (("mobility", scenario.mobility_state), ("energy", scenario.energy_state)):
        scenario_values.update(dict(_numeric_values(root, value)))
    deltas = []
    for metric in sorted(baseline_values.keys() & scenario_values.keys()):
        baseline_value = baseline_values[metric]
        scenario_value = scenario_values[metric]
        delta = scenario_value - baseline_value
        deltas.append(
            MetricDelta(
                metric=metric,
                baseline_value=baseline_value,
                scenario_value=scenario_value,
                absolute_delta=delta,
                percentage_delta=(delta / baseline_value * 100) if baseline_value else None,
            )
        )
    return deltas
