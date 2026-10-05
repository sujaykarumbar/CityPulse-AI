from __future__ import annotations

from fastapi import APIRouter

from .engine import UrbanEvolutionEngine, generate_future_scenarios
from .pathways import AdaptivePathwayEngine, evaluate_trigger
from .robustness import regret_analysis, robustness_analysis

router = APIRouter(prefix="/foresight", tags=["foresight"])


@router.get("/scenarios")
def list_scenarios() -> dict[str, object]:
    return {
        "status": "SCENARIO_ESTIMATE",
        "scenarios": generate_future_scenarios(city_id="demo-city", horizon_years=10, seed=1, scenario_count=3),
    }


@router.post("/scenarios")
def create_scenario(payload: dict) -> dict[str, object]:
    city_id = payload.get("city_id", "demo-city")
    horizon_years = int(payload.get("horizon_years", 10))
    seed = int(payload.get("seed", 1))
    assumptions = payload.get("policy_assumptions", {})
    scenarios = generate_future_scenarios(
        city_id=city_id,
        horizon_years=horizon_years,
        seed=seed,
        policy_assumptions=assumptions,
        scenario_count=max(1, int(payload.get("scenario_count", 3))),
    )
    return {"status": "SCENARIO_ESTIMATE", "scenarios": [scenario.model_dump() for scenario in scenarios]}


@router.post("/evolution/run")
def run_evolution(payload: dict) -> dict[str, object]:
    baseline = payload.get("baseline", {"population": 100_000, "mobility": 1.0, "energy": 1.0})
    policy = payload.get("policy", {})
    horizon = int(payload.get("horizon_years", 5))
    result = UrbanEvolutionEngine(seed=int(payload.get("seed", 0))).simulate_future(
        baseline=baseline,
        policy=policy,
        horizon_years=horizon,
    )
    return result


@router.post("/pathways")
def create_pathway(payload: dict) -> dict[str, object]:
    engine = AdaptivePathwayEngine()
    return engine.build_pathway(
        initial_strategy=payload.get("initial_strategy", "Transit investment"),
        monitors=payload.get("monitors", ["transit_ridership", "traffic_volume"]),
        thresholds={
            metric: float(value)
            for metric, value in payload.get("thresholds", {"transit_ridership": 80, "traffic_volume": 120}).items()
        },
        alternative_strategy=payload.get("alternative_strategy", "Demand management"),
    )


@router.post("/trigger")
def evaluate_metric_trigger(payload: dict) -> dict[str, object]:
    return evaluate_trigger(
        metric_name=payload.get("metric_name", "transit_ridership"),
        current_value=float(payload.get("current_value", 0.0)),
        threshold=float(payload.get("threshold", 0.0)),
        direction=payload.get("direction", "above"),
    )


@router.post("/robustness")
def robustness(payload: dict) -> dict[str, object]:
    scores = {str(key): float(value) for key, value in payload.get("strategy_scores", {}).items()}
    return robustness_analysis(strategy_scores=scores)


@router.post("/regret")
def regret(payload: dict) -> dict[str, object]:
    scores = {str(key): float(value) for key, value in payload.get("strategy_scores", {}).items()}
    return regret_analysis(strategy_scores=scores, best_score=float(payload.get("best_score", max(scores.values(), default=0.0))))
