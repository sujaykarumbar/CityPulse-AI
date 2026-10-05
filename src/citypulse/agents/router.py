from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.agents.registry import AgentDefinition, AgentRegistry
from citypulse.agents.schemas import AgentTaskResult, ResearchTaskRequest
from citypulse.agents.supervisor import SupervisorAgent
from citypulse.agents.tools.citypulse_tools import build_tool_registry

router = APIRouter(prefix="/agents", tags=["agents"])
supervisor = SupervisorAgent()
agent_registry = AgentRegistry()

for domain, description, tool in (
    ("traffic", "Traffic analysis via registered traffic tools.", "get_current_traffic"),
    ("mobility", "Mobility analysis via aggregated mobility tools.", "get_mobility_state"),
    ("energy", "Energy analysis via registered energy tools.", "get_current_energy"),
    ("weather", "Weather context from configured weather services.", "get_weather_context"),
    ("risk", "Risk analysis from risk event APIs.", "get_active_risks"),
    ("simulation", "Scenario simulation through validated simulation APIs.", "run_scenario"),
    ("decision", "Decision analysis from measured candidate results.", "get_decision_results"),
    ("mlops", "Model and experiment registry inspection.", "get_model_registry"),
    ("validation", "Read validation status and recorded evidence.", "get_validation_evidence"),
    ("data_quality", "Dataset quality and lineage inspection.", "get_data_quality"),
    ("research", "Urban representation status and indexed-record search.", "get_urban_foundation_status"),
):
    agent_registry.register(AgentDefinition(agent_id=f"{domain}-agent", name=f"{domain.title()} Agent", description=description, role=f"{domain}_analysis", tools=[tool], permissions=["viewer"], max_tool_calls=1))
agent_registry.register(AgentDefinition(agent_id="critic-agent", name="Verification Agent", description="Checks source-linked evidence, epistemic state and unsupported causality.", role="verification", permissions=["evidence.read"], max_tool_calls=0))
agent_registry.register(AgentDefinition(agent_id="synthesis-agent", name="Synthesis Agent", description="Preserves partial results and unavailable domain states.", role="synthesis", permissions=["evidence.read"], max_tool_calls=0))


@router.get("")
def list_agents() -> list[dict]:
    return [agent.model_dump(mode="json") for agent in agent_registry.list()]


@router.post("/tasks", response_model=AgentTaskResult)
def create_task(request: ResearchTaskRequest) -> AgentTaskResult:
    return supervisor.run(request)


@router.get("/tasks/{task_id}", response_model=AgentTaskResult)
def get_task(task_id: str) -> AgentTaskResult:
    task = supervisor.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND"})
    return task


@router.post("/tasks/{task_id}/cancel")
def cancel_task(task_id: str) -> dict[str, str]:
    task = supervisor.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND"})
    return {"task_id": task_id, "status": "CANCELLATION_NOT_SUPPORTED_AFTER_SYNCHRONOUS_COMPLETION"}


@router.get("/tasks/{task_id}/events")
def task_events(task_id: str) -> dict[str, object]:
    task = supervisor.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail={"code": "TASK_NOT_FOUND"})
    return {"task_id": task_id, "events": [{"event": "agent_completed", "agent_id": state.agent_id, "status": state.status} for state in task.agent_states]}
