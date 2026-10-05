from __future__ import annotations

from citypulse.security.roles import Role

PERMISSIONS = {
    Role.VIEWER: {"view:dashboard", "view:analytics"},
    Role.ANALYST: {"view:dashboard", "view:analytics", "run:analytics", "run:scenario"},
    Role.RESEARCHER: {"view:dashboard", "view:analytics", "run:analytics", "run:scenario", "run:research", "view:research"},
    Role.OPERATOR: {"view:dashboard", "view:health", "run:operations", "ack:alert"},
    Role.ADMIN: {"view:dashboard", "view:analytics", "run:analytics", "manage:security", "manage:users", "manage:system"},
    Role.SYSTEM: {"view:dashboard", "manage:system", "run:internal"},
}


def authorize(role: Role | str, action: str) -> bool:
    resolved = Role.from_value(role if isinstance(role, str) else role.value)
    return action in PERMISSIONS.get(resolved, set())
