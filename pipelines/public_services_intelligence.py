from __future__ import annotations

from citypulse.public_services.accessibility import compute_accessibility
from citypulse.public_services.capacity import evaluate_capacity_status
from citypulse.public_services.demand import estimate_service_demand
from citypulse.public_services.registry import ServiceRegistry


def run_public_services_profile(city_id: str) -> dict:
    """Construct a model-derived public-service intelligence profile for a city."""
    registry = ServiceRegistry()
    registry.register_facility(
        facility_id="clinic-demo",
        service_type="HEALTHCARE",
        name="Demo Clinic",
        geometry="demo-zone",
        latitude=12.5,
        longitude=45.1,
        administrative_area="demo-zone",
        ownership="public",
        operational_status="ACTIVE",
        capacity=120.0,
        capacity_unit="patients_per_day",
        source="synthetic",
        source_timestamp="2025-01-01T00:00:00Z",
        confidence="modeled",
    )

    accessibility = compute_accessibility(
        city_id=city_id,
        service_type="HEALTHCARE",
        origins={"zone-1": {"lat": 12.5, "lon": 45.1}},
        facility_locations=[{"facility_id": "clinic-demo", "lat": 12.5, "lon": 45.1, "capacity": 120.0}],
    )
    demand = estimate_service_demand(
        city_id=city_id,
        service_type="HEALTHCARE",
        population=1000.0,
        proxy_label="PROXY",
    )
    capacity = evaluate_capacity_status(demand=90.0, capacity=120.0)

    return {
        "city_id": city_id,
        "status": "MODEL_DERIVED",
        "facilities": registry.list_facilities(),
        "accessibility": accessibility,
        "demand": demand,
        "capacity": capacity,
    }
