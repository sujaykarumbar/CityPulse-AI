from __future__ import annotations

from citypulse.decision.schemas import ConstraintResult, DecisionConstraint


def evaluate_constraints(metrics: dict[str, float], constraints: list[DecisionConstraint]) -> list[ConstraintResult]:
    results: list[ConstraintResult] = []
    for constraint in constraints:
        actual = metrics.get(constraint.metric)
        if actual is None or constraint.value is None:
            results.append(
                ConstraintResult(
                    constraint=constraint.name,
                    metric=constraint.metric,
                    threshold=constraint.value,
                    actual_value=actual,
                    feasible=False,
                    status="NOT_AVAILABLE",
                )
            )
            continue
        feasible = actual <= constraint.value if constraint.direction == "maximum" else actual >= constraint.value
        results.append(
            ConstraintResult(
                constraint=constraint.name,
                metric=constraint.metric,
                threshold=constraint.value,
                actual_value=actual,
                feasible=feasible,
                status="FEASIBLE" if feasible else "INFEASIBLE",
            )
        )
    return results
