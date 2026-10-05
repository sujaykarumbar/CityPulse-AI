from __future__ import annotations

from typing import Any


class DAG:
    def __init__(self) -> None:
        self.nodes: dict[str, str] = {}
        self.edges: list[tuple[str, str]] = []

    def add_node(self, name: str, node_type: str = "variable") -> None:
        self.nodes[name] = node_type

    def add_edge(self, source: str, target: str) -> None:
        if source == target:
            raise ValueError("Self-loops are not allowed in a DAG.")
        pair = (source, target)
        if pair not in self.edges:
            self.edges.append(pair)

    def _has_cycle(self) -> bool:
        graph: dict[str, list[str]] = {node: [] for node in self.nodes}
        for source, target in self.edges:
            if source not in graph:
                graph[source] = []
            if target not in graph:
                graph[target] = []
            graph[source].append(target)

        visited: set[str] = set()
        stack: set[str] = set()

        def dfs(node: str) -> bool:
            visited.add(node)
            stack.add(node)
            for neighbor in graph.get(node, []):
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in stack:
                    return True
            stack.remove(node)
            return False

        for node in graph:
            if node not in visited and dfs(node):
                return True
        return False

    def validate(self, *, treatment: str | None = None, outcome: str | None = None) -> dict[str, Any]:
        if treatment is not None and treatment not in self.nodes:
            raise ValueError("missing treatment")
        if outcome is not None and outcome not in self.nodes:
            raise ValueError("missing outcome")
        if self._has_cycle():
            raise ValueError("cycle detected")

        duplicate_edges = set()
        for source, target in self.edges:
            pair = (source, target)
            if pair in duplicate_edges:
                raise ValueError("duplicate relationships")
            duplicate_edges.add(pair)

        return {
            "status": "VALID",
            "nodes": sorted(self.nodes),
            "edges": [dict(source=s, target=t) for s, t in self.edges],
            "assumptions": ["directed_acyclic_graph"],
        }
