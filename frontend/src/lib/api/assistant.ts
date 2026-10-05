import { api } from "./client";
import { assistantResponseSchema, type AssistantResponse } from "../../types/assistant";

export async function sendAssistantMessage(message: string, conversationId?: string): Promise<AssistantResponse> {
  const response = await api.post("/api/v1/assistant/chat", {
    message,
    conversation_id: conversationId,
  });
  return assistantResponseSchema.parse(response.data);
}
