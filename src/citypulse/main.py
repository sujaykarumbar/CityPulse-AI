from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest

from citypulse import __version__
from citypulse.agents.research_router import router as research_router
from citypulse.agents.router import router as agents_router
from citypulse.assistant.router import router as assistant_router
from citypulse.causal.router import router as causal_router
from citypulse.config import get_settings
from citypulse.evaluation.router import router as evaluation_router
from citypulse.foresight.router import router as foresight_router
from citypulse.global_city.router import router as global_city_router
from citypulse.governance.router import router as governance_router
from citypulse.knowledge_graph.router import router as knowledge_graph_router
from citypulse.mlops.router import router as mlops_router
from citypulse.models.urban_foundation.router import router as urban_foundation_router
from citypulse.operations.router import router as operations_router
from citypulse.policy.router import router as policy_router
from citypulse.security.router import router as security_router
from citypulse.streaming.router import router as streaming_router
from citypulse.transfer.router import router as transfer_router
from citypulse.validation.router import router as validation_router

settings = get_settings()
HTTP_REQUESTS = Counter(
    "citypulse_http_requests_total",
    "Completed HTTP requests handled by CityPulse.",
    ("method", "route", "status"),
)
HTTP_REQUEST_DURATION = Histogram(
    "citypulse_http_request_duration_seconds",
    "HTTP request duration in seconds.",
    ("method", "route"),
)
HTTP_ACTIVE_REQUESTS = Gauge(
    "citypulse_http_active_requests",
    "HTTP requests currently being handled.",
)

app = FastAPI(
    title=settings.app_name,
    version=__version__,
    description="The service boundary for CityPulse urban intelligence capabilities.",
)


@app.middleware("http")
async def collect_http_metrics(request: Request, call_next) -> Response:
    if request.url.path == "/metrics":
        return await call_next(request)
    start = perf_counter()
    status_code = 500
    HTTP_ACTIVE_REQUESTS.inc()
    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    finally:
        route = request.scope.get("route")
        route_name = getattr(route, "path", "unmatched")
        HTTP_REQUESTS.labels(request.method, route_name, str(status_code)).inc()
        HTTP_REQUEST_DURATION.labels(request.method, route_name).observe(perf_counter() - start)
        HTTP_ACTIVE_REQUESTS.dec()


app.include_router(assistant_router, prefix=settings.api_prefix)
app.include_router(agents_router, prefix=settings.api_prefix)
app.include_router(research_router, prefix=settings.api_prefix)
app.include_router(mlops_router, prefix=settings.api_prefix)
app.include_router(urban_foundation_router, prefix=settings.api_prefix)
app.include_router(streaming_router, prefix=settings.api_prefix)
app.include_router(validation_router, prefix=settings.api_prefix)
app.include_router(evaluation_router, prefix=settings.api_prefix)
app.include_router(security_router, prefix=settings.api_prefix)
app.include_router(governance_router, prefix=settings.api_prefix)
app.include_router(operations_router, prefix=settings.api_prefix)
app.include_router(foresight_router, prefix=settings.api_prefix)
app.include_router(global_city_router, prefix=settings.api_prefix)
app.include_router(knowledge_graph_router, prefix=settings.api_prefix)
app.include_router(transfer_router, prefix=settings.api_prefix)
app.include_router(causal_router, prefix=settings.api_prefix)
app.include_router(policy_router, prefix=settings.api_prefix)


@app.get("/health", tags=["system"])
def health() -> dict[str, str]:
    """Return a lightweight liveness response for local development and monitoring."""

    return {"status": "ok", "environment": settings.environment}


@app.get("/live", tags=["system"])
def liveness() -> dict[str, str]:
    return {"status": "alive"}


@app.get("/ready", tags=["system"])
def readiness() -> dict[str, str]:
    return {"status": "ready", "required_dependencies": "none"}


@app.get("/metrics", tags=["system"])
def metrics() -> Response:
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get(f"{settings.api_prefix}/system", tags=["system"])
def system_info() -> dict[str, str]:
    """Expose non-sensitive service metadata."""

    return {
        "name": settings.app_name,
        "version": __version__,
        "environment": settings.environment,
    }
