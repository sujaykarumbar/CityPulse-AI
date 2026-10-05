# Synthetic causal validation report

This validation uses synthetic ground-truth data only to confirm estimator implementation correctness. It does not claim any real-world intervention effect in a production city.

## Benchmark

The synthetic test checks that an implemented estimator recovers a known effect near the true value with a tolerance threshold. The result is interpreted as `SIMULATED` and `SYNTHETIC` rather than a real-world estimate.

## Status

`MEASURED` for synthetic recovery logic
`NOT_RUN` for live real-world causal effect estimation
