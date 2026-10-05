from __future__ import annotations

from typing import Any, Dict, List, Optional


class ServiceRegistry:
    """Lightweight registry for public-service facilities and service metadata."""

    def __init__(self) -> None:
        self.facilities: Dict[str, Dict[str, Any]] = {}

    def register_facility(
        self,
        facility_id: str,
        service_type: str,
        name: str,
        geometry: str,
        latitude: float,
        longitude: float,
        administrative_area: Optional[str] = None,
        ownership: Optional[str] = None,
        operational_status: str = "UNKNOWN",
        capacity: Optional[float] = None,
        capacity_unit: Optional[str] = None,
        opening_hours: Optional[str] = None,
        source: str = "NOT_AVAILABLE",
        source_timestamp: Optional[str] = None,
        confidence: str = "UNKNOWN",
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        facility = {
            "facility_id": facility_id,
            "service_type": service_type,
            "name": name,
            "geometry": geometry,
            "latitude": latitude,
            "longitude": longitude,
            "administrative_area": administrative_area,
            "ownership": ownership,
            "operational_status": operational_status,
            "capacity": capacity,
            "capacity_unit": capacity_unit,
            "opening_hours": opening_hours,
            "status": "MODEL_DERIVED",
            "provenance": {
                "source": source,
                "source_timestamp": source_timestamp,
                "transformation": "none",
                "confidence": confidence,
            },
            "metadata": metadata or {},
        }
        self.facilities[facility_id] = facility
        return facility

    def list_facilities(self, service_type: Optional[str] = None) -> List[Dict[str, Any]]:
        records = list(self.facilities.values())
        if service_type is not None:
            records = [record for record in records if record.get("service_type") == service_type]
        return records

    def get_facility(self, facility_id: str) -> Optional[Dict[str, Any]]:
        return self.facilities.get(facility_id)


SERVICE_CATEGORIES = {
    "EDUCATION",
    "HEALTHCARE",
    "EMERGENCY",
    "FIRE",
    "POLICE",
    "WASTE",
    "WATER_SERVICE",
    "SANITATION",
    "PUBLIC_TRANSPORT",
    "SOCIAL_SERVICE",
    "ADMINISTRATIVE",
    "PARKS",
    "RECREATION",
    "LIBRARIES",
    "COMMUNITY_CENTERS",
    "PUBLIC_HOUSING",
    "ENERGY_SERVICE",
    "DIGITAL_PUBLIC_SERVICE",
}

FACILITY_STATUSES = {
    "ACTIVE",
    "TEMPORARILY_CLOSED",
    "PLANNED",
    "UNDER_CONSTRUCTION",
    "DECOMMISSIONED",
    "UNKNOWN",
}
