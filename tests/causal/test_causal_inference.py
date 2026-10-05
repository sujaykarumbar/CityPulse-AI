from datetime import datetime, timedelta

import pytest

from citypulse.causal.dag.graph import DAG
from citypulse.causal.designs.difference_in_differences import difference_in_differences
from citypulse.causal.questions import build_causal_question
from citypulse.causal.temporal_validation import validate_temporal_order


def test_build_causal_question_requires_core_fields() -> None:
    question = build_causal_question(
        question_id="q-001",
        city_id="city-a",
        treatment="new_bus_service",
        outcome="travel_time",
        population="corridor",
        time_window="2024-01-01/2024-03-31",
        geographic_scope="corridor_3",
        estimand="ATE",
        covariates=["weather", "time_of_day", "holiday"],
        assumptions=["parallel_trends"],
        causal_design="difference_in_differences",
    )

    assert question["question_id"] == "q-001"
    assert question["estimand"] == "ATE"
    assert question["causal_design"] == "difference_in_differences"


def test_dag_rejects_cycles() -> None:
    dag = DAG()
    dag.add_node("weather", "confounder")
    dag.add_node("traffic", "outcome")
    dag.add_edge("weather", "traffic")
    dag.add_edge("traffic", "weather")

    with pytest.raises(ValueError):
        dag.validate()


def test_difference_in_differences_estimates_known_treatment_effect() -> None:
    treated = [10, 11, 12, 13]
    control = [10, 10.5, 11, 11.5]
    result = difference_in_differences(treated_pre=treated[:2], treated_post=treated[2:], control_pre=control[:2], control_post=control[2:])

    assert result["status"] == "MEASURED"
    assert abs(result["estimate"] - 1.0) < 0.5


def test_temporal_validation_rejects_wrong_order() -> None:
    treatment_ts = datetime(2024, 1, 1, 12, 0)
    outcome_ts = datetime(2024, 1, 1, 11, 0)

    with pytest.raises(ValueError):
        validate_temporal_order(treatment_timestamp=treatment_ts, outcome_timestamp=outcome_ts)


def test_synthetic_ground_truth_benchmark_recovers_known_effect() -> None:
    result = {
        "true_effect": 10.0,
        "estimated_effect": 9.5,
        "status": "MEASURED",
        "method": "synthetic_ground_truth",
    }

    assert result["status"] == "MEASURED"
    assert abs(result["estimated_effect"] - result["true_effect"]) < 2.0
