from __future__ import annotations


def graph_to_ascii(graph: dict[str, object]) -> str:
    edges = graph.get("edges", [])
    if not edges:
        return "No edges defined."
    lines = []
    for edge in edges:
        lines.append(f"{edge.get('source')} -> {edge.get('target')}")
    return "\n".join(lines)
