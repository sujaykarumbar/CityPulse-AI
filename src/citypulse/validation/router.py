from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.validation.schemas import BacktestRequest, RobustnessRequest, SyntheticCompareRequest, SyntheticRequest, ValidationResult
from citypulse.validation.service import ValidationService

router = APIRouter(prefix="/validation", tags=["validation"])
service = ValidationService()


@router.get("/status")
def status() -> dict:
    return service.status()


@router.get("/runs", response_model=list[ValidationResult])
def list_runs() -> list[ValidationResult]:
    return service.registry.list()


@router.get("/{validation_id}", response_model=ValidationResult)
def get_run(validation_id: str) -> ValidationResult:
    result = service.registry.get(validation_id)
    if result is None:
        raise HTTPException(status_code=404, detail={"code": "VALIDATION_NOT_FOUND"})
    return result


@router.post("/backtest", response_model=ValidationResult)
def backtest(request: BacktestRequest) -> ValidationResult:
    return service.compare(request.task, request.observed, request.predicted, request.dataset_version, request.model_version, request.result_type)


@router.post("/simulation")
def simulation_validation(request: BacktestRequest) -> dict:
    return service.simulation_compare(request.observed, request.predicted)


@router.post("/synthetic")
def synthetic(request: SyntheticRequest) -> dict:
    try:
        rows, quality = service.synthetic(request.domain, {**request.config, "sample_count": request.sample_count, "seed": request.seed})
    except ValueError as exc:
        code = str(exc)
        raise HTTPException(status_code=422, detail={"code": code}) from exc
    return {"data_origin": "SYNTHETIC", "rows": rows, "quality": quality}


@router.post("/synthetic/compare")
def compare_synthetic(request: SyntheticCompareRequest) -> dict:
    return service.compare_synthetic(request.real_values, request.synthetic_values)


@router.post("/robustness/missing-data")
def robustness_missing_data(request: RobustnessRequest) -> dict:
    return service.missingness_experiment(request.values, request.rate, request.seed, request.mode)


@router.get("/scorecard")
def scorecard() -> dict:
    return {
        "forecasting_validation": "VALIDATION_NOT_AVAILABLE",
        "simulation_validation": "VALIDATION_NOT_AVAILABLE",
        "spatial_generalization": "NOT_MEASURED",
        "temporal_generalization": "NOT_MEASURED",
        "robustness": "FRAMEWORK_AVAILABLE_RESULTS_NOT_MEASURED",
        "uncertainty_calibration": "NOT_MEASURED",
        "synthetic_data_utility": "NOT_MEASURED",
        "data_quality": "SEE_DATA_QUALITY_REPORTS",
        "reproducibility": "LINEAGE_REQUIRED_PER_RUN",
        "computational_efficiency": "NOT_MEASURED",
    }
