from __future__ import annotations

from dataclasses import dataclass

from citypulse.agents.schemas import ExecutionBudget


@dataclass
class BudgetCounter:
    budget: ExecutionBudget
    agent_calls: int = 0
    tool_calls: int = 0

    def allow_agent(self) -> bool:
        if self.agent_calls >= self.budget.max_agents:
            return False
        self.agent_calls += 1
        return True

    def allow_tool(self) -> bool:
        if self.tool_calls >= self.budget.max_tool_calls:
            return False
        self.tool_calls += 1
        return True
