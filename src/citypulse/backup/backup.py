from __future__ import annotations

from datetime import datetime, timezone
from uuid import uuid4


def create_backup(source: str, version: str, *, metadata: dict | None = None) -> dict[str, str | dict | None]:
    return {
        "backup_id": str(uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "source": source,
        "version": version,
        "status": "BACKUP_CREATED",
        "checksum": "NOT_MEASURED",
        "metadata": metadata or {},
    }


def verify_backup(backup_id: str, *, restore_target: str | None = None) -> dict[str, str]:
    return {
        "backup_id": backup_id,
        "verification_status": "NOT_TESTED",
        "restore_target": restore_target or "NOT_CONFIGURED",
        "result": "BACKUP_NOT_VERIFIED",
    }
