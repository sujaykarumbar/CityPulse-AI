from __future__ import annotations

from typing import Any


class NetworkRegistry:
    """In-memory registry for urban network definitions."""

    def __init__(self) -> None:
        self._networks: dict[str, dict[str, Any]] = {}

    def register_network(
        self,
        *,
        network_id: str,
        network_name: str,
        network_type: str,
        layer: str,
        spatial_scope: str = "regional",
        temporal_scope: str = "current",
        source: str = "synthetic",
        methodology: str = "MODELED",
        version: str = "v1",
        tags: list[str] | None = None,
    ) -> dict[str, Any]:
        record = {
            "network_id": network_id,
            "network_name": network_name,
            "network_type": network_type,
            "layer": layer,
            "spatial_scope": spatial_scope,
            "temporal_scope": temporal_scope,
            "source": source,
            "methodology": methodology,
            "version": version,
            "tags": tags or [],
            "created_at": "synthetic",
        }
        self._networks[network_id] = record
        return record

    def get_network(self, network_id: str) -> dict[str, Any] | None:
        return self._networks.get(network_id)

    def list_networks(self) -> list[dict[str, Any]]:
        return list(self._networks.values())

    def remove_network(self, network_id: str) -> None:
        self._networks.pop(network_id, None)


def build_registry() -> NetworkRegistry:
    return NetworkRegistry()
