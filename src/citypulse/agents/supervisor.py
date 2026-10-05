from __future__ import annotations

from citypulse.agents.orchestration.executor import AgentOrchestrator
from citypulse.agents.schemas import ResearchTaskRequest
from citypulse.agents.tools.citypulse_tools import build_tool_registry


class SupervisorAgent:
    """Deterministic, bounded supervisor. No LLM or arbitrary tool execution."""

    def __init__(self) -> None:
        self.orchestrator = AgentOrchestrator(build_tool_registry())

    def run(self, request: ResearchTaskRequest, role: str = "viewer"):
        return self.orchestrator.run(request, role)

    def get_task(self, task_id: str):
        return self.orchestrator.get(task_id)
