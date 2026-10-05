from __future__ import annotations

from typing import Any


def validate_dag_definition(graph: dict[str, Any]) -> dict[str, Any]:
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    if not nodes:
        return {"status": "INVALID", "error": "DAG requires at least one node."}
    if not graph.get("treatment"):
        return {"status": "INVALID", "error": "missing treatment"}
    if not graph.get("outcome"):
        return {"status": "INVALID", "error": "missing outcome"}

    seen_edges = set()
    for edge in edges:
        pair = (edge.get("source"), edge.get("target"))
        if pair in seen_edges:
            return {"status": "INVALID", "error": "duplicate relationships"}
        seen_edges.add(pair)

    return {"status": "VALID", "nodes": len(nodes), "edges": len(edges), "assumptions": ["directed_acyclic_graph"]}
