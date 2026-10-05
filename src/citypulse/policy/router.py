from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.policy.cost import policy_cost_analysis
from citypulse.policy.equity import equity_analysis
from citypulse.policy.experiments import PolicyExperimentEngine
from citypulse.policy.registry import PolicyRegistry
from citypulse.policy.robustness import robustness_report
from citypulse.policy.transferability import assess_transferability

router = APIRouter(prefix="/policy", tags=["policy"])
registry = PolicyRegistry()
engine = PolicyExperimentEngine()


@router.get("/policies")
def list_policies() -> dict[str, list[dict]]:
    return {"policies": registry.list()}


@router.post("/policies")
def create_policy(payload: dict) -> dict:
    policy = registry.register(
        policy_id=payload.get("policy_id", "policy_unknown"),
        name=payload.get("name", "Unknown Policy"),
        category=payload.get("category", "general"),
        version=payload.get("version", "1.0"),
        city_scope=payload.get("city_scope", "global"),
        status=payload.get("status", "experimental"),
        provenance=payload.get("provenance", {}),
    )
    return policy


@router.get("/policies/{policy_id}")
def get_policy(policy_id: str) -> dict:
    policy = registry.get(policy_id)
    if policy is None:
        raise HTTPException(status_code=404, detail={"code": "POLICY_NOT_FOUND"})
    return policy


@router.post("/policies/compare")
def compare_policies(payload: dict) -> dict:
    left = payload.get("left_policy", "unknown")
    right = payload.get("right_policy", "unknown")
    return {"status": "COMPARISON_READY", "left_policy": left, "right_policy": right, "differences": []}


@router.post("/experiments")
def create_experiment(payload: dict) -> dict:
    return engine.evaluate(
        policy_id=payload.get("policy_id", "unknown"),
        city_id=payload.get("city_id", "unknown"),
        baseline=payload.get("baseline", {}),
        simulation=payload.get("simulation", {}),
        evidence=payload.get("evidence", {}),
        objectives=payload.get("objectives", []),
    )


@router.post("/cost")
def cost_analysis(payload: dict) -> dict:
    return policy_cost_analysis(payload.get("costs"))


@router.post("/equity")
def equity_report(payload: dict) -> dict:
    return equity_analysis(payload.get("metrics"))


@router.post("/transferability")
def transferability(payload: dict) -> dict:
    return assess_transferability(
        source_city=payload.get("source_city", "unknown"),
        target_city=payload.get("target_city", "unknown"),
        overlap=payload.get("overlap"),
    )


@router.post("/robustness")
def robustness(payload: dict) -> dict:
    return robustness_report(policy_id=payload.get("policy_id", "unknown"), scenarios=payload.get("scenarios"))


@router.get("/reports")
def reports() -> dict[str, list[str]]:
    return {"reports": ["policy_experiment_report.md", "policy_evidence_report.md", "equity_report.md", "robustness_report.md"]}
