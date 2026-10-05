from __future__ import annotations

from typing import Any

import networkx as nx
import pandas as pd


def build_mobility_graph(
    od: pd.DataFrame,
    origin_column: str = "origin_id",
    destination_column: str = "destination_id",
    weight_column: str = "trip_count",
) -> nx.DiGraph:
    graph = nx.DiGraph()
    if od.empty:
        return graph
    for row in od.itertuples(index=False):
        origin = getattr(row, origin_column)
        destination = getattr(row, destination_column)
        weight = float(getattr(row, weight_column))
        graph.add_edge(origin, destination, weight=weight)
    return graph


def graph_statistics(graph: nx.DiGraph) -> dict[str, Any]:
    weak_components = list(nx.weakly_connected_components(graph))
    return {
        "nodes": graph.number_of_nodes(),
        "edges": graph.number_of_edges(),
        "weakly_connected_components": len(weak_components),
        "largest_component": max((len(component) for component in weak_components), default=0),
        "isolated_nodes": sum(1 for node in graph if graph.degree(node) == 0),
        "average_degree": sum(dict(graph.degree()).values()) / graph.number_of_nodes()
        if graph.number_of_nodes()
        else 0.0,
    }


def graph_metrics(graph: nx.DiGraph) -> pd.DataFrame:
    if graph.number_of_nodes() == 0:
        return pd.DataFrame(columns=["zone_id", "in_degree", "out_degree", "weighted_degree", "pagerank"])
    pagerank = nx.pagerank(graph, weight="weight")
    rows = []
    for node in graph.nodes:
        rows.append(
            {
                "zone_id": node,
                "in_degree": graph.in_degree(node),
                "out_degree": graph.out_degree(node),
                "weighted_degree": graph.degree(node, weight="weight"),
                "pagerank": pagerank[node],
            }
        )
    return pd.DataFrame(rows)
