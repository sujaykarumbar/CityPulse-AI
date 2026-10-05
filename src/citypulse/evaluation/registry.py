from __future__ import annotations

from pathlib import Path
from typing import Any

from citypulse.mlops.store import JsonStore


class EvaluationRegistry:
    def __init__(self, root: Path = Path("artifacts/evaluation")) -> None:
        self.store = JsonStore(root)

    def register(self, record: dict[str, Any]) -> dict[str, Any]:
        records = self.store.read("experiments")
        records.append(record)
        self.store.write("experiments", records)
        return record

    def list(self) -> list[dict[str, Any]]:
        return self.store.read("experiments")

    def get(self, experiment_id: str) -> dict[str, Any] | None:
        for item in self.list():
            if item.get("experiment_id") == experiment_id:
                return item
        return None
