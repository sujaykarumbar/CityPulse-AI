# Validation Limitations

No verified real urban dataset or trained model artifact is available in this
checkout. Historical model backtesting, spatial transfer, simulation calibration
against observations, and model benchmarking are therefore not performed. No
forecasting, simulation, uncertainty-calibration, or synthetic-data-utility result
should be inferred from the framework tests.

The implemented temporal and spatial split helpers create partitions but do not
train models, fit preprocessing, or establish generalization. Callers must fit
normalization and feature transformations on training data only and provide versioned
datasets, targets, horizons, and model artifacts for evaluation.

Synthetic generators are explicitly labeled `SYNTHETIC`, seeded, and capped. Their
relationships are configurable assumptions, not realism claims. Synthetic-vs-real
comparison requires real reference samples; absent reference data returns
`VALIDATION_NOT_AVAILABLE`.

The validation API currently has no route-level authentication/authorization,
request-ID propagation, audit logging, or asynchronous job execution. It is a local
development interface, not a production experiment service. Only bounded inputs are
accepted by the implemented synchronous calculation endpoints.

A metric calculated from supplied arrays describes only those aligned values. It
does not establish model quality beyond the specified sample or causal validity.
