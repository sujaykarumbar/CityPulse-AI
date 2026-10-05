from __future__ import annotations

from collections.abc import Callable
from itertools import product
from typing import Any

import numpy as np

from citypulse.validation.benchmarking.metrics import regression_metrics


def grid_search_calibration(
    observed: list[float],
    parameter_grid: dict[str, list[float]],
    simulate: Callable[[dict[str, float]], list[float]],
    max_evaluations: int = 500,
) -> dict[str, Any]:
    if not observed:
        return {"status": "GROUND_TRUTH_NOT_AVAILABLE", "candidates": []}
    if not parameter_grid or any(not values for values in parameter_grid.values()):
        raise ValueError("CALIBRATION_GRID_EMPTY")
    keys = list(parameter_grid)
    candidate_count = int(np.prod([len(parameter_grid[key]) for key in keys]))
    if candidate_count > max_evaluations:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED")
    candidates = []
    for values in product(*(parameter_grid[key] for key in keys)):
        params = dict(zip(keys, map(float, values), strict=True))
        predicted = simulate(params)
        metrics = regression_metrics(observed, predicted)
        if metrics.get("status") == "MEASURED":
            candidates.append({"parameters": params, "metrics": metrics, "objective": metrics["MAE"]})
    candidates.sort(key=lambda item: item["objective"])
    if not candidates:
        return {"status": "VALIDATION_NOT_AVAILABLE", "candidates": [], "identifiability": "IDENTIFIABILITY_NOT_ESTABLISHED"}
    return {
        "status": "MEASURED",
        "objective": "minimum MAE over supplied grid",
        "best_candidate": candidates[0],
        "candidates": candidates,
        "identifiability": "IDENTIFIABILITY_NOT_ESTABLISHED",
        "limitations": ["Grid optimum is conditional on the supplied observations, parameter grid, and simulator.", "Parameter identifiability is not inferred from best fit alone."],
    }
