from __future__ import annotations

from itertools import product
from typing import Any


def parameter_sweep(
    base_scenario: dict[str, Any], parameter: str, values: list[float], prefix: str = "candidate"
) -> list[dict[str, Any]]:
    candidates = []
    for index, value in enumerate(values):
        scenario = {**base_scenario, "parameters": {**base_scenario.get("parameters", {}), parameter: value}}
        candidates.append({"candidate_id": f"{prefix}_{index}", "scenario": scenario})
    return candidates


def grid_sweep(base_scenario: dict[str, Any], parameters: dict[str, list[Any]]) -> list[dict[str, Any]]:
    names = list(parameters)
    candidates = []
    for index, values in enumerate(product(*(parameters[name] for name in names))):
        candidate_parameters = {**base_scenario.get("parameters", {}), **dict(zip(names, values))}
        candidates.append(
            {"candidate_id": f"grid_{index}", "scenario": {**base_scenario, "parameters": candidate_parameters}}
        )
    return candidates
