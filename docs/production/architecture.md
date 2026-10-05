# Production Architecture Status

## Current foundation

The repository now has a FastAPI health/readiness surface, Prometheus HTTP request metrics at `/metrics`, API and frontend container definitions, a profile-based Compose file, and a consolidated CI workflow. The frontend image uses an unprivileged Nginx base; the API Dockerfile declares a non-root runtime user.

Compose profiles describe optional local PostgreSQL/PostGIS, Redis, Redpanda, Prometheus, and Grafana services. The application does not yet connect to those services by default. The API continues to use local JSON stores and the local streaming compatibility implementation.

## Not production-ready

The Docker daemon was unavailable during this implementation, so neither image build nor Compose startup was executed. Static review also found that the API image does not create a writable `/app/artifacts` directory before switching to UID 10001; app startup may fail when registries create their directories. The Compose contract test flags host port bindings that are not restricted to loopback. Do not expose this stack to an untrusted network.

No Kubernetes, Helm, Terraform, cloud provisioning, image publishing, deployment workflow, worker service, database migrations, production identity provider, external secrets, backup/restore automation, tracing, alerting, or operational dashboard is configured. RPO and RTO are `NOT_DEFINED`; uptime, capacity, and cost are `NOT_MEASURED`.

## Promotion boundary

The CI workflow verifies repository tests and builds/scans API and frontend images in GitHub Actions. It does not deploy to staging or production. Production environment approval, branch protection, model security/resource gates, canary behavior, rollback automation, and release manifests remain `NOT_IMPLEMENTED`.

Treat this repository as a development foundation until the infrastructure contract tests pass, container builds and runtime checks succeed, and production controls are reviewed and enabled in the hosting environment.
