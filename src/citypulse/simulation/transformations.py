from __future__ import annotations

from copy import deepcopy
from typing import Any

from citypulse.simulation.schemas import ScenarioChange, UrbanState


def _scale_numeric_mapping(mapping: dict[str, Any], multiplier: float) -> None:
    for key, value in list(mapping.items()):
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            mapping[key] = value * multiplier


def apply_change(state: UrbanState, change: ScenarioChange) -> tuple[UrbanState, list[str], list[str]]:
    result = deepcopy(state)
    affected: list[str] = []
    assumptions: list[str] = []
    parameters = change.parameters
    if change.type in {"traffic_demand_change", "demand_change"}:
        _scale_numeric_mapping(result.traffic_state, float(parameters["multiplier"]))
        _scale_numeric_mapping(result.mobility_state, float(parameters["multiplier"]))
        assumptions.append("Traffic and mobility numeric state values were scaled by the configured multiplier.")
    elif change.type == "energy_demand_change":
        _scale_numeric_mapping(result.energy_state, float(parameters["multiplier"]))
        assumptions.append("Energy numeric state values were scaled by the configured multiplier.")
    elif change.type == "weather_change":
        for key, value in parameters.items():
            if key.endswith("_multiplier") and isinstance(value, (int, float)):
                field = key.removesuffix("_multiplier")
                if field in result.weather_state and isinstance(result.weather_state[field], (int, float)):
                    result.weather_state[field] *= value
                else:
                    result.weather_state[field] = value
        assumptions.append("Weather values are hypothetical perturbations, not forecasts.")
    elif change.type in {"road_closure", "traffic_incident", "lane_reduction"}:
        segments = parameters.get("segment_ids") or [parameters.get("segment_id")]
        segments = [segment for segment in segments if segment]
        affected.extend(segments)
        for edge in result.graph_state.get("edges", []):
            if edge.get("segment_id") in segments:
                if change.type == "lane_reduction":
                    reduction = parameters["reduction"]["lanes"]
                    edge["lanes"] = max(0, edge.get("lanes", 0) - reduction)
                else:
                    edge["active"] = False
        assumptions.append("Graph effects are topology/capacity approximations, not microscopic traffic simulation.")
    elif change.type == "road_addition":
        result.graph_state.setdefault("hypothetical_edges", []).append(dict(parameters))
        assumptions.append("Added infrastructure is HYPOTHETICAL_INFRASTRUCTURE.")
    elif change.type in {"transit_disruption", "transit_station_addition"}:
        result.mobility_state.setdefault("simulated_transit_changes", []).append(dict(parameters))
        assumptions.append("Transit response is recorded as a scenario change; demand redistribution is NOT_ESTIMATED.")
    return result, affected, assumptions
