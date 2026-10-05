from __future__ import annotations

from typing import Any


class KnowledgeGraph:
    def __init__(self) -> None:
        self.relationships: list[dict[str, Any]] = []

    def add_relationship(
        self,
        source_entity: str,
        target_entity: str,
        relationship: str,
        related_entity: str,
        *,
        provenance: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        edge = {
            "source_entity": source_entity,
            "target_entity": target_entity,
            "relationship": relationship,
            "related_entity": related_entity,
            "provenance": provenance or {"source": "NOT_AVAILABLE", "confidence": 0.0},
        }
        self.relationships.append(edge)
        return edge

    def list_relationships(self) -> list[dict[str, Any]]:
        return list(self.relationships)
