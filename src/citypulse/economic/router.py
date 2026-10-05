from __future__ import annotations

from fastapi import APIRouter

from citypulse.economic.profiles import build_city_economic_profile
from citypulse.economic.resilience import EconomicResilienceEngine
from citypulse.economic.shocks import simulate_economic_shock
from citypulse.economic.specialization import analyze_specialization
from citypulse.economic.supply_chain import SupplyChainGraph

router = APIRouter(prefix="/economy", tags=["economy"])


@router.get("/cities/{city_id}")
def get_city_profile(city_id: str) -> dict:
    return build_city_economic_profile(
        city_id,
        {
            "employment": 1200.0,
            "industry_mix": {"manufacturing": 0.5, "retail": 0.3},
            "economic_diversity": 0.7,
        },
    )


@router.get("/cities/{city_id}/specialization")
def city_specialization(city_id: str) -> dict:
    return analyze_specialization(
        city_id=city_id,
        sector="manufacturing",
        share=0.6,
        reference_share=0.35,
        period="2025-Q1",
    )


@router.get("/supply-chain")
def supply_chain_summary() -> dict:
    graph = SupplyChainGraph()
    graph.add_node("city-a", "city")
    graph.add_node("factory-a", "factory")
    graph.add_edge("city-a", "factory-a", "SUPPLIES", weight=2.0)
    return graph.dependency_summary()


@router.post("/shocks/simulate")
def simulate_shock(payload: dict) -> dict:
    return simulate_economic_shock(
        city_id=str(payload.get("city_id", "unknown")),
        shock_type=str(payload.get("shock_type", "freight_disruption")),
        magnitude=float(payload.get("magnitude", 0.5)),
        sectors=payload.get("sectors", []),
        duration_days=int(payload.get("duration_days", 7)),
    )


@router.get("/resilience/{city_id}")
def city_resilience(city_id: str) -> dict:
    engine = EconomicResilienceEngine()
    return engine.evaluate(city_id=city_id, profile={"diversification": 0.7, "supplier_diversity": 0.8, "transport_redundancy": 0.6, "recovery_capacity": 0.5})
