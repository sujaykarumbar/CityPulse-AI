from __future__ import annotations

from typing import Any, Dict, List


class ServiceDependencyGraph:
    """A minimal dependency graph for service nodes and their dependencies."""

    def __init__(self) -> None:
        self.nodes: Dict[str, Dict[str, Any]] = {}
        self.edges: List[Dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, attributes: Dict[str, Any] | None = None) -> None:
        self.nodes[node_id] = {"node_id": node_id, "node_type": node_type, "attributes": attributes or {}}

    def add_edge(self, source: str, target: str, relationship: str, evidence: str = "MODELED") -> None:
        self.edges.append({
            "source": source,
            "target": target,
            "relationship": relationship,
            "evidence": evidence,
            "status": "MODEL_DERIVED",
        })

    def summary(self) -> Dict[str, Any]:
        return {
            "status": "MODEL_DERIVED",
            "nodes": list(self.nodes.values()),
            "edges": self.edges,
            "method": "service_dependency_graph",
            "limitations": ["Dependency relationships are modeled and must not be treated as observed causal chains without source evidence."],
        }
