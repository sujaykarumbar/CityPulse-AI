from __future__ import annotations

from citypulse.assistant.grounding import grounded_unavailable
from citypulse.assistant.intent import classify_intent, extract_entities
from citypulse.assistant.schemas import AssistantResponse, ChatRequest, Citation, ToolDefinition, ToolResult
from citypulse.assistant.tools import ToolRegistry, unavailable_tool
from citypulse.mlops.registry import ModelRegistry
from citypulse.models.urban_foundation.service import UrbanFoundationService
from citypulse.streaming.service import StreamingService
from citypulse.validation.service import ValidationService


class AssistantService:
    def __init__(self) -> None:
        self.registry = ToolRegistry()
        self.model_registry = ModelRegistry()
        self.streaming_service = StreamingService()
        self.urban_foundation_service = UrbanFoundationService()
        self.validation_service = ValidationService()
        self._register_unavailable_domain_tools()
        self._register_mlops_tools()
        self._register_validation_tools()
        self._register_urban_foundation_tools()

    def _register_unavailable_domain_tools(self) -> None:
        for name, description in {
            "get_current_traffic": "Retrieve current traffic from the traffic API.",
            "get_current_energy": "Retrieve current energy from the energy API.",
            "get_mobility_state": "Retrieve aggregated mobility from the mobility API.",
            "get_active_risks": "Retrieve active risk events from the risk API.",
            "run_scenario": "Run a validated urban scenario.",
            "get_decision_results": "Retrieve measured decision-analysis results.",
        }.items():
            definition, handler = unavailable_tool(name, description, "viewer" if name != "run_scenario" else "analyst")
            self.registry.register(definition, handler)

    def _register_mlops_tools(self) -> None:
        self.registry.register(
            ToolDefinition(name="get_model_registry", description="List registered CITYPULSE models."),
            lambda _: ToolResult(
                tool="get_model_registry",
                status="success",
                data={"models": [model.model_dump(mode="json") for model in self.model_registry.list()]},
            ),
        )
        self.registry.register(
            ToolDefinition(name="get_retraining_history", description="List CITYPULSE retraining candidates."),
            lambda _: ToolResult(
                tool="get_retraining_history",
                status="success",
                data={"jobs": [job.model_dump(mode="json") for job in self.model_registry.retraining_jobs()]},
            ),
        )

    def _register_urban_foundation_tools(self) -> None:
        self.registry.register(
            ToolDefinition(name="get_urban_foundation_status", description="Inspect the local multimodal urban representation layer."),
            lambda _: ToolResult(
                tool="get_urban_foundation_status",
                status="success",
                data=self.urban_foundation_service.status().model_dump(mode="json"),
            ),
        )

    def _register_validation_tools(self) -> None:
        self.registry.register(
            ToolDefinition(name="get_validation_evidence", description="Read validation status and recorded validation results."),
            lambda _: ToolResult(
                tool="get_validation_evidence",
                status="success",
                data={
                    "status": self.validation_service.status(),
                    "runs": [run.model_dump(mode="json") for run in self.validation_service.registry.list()[-10:]],
                },
            ),
        )
        self.registry.register(
            ToolDefinition(name="search_urban_foundation_index", description="Search local urban representation records by query and modality context."),
            lambda arguments: ToolResult(
                tool="search_urban_foundation_index",
                status="success",
                data=self.urban_foundation_service.search(arguments.get("query", ""), top_k=int(arguments.get("top_k", 5))).get("items", []),
            ),
        )

    def chat(self, request: ChatRequest) -> AssistantResponse:
        intent = classify_intent(request.message)
        entities = extract_entities(request.message)
        if intent == "UNKNOWN":
            return AssistantResponse(
                answer="I could not identify a supported CITYPULSE analysis request. Ask about traffic, energy, mobility, risk, system status, scenarios, or decisions.",
                intent=intent,
                entities=entities,
                status="clarification",
                uncertainty="Intent resolution was ambiguous.",
            )
        tool_name = {
            "TRAFFIC_STATUS": "get_current_traffic",
            "ENERGY_STATUS": "get_current_energy",
            "MOBILITY_STATUS": "get_mobility_state",
            "RISK_STATUS": "get_active_risks",
            "SCENARIO_CREATE": "run_scenario",
            "DECISION_ANALYSIS": "get_decision_results",
            "MODEL_INFORMATION": "get_model_registry",
            "VALIDATION_STATUS": "get_validation_evidence",
            "STREAM_STATUS": "stream_status",
        }.get(intent)
        if intent == "SYSTEM_STATUS":
            return AssistantResponse(
                answer="System status is available through the verified health and system endpoints. The assistant domain APIs are not configured in this checkout.",
                intent=intent,
                entities=entities,
                citations=[Citation(source_type="PROJECT_DOCUMENTATION", source_id="api", label="Verified API foundation", endpoint="/api/v1/system")],
            )
        if intent == "GENERAL_PROJECT_QUERY":
            return AssistantResponse(
                answer="CITYPULSE is currently configured with verified data-quality, energy, mobility, simulation, decision, and frontend foundations. Live assistant domain tools are not available in this checkout.",
                intent=intent,
                entities=entities,
                citations=[Citation(source_type="PROJECT_DOCUMENTATION", source_id="readme", label="Project documentation")],
            )
        if intent == "VALIDATION_STATUS":
            result = self.registry.execute("get_validation_evidence", {}, role="viewer")
            validation_status = result.data["status"]
            runs = result.data["runs"]
            citations = [Citation(source_type="VALIDATION_REGISTRY", source_id="validation-status", label="Validation status", endpoint="/api/v1/validation/status")]
            if not runs:
                return AssistantResponse(
                    answer="Validation is unavailable in the current checkout: no verified real dataset, trained model artifact, or recorded validation run is available.",
                    intent=intent,
                    citations=citations,
                    metadata={"tool": "get_validation_evidence", "validation_status": validation_status},
                    status="unavailable",
                    uncertainty="No validation experiment has been recorded.",
                )
            latest = runs[-1]
            metrics = [
                f"{metric['name']}={metric['value']}" if metric.get("status") == "MEASURED" else f"{metric['name']}=NOT_MEASURED"
                for metric in latest.get("metric_results", [])
            ]
            citations.append(Citation(source_type="VALIDATION_RUN", source_id=latest["validation_id"], label="Recorded validation run", endpoint=f"/api/v1/validation/{latest['validation_id']}", timestamp=latest.get("timestamp")))
            answer = f"The latest recorded validation run is for {latest['task']} (status: {latest['status']}). Metrics: {', '.join(metrics) or 'NOT_MEASURED'}."
            limitations = latest.get("limitations", [])
            if limitations:
                answer += f" Limitations: {' '.join(limitations)}"
            return AssistantResponse(
                answer=answer,
                intent=intent,
                citations=citations,
                metadata={"tool": "get_validation_evidence", "validation_id": latest["validation_id"]},
                status="completed",
                uncertainty="This reports a stored calculation only; it does not establish generalization beyond its supplied data.",
            )
        if intent == "MODEL_INFORMATION":
            result = self.registry.execute("get_model_registry", {}, role="viewer")
            models = result.data.get("models", [])
            answer = "No CITYPULSE models are registered in the current local registry." if not models else f"The registry contains {len(models)} model record(s)."
            return AssistantResponse(answer=answer, intent=intent, metadata={"tool": "get_model_registry", "model_count": len(models)}, status="completed")
        if intent == "STREAM_STATUS":
            status = self.streaming_service.status()
            return AssistantResponse(answer=f"The streaming broker status is {status.status}. Live event connectivity is not configured.", intent=intent, metadata={"tool": "stream_status", **status.model_dump(mode="json")}, status="completed", uncertainty="No live stream is connected.")
        if intent == "GENERAL_PROJECT_QUERY" and "foundation" in request.message.lower() or "representation" in request.message.lower() or "multimodal" in request.message.lower():
            status = self.urban_foundation_service.status()
            return AssistantResponse(
                answer="The repository includes a local urban representation evidence layer, but no large-scale pretrained foundation model is trained here. It is ready for multimodal research metadata and vector-index experiments without claiming a city foundation model.",
                intent="GENERAL_PROJECT_QUERY",
                entities=entities,
                metadata={"tool": "get_urban_foundation_status", **status.model_dump(mode="json")},
                status="completed",
                uncertainty="No large-scale pretrained model exists in this checkout.",
            )
        if tool_name is None:
            return AssistantResponse(answer="This request is not supported.", intent=intent, status="blocked")
        result = self.registry.execute(tool_name, {"message": request.message}, role="viewer")
        if result.status != "success":
            return AssistantResponse(
                answer=grounded_unavailable(intent.lower().replace("_", " "), result.error),
                intent=intent,
                entities=entities,
                evidence=result.evidence,
                metadata={"tool": tool_name, "tool_status": result.status},
                status="unavailable" if result.status == "unavailable" else "blocked",
                uncertainty="No live CITYPULSE result was available.",
            )
        return AssistantResponse(answer="The requested CITYPULSE result is available.", intent=intent, entities=entities, evidence=result.evidence)
