from citypulse.evaluation.benchmark import benchmark_run, build_synthetic_scenario
from citypulse.evaluation.service import EvaluationService


def test_evaluation_service_reports_not_run_when_no_evidence_exists() -> None:
    service = EvaluationService()

    status = service.status()
    assert status["status"] == "EVALUATION_NOT_AVAILABLE"
    assert status["benchmark_status"] == "NOT_RUN"
    assert status["experiments"] == 0


def test_benchmark_run_rejects_empty_ground_truth_without_fabricating_metrics() -> None:
    result = benchmark_run([], [])

    assert result["status"] == "NOT_RUN"
    assert result["ground_truth_status"] == "GROUND_TRUTH_NOT_AVAILABLE"
    assert result["metrics"] == {}


def test_synthetic_scenario_is_marked_explicitly_as_synthetic() -> None:
    scenario = build_synthetic_scenario("traffic", {"sample_count": 12, "seed": 7})

    assert scenario["status"] == "SYNTHETIC_ONLY"
    assert scenario["domain"] == "traffic"
    assert len(scenario["rows"]) == 12
