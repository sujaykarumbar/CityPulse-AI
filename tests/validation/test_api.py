from fastapi.testclient import TestClient

from citypulse.main import app
from citypulse.validation.registry.experiment_registry import ValidationRegistry
from citypulse.validation.router import service


client = TestClient(app)


def test_backtest_serializes_undefined_metrics_as_not_measured(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(service, "registry", ValidationRegistry(tmp_path))
    response = client.post(
        "/api/v1/validation/backtest",
        json={
            "task": "zero-target-edge-case",
            "observed": [0.0, 0.0],
            "predicted": [0.0, 1.0],
        },
    )

    assert response.status_code == 200
    metrics = {item["name"]: item for item in response.json()["metric_results"]}
    assert metrics["WAPE"] == {"name": "WAPE", "value": None, "status": "NOT_MEASURED", "units": None}
    assert metrics["R2"]["status"] == "NOT_MEASURED"


def test_validation_status_does_not_claim_missing_real_inputs() -> None:
    response = client.get("/api/v1/validation/status")

    assert response.status_code == 200
    assert response.json()["real_datasets"] == "NOT_AVAILABLE"
    assert response.json()["trained_models"] == "NOT_AVAILABLE"