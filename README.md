# CityPulse

CityPulse is an AI-powered digital twin and urban intelligence platform. It combines real urban data, geospatial processing, forecasting, graph learning, simulation, and explainable decision support.

## Current repository state

The checkout contains a verified foundation for data quality, energy profiling, mobility aggregation, deterministic counterfactual simulation, and transparent multi-objective decision analysis. No real city graph, verified traffic dataset, risk engine, PostGIS database, or trained forecasting artifacts are present, so unsupported results are reported as `NOT AVAILABLE`, `NOT MEASURED`, or `NOT RUN`.

## Phase 16: grounded assistant

The assistant is a controlled, evidence-first interface. It uses intent routing and an allow-listed tool registry; it never queries databases directly, executes arbitrary code, or invents unavailable urban values.

Backend endpoint:

```text
POST /api/v1/assistant/chat
```

Frontend route:

```text
/assistant
```

The current checkout exposes only verified system/health capabilities. Domain tools return explicit `unavailable` responses until their corresponding traffic, energy, mobility, risk, simulation, and decision APIs exist. Configure future provider settings through environment variables; no LLM secret is sent to the browser.

## Phase 17: MLOps

Phase 17 adds a local, auditable MLOps compatibility layer. It records model metadata, controlled lifecycle transitions, validation checks, lineage fields, retraining candidates, drift calculations, and ground-truth-aware monitoring summaries.

Run from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pipelines.mlops registry
python -m pipelines.mlops monitor
python -m pipelines.mlops drift
python -m pipelines.mlops report
```

The registry is stored under `artifacts/mlops/` when records are explicitly registered. No models are registered automatically. MLflow, PostgreSQL-backed registry storage, Prometheus, Grafana, deployments, and production metrics are not configured in this checkout and are reported as unavailable rather than fabricated.

## Phase 18: realtime streaming

Phase 18 adds a local streaming compatibility layer with validated event schemas, configurable topics, append-only event logs, at-least-once consumer semantics, idempotency, dead-letter records, dry-run replay, current-state storage, streaming health APIs, assistant stream-status grounding, and a realtime operations page.

Run from the repository root:

```powershell
$env:PYTHONPATH = "$PWD\src"
python -m pipelines.streaming status
python -m pipelines.streaming topics
```

The current status is intentionally `STREAM NOT CONNECTED`. No live urban source, Kafka/Redpanda broker, Redis state store, WebSocket event stream, stream processor cluster, or measured throughput/lag is active.

## Phase 21: validation laboratory foundation

The validation package includes chronological and spatial split utilities,
walk-forward evaluation, regression and simulation metrics, bounded synthetic data
generators, robustness perturbations, bootstrap intervals, calibration helpers, and
a validation dashboard at `/validation`. The FastAPI validation routes expose the
currently implemented calculations and explicitly label unavailable evidence.

No verified real urban validation dataset or trained model artifact is present, so
historical model performance, spatial transfer, simulation accuracy, benchmark
rankings, uncertainty calibration, and synthetic-data utility remain
`NOT_MEASURED` or `VALIDATION_NOT_AVAILABLE`. The API is for local development;
authentication, authorization, audit logging, request IDs, and asynchronous jobs are
not implemented for this router. See
[docs/validation/validation_architecture.md](docs/validation/validation_architecture.md)
and [docs/validation/limitations.md](docs/validation/limitations.md).

## Current status: Phase 3 foundation

Phase 1 established:

- a Python 3.11+ package layout under `src/`
- environment-based configuration with no committed secrets
- a FastAPI service with health and system metadata endpoints
- pytest and Ruff development tooling
- an architecture boundary for later data and ML modules

Phase 3 now adds:

- dataframe profiling with missingness, duplicates, statistics, correlations, time, and geographic ranges
- measurable quality scoring with documented weights
- validation and cleaning for timestamps, coordinates, and non-negative urban measurements
- configurable temporal, lag, rolling, traffic, and optional-reference spatial features
- non-destructive IQR and z-score outlier flags
- leakage-risk reporting for temporal and target-derived features
- a reproducible CSV-to-ML-ready pipeline with JSON reports

Phase 8 adds an energy-intelligence foundation:

- energy schema and frequency profiling
- optional, explicitly configured temporal regularization
- calendar, cyclical, lag, and past-only rolling features
- configurable peak flags and rolling z-score anomaly flags
- persistence and seasonal-naive baseline evaluation
- measured profile, anomaly, and model-comparison reports

Phase 9 adds a mobility-intelligence foundation:

- mobility schema profiling and record quality flags
- temporal mobility features
- privacy-aware, time-bucketed OD aggregation
- zone inflow, outflow, and net-flow calculations
- directed mobility graph metrics
- rolling demand anomaly flags

No mobility source is present in the repository, so mobility coverage, OD statistics, forecasts, and cross-domain relationships remain `NOT MEASURED`.

Phase 2 ingestion and real dataset selection are still intentionally separate work. This phase does not bundle fake urban data and does not claim a city has been selected.

## Local setup

PowerShell:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
```

Start the API:

```powershell
python -m uvicorn citypulse.main:app --reload
```

Open <http://127.0.0.1:8000/docs> for the interactive API documentation.

## Tests and quality checks

```powershell
python -m pytest
python -m ruff check .
```

## Phase 3 feature pipeline

Place real, processed CSV inputs under `data/processed/input/`, then run:

```powershell
python -m pipelines.features
```

The default output is written to `data/processed/ml_ready/`. Measured reports are written to `reports/` and include input/output rows, rejected rows, missingness before and after, quality dimensions, generated features, and leakage warnings. Source CSVs are never modified.

Use another input or configuration directory when needed:

```powershell
python -m pipelines.features --input-dir data/processed/input --output-dir data/processed/ml_ready --config config/features.yaml
```

The lag and rolling windows in `config/features.yaml` must match the source dataset's temporal resolution. Rolling features are shifted by one observation to avoid using the current target or future values.

## Phase 8 energy pipeline

No verified energy dataset is currently present in this checkout. Do not put invented values into the repository. When a legitimate CSV is available, place it under `data/processed/energy/` with `timestamp` and one target column such as `demand`, `load`, or `energy_consumption`.

Run the profile and baseline pipeline:

```powershell
python -m pipelines.energy_training
```

Outputs are written to `data/processed/energy_ml_ready/` and `reports/energy/`. Dataset provenance, coverage, frequency, weather alignment, deep-learning metrics, and traffic-energy relationships remain `NOT MEASURED` until real compatible inputs and the missing earlier-phase infrastructure are supplied.

## Phase 9 mobility pipeline

Place an approved, aggregated mobility CSV under `data/processed/mobility/`. The minimum OD schema is:

```text
timestamp,origin_zone,destination_zone
```

An optional `trip_count` column is aggregated as flow; otherwise each input row contributes one observed trip. Run staged processing with:

```powershell
python -m pipelines.mobility --stage profile
python -m pipelines.mobility --stage all
```

OD flows, zone flows, graph metrics, and anomaly reports are written under `reports/mobility/`. Individual-level trip records are never emitted by the OD output.

## Phase 11: simulation

The scenario engine applies validated deterministic transformations to an explicit baseline `UrbanState`. It never mutates the baseline and labels results as simulated counterfactual estimates.

```powershell
python -m pipelines.simulation --scenario config/scenarios/traffic_increase.yaml --baseline path\to\baseline.json
```

Supported transformations include demand and energy multipliers, weather perturbations, road closures, lane reductions, hypothetical road additions, and transit-change records. Real graph routing, risk recalculation, database persistence, and uncertainty estimation are unavailable in this checkout.

## Phase 12: decision analysis

Run the decision engine with candidate metrics supplied by actual simulation or model output:

```powershell
python -m pipelines.decision --problem config/decision/traffic_problem.yaml
```

The engine validates objective weights, evaluates constraints, computes weighted scores for measured candidates, and returns the complete Pareto set. It does not select a universal winner or invent missing cost/benefit values.

Documentation:

- [docs/simulation_architecture.md](docs/simulation_architecture.md)
- [docs/simulation_limitations.md](docs/simulation_limitations.md)
- [docs/decision_engine_architecture.md](docs/decision_engine_architecture.md)
- [docs/decision_limitations.md](docs/decision_limitations.md)

Expected smoke responses:

- `GET /health` returns `{"status":"ok","environment":"local"}`.
- `GET /api/v1/system` returns service name, version, and environment.

## Repository layout

```text
citypulse/
├── docs/              Architecture and research documentation
├── data/              Raw, interim, processed, and external data boundaries
├── config/            Feature-engineering configuration
├── reports/           Generated quality and feature reports
├── pipelines/         Command-line pipeline entry points
├── src/citypulse/     Installable Python package and API entry point
├── tests/              Automated tests
├── pyproject.toml      Packaging, dependencies, and tool configuration
└── .env.example        Non-secret local configuration template
```

## Development phases

1. Foundation and development environment
2. Dataset acquisition and ingestion
3. Data quality, profiling, and feature engineering
4. PostgreSQL/PostGIS and geographic processing
5. Traffic analytics and baseline ML
6. Forecasting, graph learning, energy, mobility, anomaly, risk, simulation, explainability, API, dashboard, MLOps, deployment, and research documentation

Detailed architecture notes are in [docs/architecture.md](docs/architecture.md).
