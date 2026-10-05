from __future__ import annotations

from pydantic import BaseModel, Field


class AgentDefinition(BaseModel):
    agent_id: str
    name: str
    description: str
    role: str
    version: str = "1.0.0"
    model_provider: str = "deterministic_tools"
    model_name: str | None = None
    prompt_version: str = "1.0.0"
    tools: list[str] = Field(default_factory=list)
    permissions: list[str] = Field(default_factory=list)
    timeout_seconds: float = 5.0
    max_tool_calls: int = 1
    max_tokens: int = 0
    status: str = "active"


class AgentRegistry:
    def __init__(self) -> None:
        self._agents: dict[str, AgentDefinition] = {}

    def register(self, agent: AgentDefinition) -> None:
        if agent.agent_id in self._agents:
            raise ValueError(f"AGENT_ALREADY_REGISTERED:{agent.agent_id}")
        self._agents[agent.agent_id] = agent

    def get(self, agent_id: str) -> AgentDefinition | None:
        return self._agents.get(agent_id)

    def list(self) -> list[AgentDefinition]:
        return list(self._agents.values())
