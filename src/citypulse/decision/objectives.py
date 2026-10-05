from __future__ import annotations

from citypulse.decision.schemas import DecisionObjective


def validate_objectives(objectives: list[DecisionObjective]) -> None:
    total = sum(objective.weight for objective in objectives)
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"objective weights must sum to 1.0; received {total}")


def objective_values(candidate_metrics: dict[str, float], objectives: list[DecisionObjective]) -> dict[str, float]:
    missing = [objective.metric for objective in objectives if objective.metric not in candidate_metrics]
    if missing:
        raise ValueError(f"objective metrics unavailable: {', '.join(missing)}")
    return {objective.name: float(candidate_metrics[objective.metric]) for objective in objectives}


def weighted_score(values: dict[str, float], objectives: list[DecisionObjective]) -> float:
    score = 0.0
    for objective in objectives:
        value = values[objective.name]
        score += objective.weight * (value if objective.direction == "minimize" else -value)
    return score
