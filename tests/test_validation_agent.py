from citypulse.agents.orchestration.planner import plan_task
from citypulse.agents.schemas import ResearchTaskRequest
from citypulse.agents.tools.citypulse_tools import build_tool_registry


def test_validation_question_routes_to_read_only_validation_agent() -> None:
    plan = plan_task(ResearchTaskRequest(user_request="How was the traffic model validated?"))

    assert len(plan.nodes) == 1
    assert plan.nodes[0].domain == "validation"
    assert plan.nodes[0].tool_id == "get_validation_evidence"


def test_validation_tool_preserves_unavailable_evidence_state() -> None:
    result = build_tool_registry().execute("get_validation_evidence", {}, role="viewer")

    assert result.status == "success"
    assert result.data["status"]["real_datasets"] == "NOT_AVAILABLE"
    assert result.data["status"]["trained_models"] == "NOT_AVAILABLE"


def test_validation_tool_rejects_unrecognized_role() -> None:
    result = build_tool_registry().execute("get_validation_evidence", {}, role="unauthorized")

    assert result.status == "denied"
    assert result.error_code == "PERMISSION_DENIED"