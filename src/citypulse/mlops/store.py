from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class JsonStore:
    """Small local persistence adapter; replaceable by PostgreSQL/MLflow later."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.root.mkdir(parents=True, exist_ok=True)

    def read(self, name: str) -> list[dict[str, Any]]:
        path = self.root / f"{name}.json"
        if not path.exists():
            return []
        return json.loads(path.read_text(encoding="utf-8"))

    def write(self, name: str, values: list[dict[str, Any]]) -> None:
        path = self.root / f"{name}.json"
        path.write_text(json.dumps(values, indent=2, default=str), encoding="utf-8")
