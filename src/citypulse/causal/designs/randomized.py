from __future__ import annotations


def randomized_experiment(treated_mean: float | None = None, control_mean: float | None = None) -> dict[str, object]:
    if treated_mean is None or control_mean is None:
        return {"status": "NOT_IDENTIFIED", "method": "randomized", "reason": "Randomized experiment requires both treated and control means."}
    return {"status": "MEASURED", "method": "randomized", "estimate": float(treated_mean - control_mean), "assumptions": ["random_assignment"]}
