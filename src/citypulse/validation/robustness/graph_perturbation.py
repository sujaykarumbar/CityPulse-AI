from __future__ import annotations

import random
from typing import Any

import networkx as nx


def remove_edges(graph: nx.Graph, fraction: float, seed: int = 42) -> tuple[nx.Graph, dict[str, Any]]:
    if not 0 <= fraction < 1:
        raise ValueError("INVALID_EDGE_REMOVAL_FRACTION")
    perturbed = graph.copy()
    edges = list(perturbed.edges())
    count = int(len(edges) * fraction)
    removed = random.Random(seed).sample(edges, count) if count else []
    perturbed.remove_edges_from(removed)
    return perturbed, {"operation": "edge_removal", "fraction": fraction, "removed_edges": len(removed), "seed": seed, "data_origin": "SYNTHETIC_ROBUSTNESS_TEST"}
