from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter
from uuid import uuid4

from citypulse.agents.budget import BudgetCounter
from citypulse.agents.evidence.bus import EvidenceBus
from citypulse.agents.orchestration.planner import plan_task
from citypulse.agents.schemas import AgentRunState, AgentTaskResult, Evidence, ResearchTaskRequest
from citypulse.agents.tools.registry import ToolRegistry, ToolResult
from citypulse.agents.verification.critic_agent import verify_outputs

UNAVAILABLE_DOMAINS = {"traffic", "mobility", "energy", "weather", "risk", "simulation", "decision", "geospatial", "data_quality"}


class AgentOrchestrator:
    def __init__(self, registry: ToolRegistry) -> None:
        self.registry = registry
        self.tasks: dict[str, AgentTaskResult] = {}

    def run(self, request: ResearchTaskRequest, role: str = "viewer") -> AgentTaskResult:
        started = perf_counter()
        task_id = str(uuid4())
        run_id = str(uuid4())
        plan = plan_task(request)
        counter = BudgetCounter(request.budget)
        bus = EvidenceBus()
        states: list[AgentRunState] = []
        outputs: list[dict] = []
        for node in plan.nodes:
            state = AgentRunState(agent_id=node.agent_id, task_id=task_id, status="RUNNING")
            states.append(state)
            if not counter.allow_agent() or not counter.allow_tool():
                state.status = "FAILED"
                state.error_code = "BUDGET_EXCEEDED"
                state.completed_at = datetime.now(timezone.utc)
                continue
            tool_result = self.registry.execute(node.tool_id, {"query": request.user_request, "message": request.user_request, "top_k": 5}, role=role)
            state.tool_calls = 1
            state.completed_at = datetime.now(timezone.utc)
            state.output = tool_result.model_dump(mode="json")
            if tool_result.status == "success":
                state.status = "COMPLETED"
                for item in tool_result.evidence:
                    evidence = Evidence.model_validate(item)
                    bus.publish(evidence)
                    state.evidence_refs.append(evidence.evidence_id)
                outputs.append({"agent_id": node.agent_id, "status": "completed", "data": tool_result.data})
            elif tool_result.status == "denied":
                state.status = "DENIED"
                state.error_code = tool_result.error_code
                outputs.append({"agent_id": node.agent_id, "status": "denied", "error_code": tool_result.error_code})
            elif tool_result.status == "unavailable":
                state.status = "UNAVAILABLE"
                state.error_code = tool_result.error_code or "DATA_NOT_AVAILABLE"
                outputs.append({"agent_id": node.agent_id, "status": "unavailable", "error_code": state.error_code})
            else:
                state.status = "FAILED"
                state.error_code = tool_result.error_code
                outputs.append({"agent_id": node.agent_id, "status": "failed", "error_code": state.error_code})
        evidence = bus.collect()
        verification = verify_outputs([], evidence)
        unavailable = [node.domain for node, state in zip(plan.nodes, states) if state.status in {"UNAVAILABLE", "FAILED", "DENIED"}]
        if unavailable and any(state.status == "COMPLETED" for state in states):
            task_status = "PARTIALLY_COMPLETED"
        elif unavailable:
            task_status = "PARTIALLY_COMPLETED"
        else:
            task_status = "COMPLETED"
        summary = self._synthesize(plan, states, unavailable, evidence)
        result = AgentTaskResult(
            task_id=task_id,
            run_id=run_id,
            status=task_status,
            request=request.user_request,
            plan=plan,
            agent_states=states,
            evidence=evidence,
            verification=verification,
            conflicts=[],
            answer=summary,
            reproducibility={
                "agents": [node.agent_id for node in plan.nodes],
                "tool_registry_version": "1.0.0",
                "model_provider": "deterministic_tools",
                "dataset_versions": "NOT_AVAILABLE",
                "feature_versions": "NOT_AVAILABLE",
                "graph_version": "NOT_AVAILABLE",
                "elapsed_seconds": round(perf_counter() - started, 6),
                "tool_calls": counter.tool_calls,
            },
        )
        self.tasks[task_id] = result
        return result

    @staticmethod
    def _synthesize(plan, states, unavailable: list[str], evidence: list[Evidence]) -> str:
        lines = [f"Workflow: {plan.workflow_type}.", "Agent status:"]
        for state in states:
            lines.append(f"- {state.agent_id}: {state.status}" + (f" ({state.error_code})" if state.error_code else ""))
        if evidence:
            lines.append(f"Evidence collected: {len(evidence)} item(s). Claims should be checked against cited evidence.")
        else:
            lines.append("Evidence: DATA_NOT_AVAILABLE from the current domain APIs.")
        if unavailable:
            lines.append("Unavailable domains: " + ", ".join(unavailable) + ".")
        lines.append("Causal effect: CAUSAL_EFFECT_NOT_ESTABLISHED.")
        return "\n".join(lines)

    def get(self, task_id: str) -> AgentTaskResult | None:
        return self.tasks.get(task_id)
