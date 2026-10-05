# MLOps Limitations

- No trained CITYPULSE model artifacts are present.
- MLflow and PostgreSQL registry backends are not configured.
- Metrics are only calculated from caller-supplied arrays.
- Drift is only calculated from caller-supplied reference/current values.
- Production deployment, Prometheus, Grafana, and delayed-label ingestion are not active.
- Monitoring health is distinct from predictive accuracy.
- Retraining creates candidates and never promotes automatically.
