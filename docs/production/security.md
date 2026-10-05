# Production Security Status

The CI workflow includes Gitleaks, Python/npm dependency audits, pull-request dependency review, and Trivy scans for API/frontend images. Scan gates are high severity for dependency review and npm, and high/critical for container images. No scan result for a GitHub Actions run is claimed here.

`.env.example` contains placeholders only and is explicitly unignored so it can be tracked. Copy it to `.env` for local use and replace local service passwords; never use these placeholders in shared or production environments. Real secrets belong in a managed secret store or protected deployment environment.

The API and frontend container definitions specify non-root runtime users, but the API artifact-directory write permission has not been fixed or verified. Local Compose port bindings currently expose services on host interfaces, so do not run optional unauthenticated Redis/Redpanda services on an untrusted network.

Production authentication, authorization, rate limiting, audit logging, TLS termination, external secret management, Kubernetes RBAC, NetworkPolicy, image signing, and production branch/environment protection are not configured. This setup is not approved for production use.
