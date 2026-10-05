from __future__ import annotations

from citypulse.agents.schemas import ResearchTaskRequest, TaskNode, TaskPlan

DOMAIN_TO_AGENT = {
    "traffic": ("traffic-agent", "get_current_traffic"),
    "mobility": ("mobility-agent", "get_mobility_state"),
    "energy": ("energy-agent", "get_current_energy"),
    "weather": ("weather-agent", "get_weather_context"),
    "risk": ("risk-agent", "get_active_risks"),
    "simulation": ("simulation-agent", "run_scenario"),
    "decision": ("decision-agent", "get_decision_results"),
    "geospatial": ("geospatial-agent", "get_geospatial_context"),
    "mlops": ("mlops-agent", "get_model_registry"),
    "validation": ("validation-agent", "get_validation_evidence"),
    "data_quality": ("data-quality-agent", "get_data_quality"),
    "research": ("research-agent", "search_urban_foundation_index"),
}


def plan_task(request: ResearchTaskRequest) -> TaskPlan:
    message = request.user_request.lower()
    selected = list(dict.fromkeys(domain.lower() for domain in request.domains if domain.lower() in DOMAIN_TO_AGENT))
    if not selected:
        if any(token in message for token in ("validation", "validated", "benchmark", "robustness")):
            selected = ["validation"]
        else:
            selected = [domain for domain in DOMAIN_TO_AGENT if domain.replace("_", " ") in message]
    if not selected:
        if any(token in message for token in ("similar", "historical", "embedding", "research")):
            selected = ["research", "data_quality"]
        elif any(token in message for token in ("system", "stream", "model", "foundation", "registry")):
            selected = ["mlops", "data_quality"]
        else:
            selected = ["traffic", "mobility", "weather", "data_quality"]
    selected = selected[: request.budget.max_agents]
    nodes = [
        TaskNode(node_id=f"{domain}-1", agent_id=DOMAIN_TO_AGENT[domain][0], domain=domain, tool_id=DOMAIN_TO_AGENT[domain][1])
        for domain in selected
    ]
    workflow = "SINGLE" if len(nodes) == 1 else "RESEARCH" if request.mode == "RESEARCH" else "PARALLEL"
    return TaskPlan(
        workflow_type=workflow,
        nodes=nodes,
        max_tool_calls=min(request.budget.max_tool_calls, len(nodes)),
        rationale="Deterministic domain routing over the supplied question and explicit requested domains.",
    )
