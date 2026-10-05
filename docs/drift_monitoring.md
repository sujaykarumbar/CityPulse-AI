# Drift Monitoring

The implemented numeric drift method is Population Stability Index (PSI). It compares reference and current histograms using reference-derived bins. A drift status is only emitted when a configured threshold exists; otherwise the result is `NOT_MEASURABLE`.

Feature drift and prediction drift do not prove concept drift. Concept drift requires input-target relationship evidence and is `CONCEPT_DRIFT_NOT_MEASURABLE` without delayed ground truth.
