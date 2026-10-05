from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def emit_audit_event(*, actor_id: str, operation: str, resource_type: str, action: str, result: str, tenant_id: str | None = None) -> dict[str, str | None]:
    return {
        "audit_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "actor_id": actor_id,
        "tenant_id": tenant_id,
        "operation": operation,
        "resource_type": resource_type,
        "action": action,
        "result": result,
    }
