# CI/CD

The single `.github/workflows/ci.yml` workflow runs backend tests and Ruff, frontend lint/typecheck/tests/build, Python and npm dependency audits, Gitleaks, pull-request dependency review, image builds, Trivy scans, and SPDX SBOM artifact uploads.

Audit thresholds are explicit: npm audit gates on high severity; Trivy gates on high and critical; dependency review gates on high. Python `pip-audit` scans the installed environment after CI upgrades pip. The frontend dependency tree was audited locally after updating Vitest to 4.1.11; npm reported zero vulnerabilities.

No CI run has been observed for this revision. GitHub Actions references use version tags, not verified immutable commit SHAs. The workflow does not publish images, deploy environments, require production approval, perform Playwright end-to-end tests, run migrations, or validate Kubernetes/Helm manifests. These capabilities must not be inferred from CI passing.
