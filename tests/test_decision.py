import pytest

from citypulse.decision.constraints import evaluate_constraints
from citypulse.decision.optimizer import solve
from citypulse.decision.pareto import dominates
from citypulse.decision.schemas import DecisionCandidate, DecisionConstraint, DecisionObjective, DecisionProblem


def problem() -> DecisionProblem:
    return DecisionProblem(
        problem_id="test",
        objectives=[
            DecisionObjective(name="time", metric="time", direction="minimize", weight=0.5),
            DecisionObjective(name="energy", metric="energy", direction="minimize", weight=0.5),
        ],
        candidates=[
            DecisionCandidate(candidate_id="a", metrics={"time": 10, "energy": 20}),
            DecisionCandidate(candidate_id="b", metrics={"time": 20, "energy": 30}),
            DecisionCandidate(candidate_id="c", metrics={"time": 8, "energy": 40}),
        ],
    )


def test_pareto_dominance() -> None:
    objectives = problem().objectives
    assert dominates({"time": 10, "energy": 20}, {"time": 20, "energy": 30}, objectives)
    assert not dominates({"time": 8, "energy": 40}, {"time": 10, "energy": 20}, objectives)


def test_solver_preserves_pareto_tradeoffs() -> None:
    result = solve(problem())

    assert set(result.pareto_candidate_ids) == {"a", "c"}
    assert all(candidate.status == "measured" for candidate in result.candidates)


def test_missing_constraint_value_is_not_available() -> None:
    constraints = evaluate_constraints(
        {"time": 10}, [DecisionConstraint(name="cost", metric="cost", direction="maximum", value=None)]
    )

    assert constraints[0].status == "NOT_AVAILABLE"
    assert not constraints[0].feasible


def test_weights_must_sum_to_one() -> None:
    invalid = problem().model_copy(update={"objectives": [problem().objectives[0]]})

    with pytest.raises(ValueError):
        solve(invalid)
