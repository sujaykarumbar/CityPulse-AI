# Validation Laboratory

## Purpose

The validation package provides bounded calculations and experiment utilities for
comparing supplied observations with forecasts or simulations. A utility returning
`MEASURED` means only that the calculation ran on the supplied values; it does not
establish that the values represent a city, a model's deployment population, or a
causal effect.

## Current checkout

Implemented building blocks include chronological and seeded spatial splits,
walk-forward evaluation, regression metrics, observed-versus-simulated residuals,
grid-search calibration, bootstrap intervals, seeded Monte Carlo parameter
sampling, synthetic traffic/mobility/energy/weather generation, synthetic-data
quality checks, missingness/noise perturbations, modality dropout, graph
perturbations, and distribution shifts. Monte Carlo outputs are labeled simulated;
their quantiles are not presented as confidence intervals. The frontend validation
dashboard reads the validation status, scorecard, and recorded runs.

The assistant's validation intent and the permission-checked `get_validation_evidence`
agent tool read the same local validation registry. When there are no recorded runs,
they return unavailable evidence instead of estimating performance. The MLOps model
registry still has its own validation status and promotion gate; its model lifecycle
is not yet linked to validation-run references or robustness results.

This checkout contains no verified urban validation dataset and no trained model
artifact. Therefore no historical model backtest, spatial transfer result, model
benchmark, calibration against observed city data, or synthetic-data utility result
is claimed. The scorecard intentionally reports these dimensions as unavailable or
not measured rather than combining them into a single score.

## Data splitting

`chronological_frame_split` sorts by parsed UTC time and keeps records with the same
timestamp in one partition. It returns train, validation, and test frames, plus
normalized time boundaries and leakage-control metadata. It does not fit or apply
preprocessing; callers must fit transformations on training data only.

`spatial_frame_holdout` uses a caller-selected entity column (for example a zone or
road-segment identifier), a seed, and a holdout fraction. Entities are disjoint
between partitions. It creates a split, not evidence of spatial generalization;
that requires a compatible predictor, target, and held-out observations.

## API

The local FastAPI service exposes:

- `GET /api/v1/validation/status`
- `GET /api/v1/validation/scorecard`
- `GET /api/v1/validation/runs`
- `GET /api/v1/validation/{validation_id}`
- `POST /api/v1/validation/backtest` for metrics over caller-supplied aligned arrays
- `POST /api/v1/validation/simulation` for residual comparisons
- `POST /api/v1/validation/synthetic` and `/synthetic/compare`
- `POST /api/v1/validation/robustness/missing-data`

Requests that execute currently implemented calculations have bounded Pydantic
payloads. These are local synchronous endpoints; authentication, authorization,
request-ID propagation, audit logging, and asynchronous job scheduling are not yet
implemented for the validation router. Do not expose it as a production research
execution service without those controls.

## Evidence and status semantics

- `GROUND_TRUTH_NOT_AVAILABLE`: no observations were supplied for a metric.
- `VALIDATION_NOT_AVAILABLE`: required validation inputs or artifacts are absent.
- `NOT_MEASURED`: a metric or experiment was not calculated or is undefined for its
  supplied values.
- `SYNTHETIC`: generated data; it is never represented as a real observation.
- `SIMULATED`: simulation output; residuals require aligned observed values.

All stochastic generators and perturbations record their seed. Results should also
record dataset, feature, graph, model, and simulation versions before being used as
reproducible experiment evidence. Missing lineage must remain an explicit limitation.

## Verification

Run the focused suite with:

```powershell
python -m pytest tests/validation -q
```

The tests verify deterministic generation, split invariants, metric behavior,
perturbation bounds, and API serialization. They do not substitute for experiments
on real, versioned datasets.