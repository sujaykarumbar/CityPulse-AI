# Causal Urban Intelligence implementation report

## Scope

This report documents the Phase 26 causal layer for CityPulse. It adds a transparent causal question model, DAG validation, treatment/outcome definitions, causal design registry, estimation routines, temporal checks, and explicit `NOT_IDENTIFIED` semantics when assumptions are missing.

## Evidence rules

- Causal methods never assume correlation means causation.
- Treatment must be explicitly defined.
- Outcomes must be well defined and temporally ordered.
- When the required evidence is absent, the system returns `CAUSAL_EFFECT_NOT_IDENTIFIED` or `NOT_IDENTIFIED`.
- Synthetic benchmarks are used only for implementation validation, not for real-world claims.

## Implemented components

- `citypulse.causal.questions`
- `citypulse.causal.dag.graph`
- `citypulse.causal.designs.difference_in_differences`
- `citypulse.causal.router`

## Status

Current implementation status is `MEASURED` for the causal scaffolding and `NOT_RUN` for live observational causal estimates without real urban intervention data.
