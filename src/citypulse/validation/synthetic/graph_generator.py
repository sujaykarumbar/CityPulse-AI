from __future__ import annotations

import networkx as nx


def generate_synthetic_graph(node_count: int, edge_probability: float = 0.1, seed: int = 42) -> tuple[nx.Graph, dict[str, object]]:
    if not 1 <= node_count <= 5000 or not 0 <= edge_probability <= 1:
        raise ValueError("RESOURCE_LIMIT_EXCEEDED_OR_INVALID_GRAPH_CONFIG")
    graph = nx.gnp_random_graph(node_count, edge_probability, seed=seed)
    return graph, {"data_origin": "SYNTHETIC", "generator_version": "graph-synth-0.1.0", "seed": seed, "node_count": graph.number_of_nodes(), "edge_count": graph.number_of_edges(), "generator": "Erdos-Renyi test graph; not a city road graph"}
