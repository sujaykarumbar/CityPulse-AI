from __future__ import annotations

from fastapi import APIRouter

from citypulse.governance.audit import emit_audit_event
from citypulse.security.authentication import validate_token
from citypulse.security.authorization import Role, authorize

router = APIRouter(prefix="/security", tags=["security"])


@router.get("/health")
def security_health() -> dict:
    return {"status": "SECURITY_LAYER_ACTIVE", "authentication": "JWT_VALIDATION_ENABLED", "authorization": "RBAC_ENABLED"}


@router.post("/validate-token")
def validate_token_route(payload: dict) -> dict:
    return validate_token(payload)


@router.get("/policies")
def policies() -> dict:
    return {
        "roles": [role.value for role in Role],
        "authorization_model": "RBAC",
        "enforcement": "SERVER_SIDE_ONLY",
    }


@router.post("/audit")
def audit_event(payload: dict) -> dict:
    return emit_audit_event(
        actor_id=str(payload.get("actor_id", "unknown")),
        operation=str(payload.get("operation", "unknown")),
        resource_type=str(payload.get("resource_type", "unknown")),
        action=str(payload.get("action", "read")),
        result=str(payload.get("result", "accepted")),
        tenant_id=payload.get("tenant_id"),
    )


@router.get("/authorize")
def authorize_route(role: str, action: str) -> dict:
    return {"authorized": authorize(role, action), "role": role, "action": action}
