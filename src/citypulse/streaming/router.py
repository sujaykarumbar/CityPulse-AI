from __future__ import annotations

from fastapi import APIRouter

from citypulse.streaming.schemas import ReplayRequest, StreamStatus
from citypulse.streaming.service import StreamingService

router = APIRouter(prefix="/streaming", tags=["streaming"])
service = StreamingService()


@router.get("/status", response_model=StreamStatus)
def status() -> StreamStatus:
    return service.status()


@router.get("/topics")
def topics() -> list[str]:
    return service.status().topics


@router.get("/health")
def health() -> dict[str, str | bool]:
    result = service.status()
    return {"status": result.status, "connected": result.connected, "broker": result.broker}


@router.get("/data-quality")
def data_quality() -> dict[str, str]:
    return {"status": "NO DATA AVAILABLE", "accepted": "NOT MEASURED", "rejected": "NOT MEASURED"}


@router.get("/dead-letter")
def dead_letter() -> list[dict]:
    return [item.model_dump(mode="json") for item in service.broker.dead_letters()]


@router.post("/replay")
def replay(request: ReplayRequest) -> dict:
    return service.replay(request)


@router.get("/state")
def current_state() -> dict:
    return service.current_state()
