from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def scenario_cache_key(payload: dict[str, Any]) -> str:
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":"), default=str)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def save_cache(directory: Path, payload: dict[str, Any]) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    key = scenario_cache_key(payload)
    path = directory / f"{key}.json"
    path.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return path
