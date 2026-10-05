from __future__ import annotations

from collections.abc import Callable

from citypulse.decision.schemas import SensitivityResult


def run_sensitivity(
    parameter: str, values: list[float], evaluate: Callable[[float], float]
) -> SensitivityResult:
    objective_values = [float(evaluate(value)) for value in values]
    return SensitivityResult(parameter=parameter, values=values, objective_values=objective_values)
