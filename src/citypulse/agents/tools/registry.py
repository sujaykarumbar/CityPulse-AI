from __future__ import annotations

from collections.abc import Callable
from typing import Any

from pydantic import BaseModel, Field


class ToolDefinition(BaseModel):
    tool_id: str
    name: str
    description: str
    permissions: list[str] = Field(default_factory=lambda: ["viewer"])
    timeout_seconds: float = 5.0
    rate_limit_per_minute: int = 30
    version: str = "1.0.0"
    input_fields: list[str] = Field(default_factory=list)


class ToolResult(BaseModel):
    tool_id: str
    status: str
    data: dict[str, Any] = Field(default_factory=dict)
    evidence: list[dict[str, Any]] = Field(default_factory=list)
    error_code: str | None = None


Handler = Callable[[dict[str, Any]], ToolResult]


class ToolRegistry:
    _role_rank = {"viewer": 0, "analyst": 1, "operator": 2, "admin": 3}

    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolDefinition, Handler]] = {}

    def register(self, definition: ToolDefinition, handler: Handler) -> None:
        if definition.tool_id in self._tools:
            raise ValueError(f"TOOL_ALREADY_REGISTERED:{definition.tool_id}")
        self._tools[definition.tool_id] = (definition, handler)

    def definitions(self) -> list[ToolDefinition]:
        return [definition for definition, _ in self._tools.values()]

    def execute(self, tool_id: str, arguments: dict[str, Any], role: str) -> ToolResult:
        entry = self._tools.get(tool_id)
        if entry is None:
            return ToolResult(tool_id=tool_id, status="unavailable", error_code="TOOL_NOT_REGISTERED")
        definition, handler = entry
        required = max((self._role_rank.get(permission, 99) for permission in definition.permissions), default=0)
        if self._role_rank.get(role, -1) < required:
            return ToolResult(tool_id=tool_id, status="denied", error_code="PERMISSION_DENIED")
        unexpected = set(arguments) - set(definition.input_fields)
        if unexpected:
            return ToolResult(tool_id=tool_id, status="failed", error_code="INVALID_TOOL_ARGUMENTS")
        try:
            return handler(arguments)
        except Exception as exc:
            return ToolResult(tool_id=tool_id, status="failed", error_code=f"TOOL_FAILED:{type(exc).__name__}")
