# Operations and Recovery

## Health and metrics

- `GET /live` reports process liveness.
- `GET /ready` reports application readiness. It currently checks no external dependencies because none are required by the local app configuration.
- `GET /health` remains the existing lightweight health response.
- `GET /metrics` exports process-local Prometheus HTTP request totals, request duration, and active requests. Metrics are not a substitute for uptime or dependency health.

The Compose monitoring profile scrapes the API and provisions Grafana with Prometheus. This profile was syntax-checked only; its services have not been started or validated together.

## Backups and recovery

Database, model, configuration, and object-storage backups are `NOT_CONFIGURED`. No isolated restore test exists. RPO and RTO are `NOT_DEFINED`. Do not represent named development volumes as verified backups.

Kubernetes restart policies, probes, disruption budgets, autoscaling, network policies, RBAC, TLS, rollout rollback, and chaos/recovery testing are `NOT_IMPLEMENTED` or `NOT_TESTED`. The Compose restart policy is local container restart behavior only, not high availability.

## Local service profiles

`docker compose --env-file .env up -d` starts API and frontend. Optional profiles are `database`, `cache`, `streaming`, and `monitoring`. Keep the stack on a trusted development host only: current published service ports are not restricted to loopback, and Redis/Redpanda use development-oriented settings.
