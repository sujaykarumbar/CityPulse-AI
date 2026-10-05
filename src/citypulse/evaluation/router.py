from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.evaluation.benchmark import benchmark_run, build_synthetic_scenario
from citypulse.evaluation.schemas import BenchmarkRequest, SyntheticScenarioRequest
from citypulse.evaluation.service import EvaluationService

router = APIRouter(prefix="/evaluation", tags=["evaluation"])
service = EvaluationService()


@router.get("/status")
def status() -> dict:
    return service.status()


@router.get("/runs")
def list_runs() -> list[dict]:
    return service.history()


@router.post("/benchmark")
def benchmark(request: BenchmarkRequest) -> dict:
    try:
        result = service.benchmark(
            request.observed,
            request.predicted,
            task=request.task,
            domain=request.domain,
            dataset_version=request.dataset_version,
            model_version=request.model_version,
            result_type=request.result_type,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"code": str(exc)}) from exc
    return result


@router.post("/synthetic")
def synthetic(request: SyntheticScenarioRequest) -> dict:
    try:
        return service.synthetic(request.domain, {**request.config, "sample_count": request.sample_count, "seed": request.seed})
    except ValueError as exc:
        raise HTTPException(status_code=422, detail={"code": str(exc)}) from exc


@router.get("/ablation")
def ablation() -> dict:
    return {
        "status": "NOT_RUN",
        "benchmark_status": "NOT_RUN",
        "description": "Ablation studies are planned but no executed ablation run exists yet.",
        "reproducibility": "NOT_ESTABLISHED",
    }


@router.get("/robustness")
def robustness() -> dict:
    return {
        "status": "NOT_RUN",
        "benchmark_status": "NOT_RUN",
        "description": "Robustness evaluation is scaffolded but no measured stress-test results are available.",
        "reproducibility": "NOT_ESTABLISHED",
    }


@router.get("/synthetic/demo")
def synthetic_demo() -> dict:
    return build_synthetic_scenario("traffic", {"sample_count": 24, "seed": 7})


@router.get("/benchmark/demo")
def benchmark_demo() -> dict:
    return benchmark_run([], [])
