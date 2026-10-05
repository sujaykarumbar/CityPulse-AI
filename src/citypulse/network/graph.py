from __future__ import annotations

from collections import defaultdict, deque
from typing import Any

import networkx as nx


class UrbanNetwork:
    """A lightweight multi-city graph that stores network semantics without claiming real infrastructure truth."""

    def __init__(
        self,
        *,
        network_id: str,
        network_name: str,
        network_type: str,
        layer: str = "mobility",
        directed: bool = True,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        self.network_id = network_id
        self.network_name = network_name
        self.network_type = network_type
        self.layer = layer
        self.directed = directed
        self.metadata = metadata or {}
        self.graph = nx.DiGraph() if directed else nx.Graph()
        self._city_profiles: dict[str, dict[str, Any]] = {}

    def add_city(self, city_id: str, profile: dict[str, Any] | None = None) -> dict[str, Any]:
        profile = profile or {}
        self.graph.add_node(city_id)
        self._city_profiles[city_id] = {"city_id": city_id, **profile}
        return self._city_profiles[city_id]

    def add_edge(
        self,
        source: str,
        target: str,
        attributes: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        if source not in self.graph:
            self.add_city(source)
        if target not in self.graph:
            self.add_city(target)
        payload = {
            "source": source,
            "target": target,
            "edge_type": attributes.get("edge_type", "unknown") if attributes else "unknown",
            "direction": attributes.get("direction", "forward") if attributes else "forward",
            "weight": float(attributes.get("weight", 1.0)) if attributes else 1.0,
            "unit": attributes.get("unit", "index") if attributes else "index",
            "timestamp": attributes.get("timestamp", "synthetic") if attributes else "synthetic",
            "confidence": attributes.get("confidence", 0.5) if attributes else 0.5,
            "data_source": attributes.get("data_source", "synthetic") if attributes else "synthetic",
            "provenance": attributes.get("provenance", {}) if attributes else {},
            "relationship_type": attributes.get("relationship_type", "ASSUMED") if attributes else "ASSUMED",
        }
        if attributes:
            payload.update(attributes)
        self.graph.add_edge(source, target, **payload)
        return payload

    def get_city(self, city_id: str) -> dict[str, Any] | None:
        return self._city_profiles.get(city_id)

    def compute_network_metrics(self) -> dict[str, Any]:
        node_count = self.graph.number_of_nodes()
        edge_count = self.graph.number_of_edges()
        avg_degree = (2 * edge_count / node_count) if node_count else 0.0
        density = nx.density(self.graph.to_undirected()) if node_count > 1 else 0.0
        return {
            "network_id": self.network_id,
            "network_name": self.network_name,
            "network_type": self.network_type,
            "layer": self.layer,
            "node_count": node_count,
            "edge_count": edge_count,
            "average_degree": round(avg_degree, 4),
            "density": round(density, 4),
            "status": "MODEL_DERIVED",
            "limitations": ["Network metrics are graph-derived and should not be interpreted as measured infrastructure capacity."],
        }

    def compute_centrality(self) -> dict[str, Any]:
        if self.graph.number_of_nodes() == 0:
            return {}
        undirected = self.graph.to_undirected()
        degree = nx.degree_centrality(undirected)
        weighted_degree = {node: degree for node, degree in dict(undirected.degree(weight="weight")).items()}
        betweenness = nx.betweenness_centrality(undirected, weight="weight")
        closeness = nx.closeness_centrality(undirected)
        pagerank = nx.pagerank(undirected, weight="weight")
        return {
            node: {
                "degree_centrality": round(float(degree.get(node, 0.0)), 4),
                "weighted_degree": round(float(weighted_degree.get(node, 0.0)), 4),
                "betweenness": round(float(betweenness.get(node, 0.0)), 4),
                "closeness": round(float(closeness.get(node, 0.0)), 4),
                "pagerank": round(float(pagerank.get(node, 0.0)), 4),
                "meaning": "Modeled network position; not a universal measure of urban importance.",
            }
            for node in undirected.nodes
        }

    def simulate_cascade(
        self,
        *,
        origin: str,
        shock_type: str,
        shock_magnitude: float,
        depth: int = 2,
        scenario: str = "SCENARIO_ESTIMATE",
    ) -> dict[str, Any]:
        if origin not in self.graph:
            return {"status": "NOT_AVAILABLE", "reason": f"Origin node {origin} is not in the network."}

        affected_nodes = {origin}
        affected_edges: list[tuple[str, str]] = []
        queue: deque[tuple[str, int]] = deque([(origin, 0)])
        seen: set[str] = {origin}
        while queue:
            node, current_depth = queue.popleft()
            if current_depth >= depth:
                continue
            for neighbor in self.graph.neighbors(node):
                if neighbor in seen:
                    continue
                seen.add(neighbor)
                affected_nodes.add(neighbor)
                affected_edges.append((node, neighbor))
                queue.append((neighbor, current_depth + 1))

        return {
            "cascade_id": f"cascade-{origin}-{depth}",
            "origin": origin,
            "shock_type": shock_type,
            "shock_magnitude": float(shock_magnitude),
            "depth": depth,
            "affected_nodes": sorted(affected_nodes),
            "affected_edges": [list(edge) for edge in affected_edges],
            "status": "SIMULATED",
            "scenario": scenario,
            "metrics": {
                "affected_nodes": len(affected_nodes),
                "affected_edges": len(affected_edges),
                "propagation_label": "MODEL_INDICATED_FRAGILITY" if shock_magnitude >= 0.5 else "POTENTIAL_TRANSITION",
            },
            "limitations": [
                "Cascades are simulation outputs and must not be interpreted as real-world disruptions without supporting evidence.",
            ],
        }

    def to_registry_record(self) -> dict[str, Any]:
        return {
            "network_id": self.network_id,
            "network_name": self.network_name,
            "network_type": self.network_type,
            "layer": self.layer,
            "node_count": self.graph.number_of_nodes(),
            "edge_count": self.graph.number_of_edges(),
            "status": "MODEL_DERIVED",
        }


class DependencyEngine:
    """Computes city dependency indicators for a network using the available modeled edges."""

    def __init__(self, network: UrbanNetwork) -> None:
        self.network = network

    def compute_dependency(self, city_id: str) -> dict[str, Any]:
        node_data = self.network.get_city(city_id)
        inbound_weight = sum(
            data.get("weight", 1.0) for _, _, data in self.network.graph.in_edges(city_id, data=True)
        )
        outbound_weight = sum(
            data.get("weight", 1.0) for _, _, data in self.network.graph.out_edges(city_id, data=True)
        )
        if node_data is None:
            return {"city_id": city_id, "status": "NOT_AVAILABLE", "dependencies": {}}

        values = {
            "inbound_commuting_dependency": round(float(inbound_weight), 4),
            "outbound_commuting_dependency": round(float(outbound_weight), 4),
            "transport_dependency": round(float((inbound_weight + outbound_weight) / 2.0), 4),
            "energy_dependency": round(float(min(inbound_weight, outbound_weight) / max(inbound_weight + outbound_weight, 1.0)), 4),
            "infrastructure_dependency": round(float((inbound_weight + outbound_weight) / max(len(node_data.get("urban_profile", {})) or 1, 1)), 4),
            "regional_service_dependency": round(float(inbound_weight + outbound_weight), 4),
            "status": "MODEL_DERIVED",
        }
        return {"city_id": city_id, "dependencies": values, "status": "MODEL_DERIVED"}

    def compute_all(self) -> dict[str, dict[str, Any]]:
        return {city_id: self.compute_dependency(city_id) for city_id in self.network.graph.nodes}
