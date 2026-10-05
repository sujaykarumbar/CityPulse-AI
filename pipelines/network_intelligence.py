from __future__ import annotations

import argparse
import json
from pathlib import Path

from citypulse.network import DependencyEngine, NetworkRegistry, UrbanNetwork


def build_demo_network() -> UrbanNetwork:
    network = UrbanNetwork(
        network_id="regional-demo",
        network_name="Regional Demo Network",
        network_type="mobility",
        layer="mobility",
    )
    network.add_city("A", {"city_id": "A", "population": 120000})
    network.add_city("B", {"city_id": "B", "population": 90000})
    network.add_city("C", {"city_id": "C", "population": 70000})
    network.add_edge("A", "B", {"weight": 3.0, "edge_type": "road", "relationship_type": "OBSERVED"})
    network.add_edge("B", "C", {"weight": 2.0, "edge_type": "rail", "relationship_type": "ESTIMATED"})
    return network


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a simple interconnected urban network intelligence demonstration.")
    parser.add_argument("--output", default="reports/network_intelligence/demo.json")
    args = parser.parse_args()

    network = build_demo_network()
    registry = NetworkRegistry()
    registry.register_network(
        network_id=network.network_id,
        network_name=network.network_name,
        network_type=network.network_type,
        layer=network.layer,
    )
    dependencies = DependencyEngine(network).compute_all()
    payload = {
        "network": network.to_registry_record(),
        "dependencies": dependencies,
        "metrics": network.compute_network_metrics(),
        "centrality": network.compute_centrality(),
        "cascade": network.simulate_cascade(
            origin="A",
            shock_type="road_closure",
            shock_magnitude=0.6,
            depth=2,
            scenario="MODEL_STRESS_TEST",
        ),
        "registry": registry.list_networks(),
    }
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Urban network experiment written to {output_path}")


if __name__ == "__main__":
    main()
