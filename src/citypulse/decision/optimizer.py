from __future__ import annotations

from citypulse.decision.constraints import evaluate_constraints
from citypulse.decision.objectives import objective_values, validate_objectives, weighted_score
from citypulse.decision.pareto import pareto_front
from citypulse.decision.schemas import CandidateResult, DecisionProblem, DecisionResult


def solve(problem: DecisionProblem) -> DecisionResult:
    validate_objectives(problem.objectives)
    results: list[CandidateResult] = []
    measured_values: dict[str, dict[str, float]] = {}
    for candidate in problem.candidates:
        constraints = evaluate_constraints(candidate.metrics, problem.constraints)
        if any(result.status == "NOT_AVAILABLE" for result in constraints):
            results.append(
                CandidateResult(
                    candidate_id=candidate.candidate_id,
                    objective_values={},
                    constraints=constraints,
                    feasible=False,
                    weighted_score=None,
                    status="not_available",
                )
            )
            continue
        try:
            values = objective_values(candidate.metrics, problem.objectives)
        except ValueError:
            results.append(
                CandidateResult(
                    candidate_id=candidate.candidate_id,
                    objective_values={},
                    constraints=constraints,
                    feasible=False,
                    weighted_score=None,
                    status="not_run",
                )
            )
            continue
        feasible = all(result.feasible for result in constraints)
        results.append(
            CandidateResult(
                candidate_id=candidate.candidate_id,
                objective_values=values,
                constraints=constraints,
                feasible=feasible,
                weighted_score=weighted_score(values, problem.objectives),
                status="measured",
            )
        )
        if feasible:
            measured_values[candidate.candidate_id] = values
    return DecisionResult(
        problem_id=problem.problem_id,
        candidates=results,
        pareto_candidate_ids=pareto_front(measured_values, problem.objectives),
        limitations=[
            "Pareto solutions are trade-offs, not universal recommendations.",
            "Causal effects are not established by objective comparisons.",
        ],
    )
