# Phase 31 Architecture

This repository already contains validated simulation, decision, causal, behavioral, policy, and foresight layers. Phase 31 adds an adaptive intelligence loop on top of them rather than replacing those subsystems.

## Core pattern

The new layer keeps the repository’s evidence-first semantics and implements a decision-support loop:

1. estimate current city state
2. compare observed values to assumptions
3. detect meaningful change
4. assess strategy performance against expected outcomes
5. trigger reassessment when assumptions or metrics drift
6. generate candidate strategies and compare them with simulation and robustness logic
7. require human review before any real-world action is considered

## Components

- `citypulse.adaptive.state`: strategy-state and state-estimation schemas
- `citypulse.adaptive.assumptions`: assumption registry and drift checks
- `citypulse.adaptive.change_detection`: simple change-event detection and regime classification
- `citypulse.adaptive.strategy`: strategy lifecycle, health, and alternative generation
- `citypulse.adaptive.engine`: orchestration for adaptive monitoring and reassessment
- `citypulse.adaptive.router`: FastAPI endpoints under `/api/v1/adaptive`

## Semantics

All adaptive outputs explicitly preserve the same provenance language used elsewhere in CITYPULSE:

- `OBSERVED`
- `ESTIMATED`
- `SIMULATED`
- `SCENARIO_ESTIMATE`
- `MODEL_DERIVED`
- `SYNTHETIC`
- `NOT_AVAILABLE`
- `INSUFFICIENT_DATA`

The adaptive loop does not execute real-world infrastructure changes or policy deployment. It produces decision support only.
