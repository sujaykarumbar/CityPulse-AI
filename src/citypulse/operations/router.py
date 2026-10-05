from __future__ import annotations

from fastapi import APIRouter

from citypulse.backup.backup import create_backup, verify_backup
from citypulse.operations.health import aggregate_health
from citypulse.observability.slis import build_error_budget
from citypulse.recovery.disaster_recovery import compute_recovery_plan

router = APIRouter(prefix="/operations", tags=["operations"])


@router.get("/health")
def service_health() -> dict:
    return aggregate_health({"api": "HEALTHY", "database": "UNKNOWN", "redis": "DEGRADED"})


@router.get("/slo")
def slo() -> dict:
    return build_error_budget(0.99, 0.002)


@router.post("/backup")
def backup_route(payload: dict) -> dict:
    return create_backup(payload.get("source", "unknown"), payload.get("version", "0.0.0"), metadata=payload.get("metadata", {}))


@router.get("/backup/verify")
def verify_backup_route() -> dict:
    return verify_backup("demo-backup", restore_target="staging")


@router.get("/recovery")
def recovery() -> dict:
    return compute_recovery_plan(6, 12)
