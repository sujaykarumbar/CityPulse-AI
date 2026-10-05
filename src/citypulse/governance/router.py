from __future__ import annotations

from fastapi import APIRouter

from citypulse.governance.classification import DataClassification, classify_dataset
from citypulse.governance.retention import RetentionPolicy, evaluate_retention

router = APIRouter(prefix="/governance", tags=["governance"])


@router.get("/classification")
def classification() -> dict:
    return {"status": "CLASSIFICATION_FRAMEWORK_ACTIVE", "values": [item.value for item in DataClassification]}


@router.post("/datasets")
def catalog_dataset(payload: dict) -> dict:
    classification = classify_dataset(payload)
    return {"dataset_id": payload.get("dataset_id", "unknown"), "classification": classification.value, "status": "CATALOGED"}


@router.get("/retention")
def retention() -> dict:
    policy = RetentionPolicy(name="raw-events", classification=DataClassification.RESTRICTED, days=90)
    return evaluate_retention(policy, 30)
