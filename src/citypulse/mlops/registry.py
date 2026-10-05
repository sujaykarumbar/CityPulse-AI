from __future__ import annotations

from pathlib import Path
from uuid import uuid4

from citypulse.mlops.schemas import ModelRecord, RetrainingJob
from citypulse.mlops.store import JsonStore


class ModelRegistry:
    def __init__(self, root: Path = Path("artifacts/mlops")) -> None:
        self.store = JsonStore(root)

    def register(self, record: ModelRecord) -> ModelRecord:
        records = self.store.read("models")
        if any(item["model_name"] == record.model_name and item["model_version"] == record.model_version for item in records):
            raise ValueError("MODEL_VERSION_ALREADY_REGISTERED")
        records.append(record.model_dump(mode="json"))
        self.store.write("models", records)
        return record

    def list(self, model_name: str | None = None) -> list[ModelRecord]:
        records = [ModelRecord.model_validate(item) for item in self.store.read("models")]
        return [record for record in records if model_name is None or record.model_name == model_name]

    def get(self, model_name: str, version: str | None = None) -> ModelRecord | None:
        records = self.list(model_name)
        if version is not None:
            return next((record for record in records if record.model_version == version), None)
        return records[-1] if records else None

    def transition(self, model_name: str, version: str, target: str, actor: str) -> ModelRecord:
        allowed = {
            "EXPERIMENT": {"VALIDATING", "REJECTED", "FAILED"},
            "VALIDATING": {"VALIDATED", "REJECTED", "FAILED"},
            "VALIDATED": {"STAGING", "ARCHIVED"},
            "STAGING": {"PRODUCTION", "ARCHIVED", "REJECTED"},
            "PRODUCTION": {"ARCHIVED"},
        }
        records = self.list()
        target_record = next((record for record in records if record.model_name == model_name and record.model_version == version), None)
        if target_record is None:
            raise KeyError("MODEL_NOT_FOUND")
        if target not in allowed.get(target_record.lifecycle, set()):
            raise ValueError(f"INVALID_LIFECYCLE_TRANSITION:{target_record.lifecycle}->{target}")
        target_record.lifecycle = target  # type: ignore[assignment]
        target_record.updated_at = target_record.updated_at.now(target_record.updated_at.tzinfo)
        target_record.approval_status = "APPROVED" if target in {"STAGING", "PRODUCTION"} else target_record.approval_status
        self.store.write("models", [record.model_dump(mode="json") for record in records])
        self.store.write("audit", self.store.read("audit") + [{"action": "lifecycle_transition", "model": model_name, "version": version, "target": target, "actor": actor}])
        return target_record

    def create_retraining_job(self, model_name: str, trigger_type: str, reason: str) -> RetrainingJob:
        job = RetrainingJob(job_id=str(uuid4()), model_name=model_name, trigger_type=trigger_type, trigger_reason=reason)
        self.store.write("retraining", self.store.read("retraining") + [job.model_dump(mode="json")])
        return job

    def retraining_jobs(self, model_name: str | None = None) -> list[RetrainingJob]:
        jobs = [RetrainingJob.model_validate(item) for item in self.store.read("retraining")]
        return [job for job in jobs if model_name is None or job.model_name == model_name]
