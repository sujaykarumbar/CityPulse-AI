from __future__ import annotations

from typing import Any


class PolicyRegistry:
    def __init__(self) -> None:
        self._policies: dict[str, dict[str, Any]] = {}

    def register(
        self,
        *,
        policy_id: str,
        name: str,
        category: str,
        version: str = "1.0",
        city_scope: str = "global",
        status: str = "experimental",
        provenance: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        policy = {
            "policy_id": policy_id,
            "name": name,
            "category": category,
            "version": version,
            "city_scope": city_scope,
            "status": status,
            "provenance": provenance or {"source": "NOT_AVAILABLE"},
        }
        self._policies[policy_id] = policy
        return policy

    def get(self, policy_id: str) -> dict[str, Any] | None:
        return self._policies.get(policy_id)

    def list(self) -> list[dict[str, Any]]:
        return list(self._policies.values())
