from __future__ import annotations

from typing import Any

from fastapi import APIRouter, HTTPException

from citypulse.network.graph import DependencyEngine, UrbanNetwork
from citypulse.network.registry import NetworkRegistry
from citypulse.network.resilience import NetworkResilienceEngine

router = APIRouter(prefix="/networks", tags=["urban-network"])
registry = NetworkRegistry()


@router.get("")
def list_networks() -> dict[str, Any]:
    return {"status": "NETWORKS_READY", "networks": registry.list_networks()}


@router.get("/{network_id}")
def get_network(network_id: str) -> dict[str, Any]:
    network_record = registry.get_network(network_id)
    if network_record is None:
        raise HTTPException(status_code=404, detail={"code": "NETWORK_NOT_FOUND"})
    return {"network_id": network_id, "record": network_record}


@router.post("/build")
def build_network(payload: dict[str, Any]) -> dict[str, Any]:
    network_id = str(payload.get("network_id", "network-1"))
    network = UrbanNetwork(
        network_id=network_id,
        network_name=str(payload.get("network_name", network_id)),
        network_type=str(payload.get("network_type", "mobility")),
        layer=str(payload.get("layer", "mobility")),
        directed=bool(payload.get("directed", True)),
        metadata=payload.get("metadata", {}),
    )
    for city_id, profile in payload.get("cities", {}).items():
        network.add_city(city_id, profile)
    for edge in payload.get("edges", []):
        network.add_edge(edge["source"], edge["target"], edge.get("attributes", {}))
    registry.register_network(
        network_id=network.network_id,
        network_name=network.network_name,
        network_type=network.network_type,
        layer=network.layer,
        spatial_scope=str(payload.get("spatial_scope", "regional")),
        temporal_scope=str(payload.get("temporal_scope", "current")),
        source=str(payload.get("source", "synthetic")),
        methodology=str(payload.get("methodology", "MODELED")),
        version=str(payload.get("version", "v1")),
    )
    return {"status": "MODEL_DERIVED", "network": network.to_registry_record()}


@router.get("/{network_id}/metrics")
def get_network_metrics(network_id: str) -> dict[str, Any]:
    network = _load_network(network_id)
    return network.compute_network_metrics()


@router.get("/{network_id}/centrality")
def get_network_centrality(network_id: str) -> dict[str, Any]:
    network = _load_network(network_id)
    return network.compute_centrality()


@router.get("/{network_id}/dependencies")
def get_network_dependencies(network_id: str) -> dict[str, Any]:
    network = _load_network(network_id)
    engine = DependencyEngine(network)
    return engine.compute_all()


@router.post("/shocks")
def create_shock(payload: dict[str, Any]) -> dict[str, Any]:
    network = _load_network(str(payload.get("network_id", "network-1")))
    return network.simulate_cascade(
        origin=str(payload.get("origin", "unknown")),
        shock_type=str(payload.get("shock_type", "road_closure")),
        shock_magnitude=float(payload.get("shock_magnitude", 0.5)),
        depth=int(payload.get("depth", 2)),
        scenario=str(payload.get("scenario", "SCENARIO_ESTIMATE")),
    )


@router.post("/cascade")
def simulate_cascade(payload: dict[str, Any]) -> dict[str, Any]:
    return create_shock(payload)


@router.post("/resilience")
def evaluate_resilience(payload: dict[str, Any]) -> dict[str, Any]:
    network = _load_network(str(payload.get("network_id", "network-1")))
    engine = NetworkResilienceEngine(network.graph)
    return engine.evaluate(shock={"shock_magnitude": float(payload.get("shock_magnitude", 0.5))})


@router.post("/policy-simulation")
def multi_city_policy(payload: dict[str, Any]) -> dict[str, Any]:
    from citypulse.network.policy import MultiCityPolicySimulation

    simulation = MultiCityPolicySimulation(city_policies=payload.get("city_policies", {}))
    return simulation.simulate()


@router.get("/tradeoffs")
def tradeoff_summary() -> dict[str, Any]:
    return {"status": "NOT_RUN", "tradeoffs": [], "limitations": ["Trade-off analytics require explicit city-level policy inputs."]}


@router.get("/futures")
def network_futures() -> dict[str, Any]:
    return {
        "status": "MODEL_DERIVED",
        "future_scenarios": [
            "High Regional Growth",
            "Low Regional Growth",
            "Transit Integration",
            "Energy Stress",
        ],
        "limitations": ["These are synthetic scenario labels only and not observed futures."],
    }


@router.get("/knowledge-graph")
def knowledge_graph() -> dict[str, Any]:
    return {
        "status": "GRAPH_AVAILABLE",
        "relationships": [
            {"source": "City A", "target": "City B", "relationship": "CONNECTED_TO", "provenance": "synthetic"},
        ],
    }


def _load_network(network_id: str) -> UrbanNetwork:
    record = registry.get_network(network_id)
    if record is None:
        # A minimal synthetic network is created when none already exists.
        network = UrbanNetwork(
            network_id=network_id,
            network_name=network_id,
            network_type="mobility",
            layer="mobility",
        )
        network.add_city("city-a", {"city_id": "city-a"})
        network.add_city("city-b", {"city_id": "city-b"})
        network.add_edge("city-a", "city-b", {"weight": 1.0, "relationship_type": "ASSUMED"})
        registry.register_network(
            network_id=network_id,
            network_name=network.network_name,
            network_type=network.network_type,
            layer=network.layer,
        )
        return network
    return UrbanNetwork(
        network_id=network_id,
        network_name=record.get("network_name", network_id),
        network_type=record.get("network_type", "mobility"),
        layer=record.get("layer", "mobility"),
    )
