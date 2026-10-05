from __future__ import annotations

from citypulse.decision.schemas import DecisionObjective


def dominates(left: dict[str, float], right: dict[str, float], objectives: list[DecisionObjective]) -> bool:
    no_worse = True
    strictly_better = False
    for objective in objectives:
        left_value = left[objective.name]
        right_value = right[objective.name]
        if objective.direction == "minimize":
            no_worse &= left_value <= right_value
            strictly_better |= left_value < right_value
        else:
            no_worse &= left_value >= right_value
            strictly_better |= left_value > right_value
    return no_worse and strictly_better


def pareto_front(
    values_by_candidate: dict[str, dict[str, float]], objectives: list[DecisionObjective]
) -> list[str]:
    return [
        candidate_id
        for candidate_id, values in values_by_candidate.items()
        if not any(
            other_id != candidate_id and dominates(other_values, values, objectives)
            for other_id, other_values in values_by_candidate.items()
        )
    ]
