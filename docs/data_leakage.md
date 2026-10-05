# Data Leakage Safeguards

Temporal features are generated from timestamps, and lag or rolling values use `shift(1)` before aggregation. This ensures a row cannot use its own target or future observations in a past-only feature.

The leakage checker reports suspicious target-derived names, post-event names, and unsorted timestamps. Reports require human review because naming alone cannot prove causality. Time-series consumers must use chronological train/validation/test splits; random splitting is not appropriate for forecasting.
