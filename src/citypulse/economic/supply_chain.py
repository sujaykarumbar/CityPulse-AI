from __future__ import annotations

from collections import defaultdict
from typing import Any


class SupplyChainGraph:
    """Minimal supply-chain graph for regional dependency analysis."""

    def __init__(self) -> None:
        self.nodes: dict[str, dict[str, Any]] = {}
        self.edges: list[dict[str, Any]] = []

    def add_node(self, node_id: str, node_type: str, metadata: dict[str, Any] | None = None) -> dict[str, Any]:
        record = {"node_id": node_id, "node_type": node_type, **(metadata or {})}
        self.nodes[node_id] = record
        return record

    def add_edge(
        self,
        source: str,
        target: str,
        relationship: str,
        *,
        weight: float = 1.0,
        evidence_type: str = "MODELED",
    ) -> dict[str, Any]:
        record = {
            "source": source,
            "target": target,
            "relationship": relationship,
            "weight": float(weight),
            "evidence_type": evidence_type,
            "status": "MODEL_DERIVED",
        }
        self.edges.append(record)
        return record

    def dependency_summary(self) -> dict[str, Any]:
        by_source = defaultdict(float)
        for edge in self.edges:
            by_source[edge["source"]] += float(edge["weight"])
        return {
            "status": "MODEL_DERIVED",
            "source_dependencies": dict(sorted(by_source.items())),
            "edge_count": len(self.edges),
            "node_count": len(self.nodes),
        }
