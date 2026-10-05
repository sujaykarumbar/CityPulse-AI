from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.models.urban_foundation.schemas import (
    UrbanFoundationSearchRequest,
    UrbanFoundationSearchResponse,
    UrbanFoundationStatus,
    UrbanRepresentationRecord,
)
from citypulse.models.urban_foundation.service import UrbanFoundationService

router = APIRouter(prefix="/urban-foundation", tags=["urban-foundation"])
service = UrbanFoundationService()


@router.get("/status", response_model=UrbanFoundationStatus)
def status() -> UrbanFoundationStatus:
    return service.status()


@router.get("/modalities")
def modalities() -> list[str]:
    return service.modalities_available()


@router.get("/objectives")
def objectives() -> list[dict]:
    return service.objectives_available()


@router.get("/experiments")
def experiments() -> list[dict]:
    return [item.model_dump(mode="json") for item in service.list_experiments()]


@router.post("/index", response_model=dict)
def index_records(records: list[UrbanRepresentationRecord]) -> dict:
    indexed = service.index_embeddings(records)
    return {"status": "indexed", "count": len(indexed)}


@router.post("/search", response_model=UrbanFoundationSearchResponse)
def search(request: UrbanFoundationSearchRequest) -> UrbanFoundationSearchResponse:
    result = service.search(request.query, top_k=request.top_k)
    return UrbanFoundationSearchResponse.model_validate(result)
