from fastapi.testclient import TestClient

from citypulse.main import app
from citypulse.public_services.accessibility import compute_accessibility
from citypulse.public_services.capacity import evaluate_capacity_status
from citypulse.public_services.registry import ServiceRegistry
from citypulse.public_services.resilience import simulate_service_resilience


def test_service_registry_tracks_facility_provenance() -> None:
    registry = ServiceRegistry()
    facility = registry.register_facility(
        facility_id="clinic-a",
        service_type="HEALTHCARE",
        name="Community Clinic",
        geometry="district-1",
        latitude=12.5,
        longitude=45.1,
        administrative_area="district-1",
        ownership="public",
        operational_status="ACTIVE",
        capacity=150,
        capacity_unit="patients_per_day",
        source="government_dataset",
        source_timestamp="2024-01-01T00:00:00Z",
        confidence="documented",
    )

    assert facility["facility_id"] == "clinic-a"
    assert facility["status"] == "MODEL_DERIVED"
    assert facility["provenance"]["source"] == "government_dataset"


def test_accessibility_engine_produces_threshold_curve() -> None:
    result = compute_accessibility(
        city_id="city-a",
        service_type="HEALTHCARE",
        origins={"zone-1": {"lat": 12.5, "lon": 45.1}},
        facility_locations=[{"facility_id": "clinic-a", "lat": 12.5, "lon": 45.1, "capacity": 150}],
        thresholds=[10, 20, 30],
    )

    assert result["city_id"] == "city-a"
    assert result["service_type"] == "HEALTHCARE"
    assert result["status"] == "MODEL_DERIVED"
    assert result["accessibility_curve"][0]["threshold_minutes"] == 10


def test_capacity_throughput_and_resilience_are_labeled() -> None:
    status = evaluate_capacity_status(demand=90.0, capacity=100.0)
    resilience = simulate_service_resilience(
        city_id="city-a",
        service_type="HEALTHCARE",
        baseline_accessibility=0.8,
        shock_accessibility=0.5,
    )

    assert status["status"] == "MODEL_DERIVED"
    assert resilience["service_type"] == "HEALTHCARE"
    assert resilience["status"] == "MODEL_DERIVED"


def test_public_service_api_endpoints_exist() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/services/facilities")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "MODEL_DERIVED"
    assert "facilities" in payload
