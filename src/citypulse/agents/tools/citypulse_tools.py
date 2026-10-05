from __future__ import annotations

from pathlib import Path

from citypulse.agents.tools.registry import ToolDefinition, ToolRegistry, ToolResult
from citypulse.mlops.registry import ModelRegistry
from citypulse.models.urban_foundation.service import UrbanFoundationService
from citypulse.streaming.service import StreamingService
from citypulse.validation.service import ValidationService


def build_tool_registry() -> ToolRegistry:
    registry = ToolRegistry()
    model_registry = ModelRegistry()
    foundation = UrbanFoundationService()
    streaming = StreamingService()
    validation = ValidationService()
    registry.register(
        ToolDefinition(tool_id="get_model_registry", name="Get model registry", description="Read local CITYPULSE model records.", permissions=["viewer"]),
        lambda _: ToolResult(tool_id="get_model_registry", status="success", data={"models": [model.model_dump(mode="json") for model in model_registry.list()]}),
    )
    registry.register(
        ToolDefinition(tool_id="get_validation_evidence", name="Get validation evidence", description="Read validation status and recorded validation runs without inferring unmeasured results.", permissions=["viewer"]),
        lambda _: ToolResult(
            tool_id="get_validation_evidence",
            status="success",
            data={
                "status": validation.status(),
                "runs": [run.model_dump(mode="json") for run in validation.registry.list()[-10:]],
            },
        ),
    )
    registry.register(
        ToolDefinition(tool_id="get_stream_status", name="Get stream status", description="Read actual local streaming status.", permissions=["viewer"]),
        lambda _: ToolResult(tool_id="get_stream_status", status="success", data=streaming.status().model_dump(mode="json")),
    )
    registry.register(
        ToolDefinition(tool_id="get_urban_foundation_status", name="Get representation status", description="Read urban representation research-layer status.", permissions=["viewer"]),
        lambda _: ToolResult(tool_id="get_urban_foundation_status", status="success", data=foundation.status().model_dump(mode="json")),
    )
    registry.register(
        ToolDefinition(tool_id="search_urban_foundation_index", name="Search representation index", description="Search only locally indexed representation records.", permissions=["viewer"], input_fields=["query", "top_k"]),
        lambda args: ToolResult(tool_id="search_urban_foundation_index", status="success", data=foundation.search(args["query"], args.get("top_k", 5))),
    )
    for domain, tool in (("traffic", "get_current_traffic"), ("mobility", "get_mobility_state"), ("energy", "get_current_energy"), ("weather", "get_weather_context"), ("risk", "get_active_risks"), ("geospatial", "get_geospatial_context"), ("simulation", "run_scenario"), ("decision", "get_decision_results"), ("data_quality", "get_data_quality")):
        registry.register(
            ToolDefinition(tool_id=tool, name=f"Read {domain}", description=f"Read {domain} from a domain API not present in this checkout.", permissions=["viewer"]),
            lambda _, tool_id=tool: ToolResult(tool_id=tool_id, status="unavailable", error_code="DATA_NOT_AVAILABLE"),
        )
    return registry
