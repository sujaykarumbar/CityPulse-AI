from __future__ import annotations

from fastapi import APIRouter

from citypulse.transfer.learning import transfer_experiment

router = APIRouter(prefix="/global", tags=["transfer-learning"])


@router.post("/transfer")
def transfer_route(payload: dict) -> dict:
    return transfer_experiment(
        payload.get("source_city", "unknown"),
        payload.get("target_city", "unknown"),
        payload.get("local_results", {}),
        payload.get("transfer_results", {}),
    )
