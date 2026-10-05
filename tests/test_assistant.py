from citypulse.assistant.intent import classify_intent, extract_entities
from citypulse.assistant.schemas import ChatRequest
from citypulse.assistant.service import AssistantService
from fastapi.testclient import TestClient
from citypulse.main import app


def test_intent_and_entity_extraction() -> None:
    assert classify_intent("What is traffic on road 123?") == "TRAFFIC_STATUS"
    assert classify_intent("How was the traffic model validated?") == "VALIDATION_STATUS"
    assert extract_entities("What is traffic on road 123?")[0].value == "123"


def test_unavailable_domain_data_is_not_fabricated() -> None:
    response = AssistantService().chat(ChatRequest(message="What is happening with traffic right now?"))

    assert response.status == "unavailable"
    assert "cannot provide" in response.answer.lower()
    assert response.metadata["tool_status"] == "unavailable"


def test_unknown_question_requests_clarification() -> None:
    response = AssistantService().chat(ChatRequest(message="Tell me something"))

    assert response.status == "clarification"
    assert response.intent == "UNKNOWN"


def test_validation_answer_reports_missing_evidence_without_fabricating() -> None:
    response = AssistantService().chat(ChatRequest(message="How was the traffic model validated?"))

    assert response.intent == "VALIDATION_STATUS"
    assert response.status == "unavailable"
    assert "no verified real dataset" in response.answer.lower()
    assert response.citations[0].endpoint == "/api/v1/validation/status"


def test_assistant_http_contract_is_structured() -> None:
    response = TestClient(app).post("/api/v1/assistant/chat", json={"message": "What is traffic right now?"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["intent"] == "TRAFFIC_STATUS"
    assert payload["status"] == "unavailable"
    assert "citations" in payload
