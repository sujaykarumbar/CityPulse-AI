from __future__ import annotations

from pathlib import Path

from citypulse.mlops.store import JsonStore
from citypulse.validation.schemas import ValidationResult


class ValidationRegistry:
    def __init__(self, root: Path = Path("artifacts/validation")) -> None:
        self.store = JsonStore(root)

    def register(self, result: ValidationResult) -> ValidationResult:
        records = self.store.read("validation_runs")
        records.append(result.model_dump(mode="json"))
        self.store.write("validation_runs", records)
        return result

    def list(self) -> list[ValidationResult]:
        return [ValidationResult.model_validate(item) for item in self.store.read("validation_runs")]

    def get(self, validation_id: str) -> ValidationResult | None:
        return next((item for item in self.list() if item.validation_id == validation_id), None)
