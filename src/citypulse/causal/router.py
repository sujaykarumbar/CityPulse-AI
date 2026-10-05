from __future__ import annotations

from fastapi import APIRouter

from citypulse.causal.dag.adjustment import identify_adjustment_set
from citypulse.causal.dag.graph import DAG
from citypulse.causal.designs.difference_in_differences import difference_in_differences
from citypulse.causal.questions import build_causal_question

router = APIRouter(prefix="/causal", tags=["causal"])


@router.get("/questions")
def list_questions() -> dict[str, list[str]]:
    return {"questions": []}


@router.post("/questions")
def create_question(payload: dict) -> dict:
    return build_causal_question(
        question_id=payload.get("question_id", "question-unknown"),
        city_id=payload.get("city_id", "unknown"),
        treatment=payload.get("treatment", "unknown"),
        outcome=payload.get("outcome", "unknown"),
        population=payload.get("population", "city"),
        time_window=payload.get("time_window", "NOT_AVAILABLE"),
        geographic_scope=payload.get("geographic_scope", "city"),
        estimand=payload.get("estimand", "ATE"),
        covariates=payload.get("covariates", []),
        assumptions=payload.get("assumptions", []),
        causal_design=payload.get("causal_design", "difference_in_differences"),
    )


@router.post("/dag/validate")
def validate_dag(payload: dict) -> dict:
    dag = DAG()
    for node in payload.get("nodes", []):
        dag.add_node(node.get("name"), node.get("node_type", "variable"))
    for edge in payload.get("edges", []):
        dag.add_edge(edge.get("source"), edge.get("target"))
    try:
        return dag.validate(treatment=payload.get("treatment"), outcome=payload.get("outcome"))
    except ValueError as exc:
        return {"status": "INVALID", "error": str(exc)}


@router.get("/designs")
def list_designs() -> dict[str, list[str]]:
    from citypulse.causal.designs import AVAILABLE_DESIGNS

    return {"designs": AVAILABLE_DESIGNS}


@router.post("/estimate")
def estimate_effect(payload: dict) -> dict:
    design = payload.get("design", "difference_in_differences")
    if design == "difference_in_differences":
        return difference_in_differences(
            treated_pre=payload.get("treated_pre"),
            treated_post=payload.get("treated_post"),
            control_pre=payload.get("control_pre"),
            control_post=payload.get("control_post"),
        )
    return {"status": "CAUSAL_EFFECT_NOT_IDENTIFIED", "method": design, "reason": "Design not implemented for the supplied evidence."}


@router.post("/diagnostics")
def causal_diagnostics(payload: dict) -> dict:
    adjustment = identify_adjustment_set(
        payload.get("treatment", "unknown"),
        payload.get("outcome", "unknown"),
        payload.get("confounders", []),
    )
    return {"status": "DIAGNOSTICS_READY", "adjustment": adjustment}


@router.post("/sensitivity")
def sensitivity_analysis(payload: dict) -> dict:
    return {"status": "NOT_RUN", "method": payload.get("method", "not_specified"), "limitations": ["Sensitivity checks require a valid causal design and measured covariates."]}


@router.post("/placebo")
def placebo_tests(payload: dict) -> dict:
    return {"status": "NOT_RUN", "method": payload.get("method", "not_specified"), "limitations": ["Placebo testing is only meaningful when a defined treatment and counterfactual window exist."]}


@router.get("/effects")
def list_effects() -> dict[str, list[str]]:
    return {"effects": []}


@router.post("/cross-city")
def cross_city(payload: dict) -> dict:
    return {"status": "NOT_SUPPORTED", "reason": "Cross-city causal transportability requires explicit city comparability and measured effect modifiers."}


@router.get("/reports")
def list_reports() -> dict[str, list[str]]:
    return {"reports": ["implementation_report.md", "synthetic_validation_report.md", "causal_method_report.md", "diagnostics_report.md", "sensitivity_report.md", "cross_city_report.md", "limitations_report.md"]}
