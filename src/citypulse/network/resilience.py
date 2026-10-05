from __future__ import annotations

from typing import Any

import networkx as nx


class NetworkResilienceEngine:
    """Measures connectivity, redundancy, and recovery using modeled graph structure."""

    def __init__(self, graph: Any) -> None:
        self.graph = graph

    def evaluate(self, *, shock: dict[str, Any] | None = None) -> dict[str, Any]:
        g = self.graph.to_undirected() if hasattr(self.graph, "to_undirected") else self.graph
        node_count = g.number_of_nodes()
        edge_count = g.number_of_edges()
        connected = nx.is_connected(g) if node_count > 0 else False
        components = list(nx.connected_components(g)) if node_count > 0 else []
        largest_component = max((len(component) for component in components), default=0)

        redundancy = 0.0 if node_count == 0 else (edge_count / max(node_count, 1)) / 2.0
        recovery = 0.5 if shock is None else max(0.0, min(1.0, 1.0 - float(shock.get("shock_magnitude", 0.0))))

        return {
            "status": "MODEL_DERIVED",
            "connectivity": float(1.0 if connected else largest_component / max(node_count, 1)),
            "redundancy": round(redundancy, 4),
            "recovery_capacity": round(recovery, 4),
            "node_count": node_count,
            "edge_count": edge_count,
            "largest_component_size": largest_component,
            "bottlenecks": sorted(nx.articulation_points(g)) if node_count > 0 else [],
            "limitations": [
                "Resilience metrics are modeled from graph structure and do not imply real infrastructure robustness.",
            ],
        }
