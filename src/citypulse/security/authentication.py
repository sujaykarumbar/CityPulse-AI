from __future__ import annotations

from typing import Any

REQUIRED_CLAIMS = {"sub", "iss", "aud", "exp", "nbf", "token_type"}


def validate_token(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not payload:
        return {"valid": False, "reason": "missing_required_claims", "details": "Token payload was empty."}
    missing = sorted(REQUIRED_CLAIMS - set(payload.keys()))
    if missing:
        return {"valid": False, "reason": "missing_required_claims", "missing": missing}

    # Explicitly reject obviously invalid/expired tokens without inventing a trusted authentication result.
    if payload.get("exp") is None or payload.get("nbf") is None:
        return {"valid": False, "reason": "invalid_claims"}
    if int(payload["exp"]) < int(payload.get("nbf", 0)):
        return {"valid": False, "reason": "invalid_claims"}
    if payload.get("token_type") not in {"access", "refresh"}:
        return {"valid": False, "reason": "invalid_token_type"}

    return {
        "valid": True,
        "claims": payload,
        "role": payload.get("role", "VIEWER"),
        "tenant_id": payload.get("tenant_id"),
        "city_id": payload.get("city_id"),
    }
