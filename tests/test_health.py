from fastapi.testclient import TestClient

from citypulse.main import app

client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_liveness_and_readiness_endpoints() -> None:
    live = client.get("/live")
    ready = client.get("/ready")

    assert live.status_code == 200
    assert live.json() == {"status": "alive"}
    assert ready.status_code == 200
    assert ready.json() == {"status": "ready", "required_dependencies": "none"}


def test_metrics_endpoint_exposes_http_request_counters() -> None:
    client.get("/health")
    response = client.get("/metrics")

    assert response.status_code == 200
    assert "citypulse_http_requests_total" in response.text
    assert 'route="/health"' in response.text


def test_system_endpoint_exposes_version() -> None:
    response = client.get("/api/v1/system")

    assert response.status_code == 200
    assert response.json()["name"] == "CityPulse API"
