from fastapi.testclient import TestClient

from citypulse.main import app
from citypulse.network import DependencyEngine, NetworkRegistry, UrbanNetwork


def test_network_builds_and_reports_dependency() -> None:
    network = UrbanNetwork(
        network_id="regional-mobility",
        network_name="Regional Mobility",
        network_type="mobility",
        layer="mobility",
    )
    network.add_city(
        "A",
        {
            "city_id": "A",
            "population": 120000,
            "mobility_profile": {"commuting": 0.7},
            "energy_profile": {"demand": 1.0},
        },
    )
    network.add_city(
        "B",
        {
            "city_id": "B",
            "population": 90000,
            "mobility_profile": {"commuting": 0.5},
            "energy_profile": {"demand": 0.8},
        },
    )
    network.add_city(
        "C",
        {
            "city_id": "C",
            "population": 70000,
            "mobility_profile": {"commuting": 0.3},
            "energy_profile": {"demand": 0.6},
        },
    )
    network.add_edge("A", "B", {"edge_type": "road", "weight": 4.0, "relationship_type": "OBSERVED"})
    network.add_edge("B", "C", {"edge_type": "rail", "weight": 2.0, "relationship_type": "OBSERVED"})

    metrics = network.compute_network_metrics()
    assert "node_count" in metrics
    assert metrics["node_count"] == 3
    assert "average_degree" in metrics

    dependency = DependencyEngine(network).compute_dependency("A")
    assert dependency["city_id"] == "A"
    assert "transport_dependency" in dependency["dependencies"]


def test_network_centrality_and_cascade_are_supported() -> None:
    network = UrbanNetwork(network_id="test-network", network_name="Test", network_type="mobility")
    for city_id in ["A", "B", "C", "D"]:
        network.add_city(city_id, {"city_id": city_id})
    network.add_edge("A", "B", {"weight": 3.0, "relationship_type": "OBSERVED"})
    network.add_edge("B", "C", {"weight": 2.0, "relationship_type": "OBSERVED"})
    network.add_edge("C", "D", {"weight": 2.0, "relationship_type": "OBSERVED"})
    network.add_edge("A", "D", {"weight": 1.0, "relationship_type": "OBSERVED"})

    centrality = network.compute_centrality()
    assert "A" in centrality
    assert centrality["A"]["degree_centrality"] >= 0

    cascade = network.simulate_cascade(
        origin="B",
        shock_type="road_closure",
        shock_magnitude=0.5,
        depth=2,
        scenario="MODEL_STRESS_TEST",
    )
    assert cascade["origin"] == "B"
    assert cascade["depth"] == 2
    assert cascade["status"] in {"SIMULATED", "MODEL_DERIVED"}


def test_network_api_works() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/networks")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "NETWORKS_READY"
    assert "networks" in payload


def test_registry_tracks_networks() -> None:
    registry = NetworkRegistry()
    registry.register_network(
        network_id="demo-network",
        network_name="Demo network",
        network_type="mobility",
        layer="mobility",
        spatial_scope="regional",
    )
    assert registry.get_network("demo-network")["network_id"] == "demo-network"
