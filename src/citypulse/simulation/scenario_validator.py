from __future__ import annotations

from typing import Any

from citypulse.simulation.schemas import Scenario, UrbanState


class ScenarioValidationError(ValueError):
    """Raised when a scenario cannot be safely applied."""


def _require_multiplier(parameters: dict[str, Any], name: str = "multiplier") -> float:
    value = parameters.get(name)
    if not isinstance(value, (int, float)) or value <= 0:
        raise ScenarioValidationError(f"{name} must be a positive number")
    return float(value)


def validate_scenario(scenario: Scenario, baseline: UrbanState) -> None:
    known_segments = set(baseline.graph_state.get("segment_ids", []))
    known_segments.update(
        edge.get("segment_id")
        for edge in baseline.graph_state.get("edges", [])
        if isinstance(edge, dict) and edge.get("segment_id") is not None
    )
    known_nodes = set(baseline.graph_state.get("node_ids", []))
    for change in scenario.changes:
        parameters = change.parameters
        if change.type in {"traffic_demand_change", "demand_change", "energy_demand_change"}:
            _require_multiplier(parameters)
        elif change.type == "weather_change":
            if not any(isinstance(value, (int, float)) and value >= 0 for value in parameters.values()):
                raise ScenarioValidationError("weather_change requires a non-negative numeric perturbation")
        elif change.type in {"road_closure", "lane_reduction", "traffic_incident"}:
            segment_ids = parameters.get("segment_ids") or ([parameters.get("segment_id")] if parameters.get("segment_id") else [])
            if not segment_ids or any(not isinstance(value, str) for value in segment_ids):
                raise ScenarioValidationError("road changes require segment_ids")
            if known_segments and not set(segment_ids).issubset(known_segments):
                raise ScenarioValidationError("scenario references an unknown segment")
            if change.type == "lane_reduction":
                reduction = parameters.get("reduction", {}).get("lanes")
                if not isinstance(reduction, int) or reduction < 0:
                    raise ScenarioValidationError("lane reduction must be a non-negative integer")
        elif change.type == "road_addition":
            if parameters.get("start_node") is None or parameters.get("end_node") is None:
                raise ScenarioValidationError("road_addition requires start_node and end_node")
            if known_nodes and not {parameters["start_node"], parameters["end_node"]}.issubset(known_nodes):
                raise ScenarioValidationError("road_addition references an unknown node")
        elif change.type == "transit_disruption" and not parameters.get("route_id") and not parameters.get("station_id"):
            raise ScenarioValidationError("transit_disruption requires route_id or station_id")
        elif change.type == "transit_station_addition":
            latitude = parameters.get("latitude")
            longitude = parameters.get("longitude")
            if not isinstance(latitude, (int, float)) or not isinstance(longitude, (int, float)):
                raise ScenarioValidationError("transit_station_addition requires latitude and longitude")
            if not -90 <= latitude <= 90 or not -180 <= longitude <= 180:
                raise ScenarioValidationError("transit station coordinates are outside geographic bounds")
