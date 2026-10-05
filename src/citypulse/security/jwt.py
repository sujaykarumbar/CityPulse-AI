from __future__ import annotations

from typing import Any


def validate_jwt_claims(claims: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "valid": bool(claims),
        "issuer_valid": bool(claims and claims.get("iss")),
        "audience_valid": bool(claims and claims.get("aud")),
        "expired": bool(claims and claims.get("exp") and int(claims["exp"]) < 0),
        "claims": claims or {},
    }
