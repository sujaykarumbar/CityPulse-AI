from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException

from citypulse.mlops.registry import ModelRegistry
from citypulse.mlops.schemas import ModelRecord, PromotionRequest, RetrainingJob, RollbackRequest, ValidationResult
from citypulse.mlops.validation import validate_model

router = APIRouter(prefix="/mlops", tags=["mlops"])
registry = ModelRegistry(Path("artifacts/mlops"))


@router.get("/models", response_model=list[ModelRecord])
def list_models() -> list[ModelRecord]:
    return registry.list()


@router.get("/models/{model_name}", response_model=ModelRecord)
def get_model(model_name: str) -> ModelRecord:
    record = registry.get(model_name)
    if record is None:
        raise HTTPException(status_code=404, detail={"code": "MODEL_NOT_FOUND"})
    return record


@router.post("/models/{model_name}/validate", response_model=ValidationResult)
def validate_registered_model(model_name: str) -> ValidationResult:
    record = registry.get(model_name)
    if record is None:
        raise HTTPException(status_code=404, detail={"code": "MODEL_NOT_FOUND"})
    return validate_model(record)


@router.post("/models/{model_name}/promote", response_model=ModelRecord)
def promote_model(model_name: str, request: PromotionRequest) -> ModelRecord:
    record = registry.get(model_name)
    if record is None:
        raise HTTPException(status_code=404, detail={"code": "MODEL_NOT_FOUND"})
    if record.validation_status != "PASS":
        raise HTTPException(status_code=409, detail={"code": "MODEL_NOT_VALIDATED"})
    return registry.transition(model_name, record.model_version, "STAGING", request.actor)


@router.post("/models/{model_name}/retrain", response_model=RetrainingJob)
def request_retraining(model_name: str, request: PromotionRequest) -> RetrainingJob:
    return registry.create_retraining_job(model_name, "manual", request.reason)


@router.get("/retraining", response_model=list[RetrainingJob])
def list_retraining() -> list[RetrainingJob]:
    return registry.retraining_jobs()
