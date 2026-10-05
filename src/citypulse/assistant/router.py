from fastapi import APIRouter

from citypulse.assistant.schemas import AssistantResponse, ChatRequest
from citypulse.assistant.service import AssistantService

router = APIRouter(prefix="/assistant", tags=["assistant"])
service = AssistantService()


@router.post("/chat", response_model=AssistantResponse)
def chat(request: ChatRequest) -> AssistantResponse:
    return service.chat(request)
