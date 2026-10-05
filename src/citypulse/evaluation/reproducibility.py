from __future__ import annotations

from typing import Any


def build_reproducibility_metadata(config: dict[str, Any] | None = None) -> dict[str, Any]:
    metadata = {
        "status": "LINEAGE_REQUIRED_PER_RUN",
        "data_origin": "NOT_AVAILABLE",
        "reproducibility": "NOT_ESTABLISHED",
        "seed": (config or {}).get("seed"),
    }
    if config:
        metadata["config_hash"] = hash(repr(sorted(config.items())))
    return metadata
