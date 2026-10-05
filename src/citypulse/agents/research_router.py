from __future__ import annotations

from fastapi import APIRouter, HTTPException

from citypulse.agents.schemas import AgentTaskResult, ResearchTaskRequest
from citypulse.agents.supervisor import SupervisorAgent

router = APIRouter(prefix="/research", tags=["research"])
supervisor = SupervisorAgent()


@router.post("/run", response_model=AgentTaskResult)
def run_research(request: ResearchTaskRequest) -> AgentTaskResult:
    request.mode = "RESEARCH"
    return supervisor.run(request)


@router.get("/{run_id}", response_model=AgentTaskResult)
def get_research(run_id: str) -> AgentTaskResult:
    result = supervisor.get_task(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail={"code": "RESEARCH_RUN_NOT_FOUND"})
    return result


@router.get("/{run_id}/report")
def get_report(run_id: str) -> dict:
    result = supervisor.get_task(run_id)
    if result is None:
        raise HTTPException(status_code=404, detail={"code": "RESEARCH_RUN_NOT_FOUND"})
    return {"run_id": run_id, "status": result.status, "report": result.answer, "evidence": [item.model_dump(mode="json") for item in result.evidence], "limitations": result.verification.get("limitations", [])}
