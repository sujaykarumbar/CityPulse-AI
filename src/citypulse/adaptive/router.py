from __future__ import annotations

from fastapi import APIRouter

from .assumptions import check_assumption
from .change_detection import detect_change
from .engine import AdaptiveUrbanIntelligenceEngine
from .strategy import StrategyLifecycle, compute_strategy_health, generate_alternatives

router = APIRouter(prefix="/adaptive", tags=["adaptive"])
engine = AdaptiveUrbanIntelligenceEngine()


@router.get("/state")
def adaptive_state() -> dict[str, str]:
    return {"status": "MODEL_DERIVED", "mode": "closed_loop_monitoring"}


@router.post("/assumptions/check")
def check_assumption_route(payload: dict) -> dict:
    result = check_assumption(
        assumption_id=payload.get("assumption_id", "assumption_unknown"),
        description=payload.get("description", "Assumption check"),
        variable=payload.get("variable", "unknown"),
        expected_range=tuple(payload.get("expected_range", (0.0, 0.0))),
        observed_value=float(payload.get("observed_value", 0.0)),
    )
    return result


@router.post("/changes")
def change_route(payload: dict) -> dict:
    return detect_change(
        metric_name=payload.get("metric_name", "performance"),
        previous_value=float(payload.get("previous_value", 0.0)),
        current_value=float(payload.get("current_value", 0.0)),
        threshold=float(payload.get("threshold", 0.1)),
    )


@router.post("/monitor")
def monitor_route(payload: dict) -> dict:
    return engine.monitor_strategy(
        city_id=payload.get("city_id", "unknown"),
        strategy_id=payload.get("strategy_id", "strategy_unknown"),
        observed_metrics=payload.get("observed_metrics", {}),
        expected_metrics=payload.get("expected_metrics", {}),
        assumptions=payload.get("assumptions"),
    )


@router.post("/alternatives")
def alternatives_route(payload: dict) -> dict:
    return {"alternatives": generate_alternatives(payload.get("strategy_id", "unknown"), payload.get("options", ["continue", "modify"]))}


@router.post("/health")
def health_route(payload: dict) -> dict:
    metrics = payload.get("metrics", {})
    return compute_strategy_health({str(key): float(value) for key, value in metrics.items()})


@router.post("/transition")
def transition_route(payload: dict) -> dict:
    lifecycle = StrategyLifecycle()
    return {"status": lifecycle.advance(payload.get("status", "ACTIVE"), payload.get("action", "monitor"))}
