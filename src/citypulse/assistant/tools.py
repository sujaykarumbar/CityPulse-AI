from __future__ import annotations

from collections.abc import Callable
from typing import Any

from citypulse.assistant.schemas import ToolDefinition, ToolResult


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, tuple[ToolDefinition, Callable[[dict[str, Any]], ToolResult]]] = {}

    def register(self, definition: ToolDefinition, handler: Callable[[dict[str, Any]], ToolResult]) -> None:
        self._tools[definition.name] = (definition, handler)

    def definitions(self) -> list[ToolDefinition]:
        return [definition for definition, _ in self._tools.values()]

    def execute(self, name: str, arguments: dict[str, Any], role: str = "viewer") -> ToolResult:
        registered = self._tools.get(name)
        if not registered:
            return ToolResult(tool=name, status="unavailable", error="Tool is not registered")
        definition, handler = registered
        roles = {"viewer": 0, "analyst": 1, "operator": 2, "admin": 3}
        if roles.get(role, -1) < roles.get(definition.required_role, 99):
            return ToolResult(tool=name, status="forbidden", error="Permission denied for this tool")
        try:
            return handler(arguments)
        except Exception as exc:
            return ToolResult(tool=name, status="error", error=f"Tool execution failed: {type(exc).__name__}")


def unavailable_tool(name: str, description: str, required_role: str = "viewer") -> tuple[ToolDefinition, Callable[[dict[str, Any]], ToolResult]]:
    definition = ToolDefinition(name=name, description=description, required_role=required_role)

    def handler(_: dict[str, Any]) -> ToolResult:
        return ToolResult(tool=name, status="unavailable", error="The corresponding CITYPULSE API is not available")

    return definition, handler
