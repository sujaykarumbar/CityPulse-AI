from __future__ import annotations

from typing import Any, Dict, List, Sequence


def compute_accessibility(
    city_id: str,
    service_type: str,
    origins: Dict[str, Dict[str, float]],
    facility_locations: Sequence[Dict[str, Any]],
    thresholds: Sequence[int] | None = None,
) -> Dict[str, Any]:
    """Compute a simple model-derived accessibility summary for a service type.

    This intentionally uses a conservative, transparent approximation that does not
    treat proximity as proof of service quality or actual observed accessibility.
    """
    thresholds = list(thresholds or [5, 10, 15, 30, 45, 60])
    curve = []
    for threshold in thresholds:
        coverage_points = 0
        for origin in origins.values():
            for facility in facility_locations:
                lat_delta = abs(float(origin.get("lat", 0.0)) - float(facility.get("lat", 0.0)))
                lon_delta = abs(float(origin.get("lon", 0.0)) - float(facility.get("lon", 0.0)))
                distance_km = ((lat_delta ** 2) + (lon_delta ** 2)) ** 0.5 * 111.0
                if distance_km <= threshold / 10.0:
                    coverage_points += 1
        curve.append({
            "threshold_minutes": threshold,
            "accessible_facilities": coverage_points,
            "method": "MODELED_DISTANCE_PROXY",
            "status": "MODEL_DERIVED",
        })

    nearest_facility = None
    nearest_distance = None
    for facility in facility_locations:
        for origin in origins.values():
            lat_delta = abs(float(origin.get("lat", 0.0)) - float(facility.get("lat", 0.0)))
            lon_delta = abs(float(origin.get("lon", 0.0)) - float(facility.get("lon", 0.0)))
            distance = ((lat_delta ** 2) + (lon_delta ** 2)) ** 0.5 * 111.0
            if nearest_distance is None or distance < nearest_distance:
                nearest_distance = distance
                nearest_facility = facility.get("facility_id", "unknown")

    return {
        "city_id": city_id,
        "service_type": service_type,
        "status": "MODEL_DERIVED",
        "methodology": "distance_based_accessibility_proxy",
        "evidence_level": "MODEL_DERIVED",
        "nearest_facility": nearest_facility,
        "nearest_distance_km": round(nearest_distance or 0.0, 3),
        "accessibility_curve": curve,
        "limitations": [
            "This is a modeled proxy and is not a validated travel-time or service-quality assessment.",
            "No ground-truth facility access data is assumed.",
        ],
    }
