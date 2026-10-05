from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from citypulse.public_services.accessibility import compute_accessibility
from citypulse.public_services.capacity import evaluate_capacity_status
from citypulse.public_services.demand import estimate_service_demand, forecast_service_demand
from citypulse.public_services.equity import analyze_service_equity
from citypulse.public_services.graph import ServiceDependencyGraph
from citypulse.public_services.optimization import optimize_facility_locations
from citypulse.public_services.registry import ServiceRegistry
from citypulse.public_services.resilience import simulate_service_resilience
from citypulse.public_services.scenarios import run_service_scenario

router = APIRouter(prefix="/services", tags=["public-services"])
registry = ServiceRegistry()

# Seed a minimal research-safe registry representative of a city planning dataset.
registry.register_facility(
    facility_id="clinic-a",
    service_type="HEALTHCARE",
    name="Central Clinic",
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
registry.register_facility(
    facility_id="school-a",
    service_type="EDUCATION",
    name="North School",
    geometry="district-2",
    latitude=12.6,
    longitude=45.2,
    administrative_area="district-2",
    ownership="public",
    operational_status="ACTIVE",
    capacity=420,
    capacity_unit="students",
    source="government_dataset",
    source_timestamp="2024-01-01T00:00:00Z",
    confidence="documented",
)


@router.get("")
def list_service_categories() -> Dict[str, Any]:
    return {
        "status": "MODEL_DERIVED",
        "service_types": ["HEALTHCARE", "EDUCATION", "EMERGENCY", "WASTE", "PUBLIC_TRANSPORT"],
        "method": "catalogue_based",
    }


@router.get("/facilities")
def list_facilities() -> Dict[str, Any]:
    return {
        "status": "MODEL_DERIVED",
        "facilities": registry.list_facilities(),
        "method": "facility_registry",
    }


@router.get("/public-facilities")
def list_public_facilities() -> Dict[str, Any]:
    return list_facilities()


@router.get("/facilities/{facility_id}")
def get_facility(facility_id: str) -> Dict[str, Any]:
    facility = registry.get_facility(facility_id)
    if facility is None:
        raise HTTPException(status_code=404, detail={"code": "FACILITY_NOT_FOUND"})
    return {"status": "MODEL_DERIVED", "facility": facility}


@router.get("/public-facilities/{facility_id}")
def get_public_facility(facility_id: str) -> Dict[str, Any]:
    return get_facility(facility_id)


@router.post("/facilities")
def register_facility(payload: Dict[str, Any]) -> Dict[str, Any]:
    facility = registry.register_facility(
        facility_id=str(payload.get("facility_id", "unknown")),
        service_type=str(payload.get("service_type", "UNKNOWN")),
        name=str(payload.get("name", "unnamed-facility")),
        geometry=str(payload.get("geometry", "unknown")),
        latitude=float(payload.get("latitude", 0.0)),
        longitude=float(payload.get("longitude", 0.0)),
        administrative_area=payload.get("administrative_area"),
        ownership=payload.get("ownership"),
        operational_status=str(payload.get("operational_status", "UNKNOWN")),
        capacity=payload.get("capacity"),
        capacity_unit=payload.get("capacity_unit"),
        opening_hours=payload.get("opening_hours"),
        source=str(payload.get("source", "NOT_AVAILABLE")),
        source_timestamp=payload.get("source_timestamp"),
        confidence=str(payload.get("confidence", "UNKNOWN")),
        metadata=payload.get("metadata", {}),
    )
    return {"status": "MODEL_DERIVED", "facility": facility}


@router.post("/accessibility/analyze")
def analyze_accessibility(payload: Dict[str, Any]) -> Dict[str, Any]:
    return compute_accessibility(
        city_id=str(payload.get("city_id", "unknown")),
        service_type=str(payload.get("service_type", "HEALTHCARE")),
        origins=payload.get("origins", {}),
        facility_locations=payload.get("facility_locations", []),
        thresholds=payload.get("thresholds", [10, 20, 30]),
    )


@router.get("/demand")
def get_demand() -> Dict[str, Any]:
    return estimate_service_demand(
        city_id="city-a",
        service_type="HEALTHCARE",
        population=1200.0,
        proxy_label="PROXY",
    )


@router.post("/demand/forecast")
def forecast_demand(payload: Dict[str, Any]) -> Dict[str, Any]:
    return forecast_service_demand(
        city_id=str(payload.get("city_id", "unknown")),
        service_type=str(payload.get("service_type", "HEALTHCARE")),
        history=payload.get("history", [1200.0, 1280.0, 1360.0]),
        horizon=int(payload.get("horizon", 1)),
    )


@router.get("/capacity")
def get_capacity() -> Dict[str, Any]:
    return evaluate_capacity_status(demand=90.0, capacity=100.0)


@router.get("/equity")
def get_equity() -> Dict[str, Any]:
    return analyze_service_equity(
        city_id="city-a",
        service_type="HEALTHCARE",
        accessibility_scores=[0.35, 0.55, 0.7, 0.8, 0.9],
    )


@router.get("/resilience")
def get_resilience() -> Dict[str, Any]:
    return simulate_service_resilience(
        city_id="city-a",
        service_type="HEALTHCARE",
        baseline_accessibility=0.8,
        shock_accessibility=0.5,
    )


@router.post("/scenarios/run")
def run_scenario(payload: Dict[str, Any]) -> Dict[str, Any]:
    return run_service_scenario(
        city_id=str(payload.get("city_id", "unknown")),
        service_type=str(payload.get("service_type", "HEALTHCARE")),
        scenario=str(payload.get("scenario", "facility_closure")),
        assumptions=payload.get("assumptions", {}),
    )


@router.post("/optimization/location")
def optimize_location(payload: Dict[str, Any]) -> Dict[str, Any]:
    return optimize_facility_locations(
        city_id=str(payload.get("city_id", "unknown")),
        candidates=payload.get("candidates", []),
        objective_weights=payload.get("objective_weights"),
        budget=payload.get("budget"),
    )


@router.get("/service-resilience")
def get_service_resilience() -> Dict[str, Any]:
    return get_resilience()


@router.get("/dependency-graph")
def get_dependency_graph() -> Dict[str, Any]:
    graph = ServiceDependencyGraph()
    graph.add_node("clinic-a", "facility", {"service_type": "HEALTHCARE"})
    graph.add_node("power-grid", "infrastructure", {"service_type": "ENERGY_SERVICE"})
    graph.add_edge("clinic-a", "power-grid", "DEPENDS_ON", evidence="MODEL_ESTIMATE")
    return graph.summary()
