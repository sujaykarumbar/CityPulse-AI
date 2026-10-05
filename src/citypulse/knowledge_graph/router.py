from __future__ import annotations

from fastapi import APIRouter

from citypulse.knowledge_graph.graph import KnowledgeGraph

router = APIRouter(prefix="/global", tags=["knowledge-graph"])
knowledge_graph = KnowledgeGraph()


@router.get("/knowledge-graph")
def list_knowledge_graph() -> dict:
    return {"status": "GRAPH_AVAILABLE", "relationships": knowledge_graph.list_relationships()}


@router.post("/knowledge-graph")
def add_relationship(payload: dict) -> dict:
    return knowledge_graph.add_relationship(
        payload.get("source_entity", "unknown"),
        payload.get("target_entity", "unknown"),
        payload.get("relationship", "RELATED_TO"),
        payload.get("related_entity", "unknown"),
        provenance=payload.get("provenance", {}),
    )
