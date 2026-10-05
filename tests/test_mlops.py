from pathlib import Path

import pytest

from citypulse.mlops.drift import calculate_drift
from citypulse.mlops.monitoring import regression_metrics
from citypulse.mlops.registry import ModelRegistry
from citypulse.mlops.schemas import ModelRecord
from citypulse.mlops.validation import validate_model
from fastapi.testclient import TestClient
from citypulse.main import app


def record() -> ModelRecord:
    return ModelRecord(model_id="m1", model_name="traffic", model_version="v1", model_type="baseline", domain="TRAFFIC", task="forecast", framework="sklearn", metrics={"mae": 2.0}, dataset_version="d1", feature_version="f1")


def test_registry_duplicate_and_lifecycle(tmp_path: Path) -> None:
    registry = ModelRegistry(tmp_path)
    registry.register(record())
    with pytest.raises(ValueError, match="ALREADY"):
        registry.register(record())
    registry.transition("traffic", "v1", "VALIDATING", "tester")
    registry.transition("traffic", "v1", "VALIDATED", "tester")
    assert registry.get("traffic", "v1").lifecycle == "VALIDATED"


def test_validation_warns_when_artifact_is_not_configured(tmp_path: Path) -> None:
    result = validate_model(record(), {})

    assert result.status == "WARN"
    assert any(check.name == "artifact_uri" for check in result.checks)


def test_drift_requires_threshold_for_status() -> None:
    result = calculate_drift("speed", [1, 2, 3], [10, 11, 12])

    assert result.status == "NOT_MEASURABLE"
    assert result.sample_size_current == 3


def test_performance_requires_aligned_ground_truth() -> None:
    assert regression_metrics([], []) == {"status": "GROUND_TRUTH_NOT_AVAILABLE"}


def test_mlops_models_endpoint_returns_registry_records() -> None:
    response = TestClient(app).get("/api/v1/mlops/models")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
