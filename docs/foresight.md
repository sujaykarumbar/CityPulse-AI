# Phase 30: Urban Evolutionary Planning & Strategic Foresight

This phase introduces a synthetic, evidence-first long-horizon urban planning layer. It is deliberately scoped to model future scenarios, adaptive pathways, and strategy comparison without claiming deterministic predictive validity.

## Architecture

The foresight layer sits above the existing CityPulse stack and composes the existing simulation, policy, decision, causal, and behavioral capabilities. It does not replace them.

Key components:

- `citypulse.foresight.engine`: long-horizon future-state generation and synthetic evolution logic
- `citypulse.foresight.pathways`: adaptive strategy pathways and trigger evaluation
- `citypulse.foresight.robustness`: robustness and regret summaries
- `citypulse.foresight.router`: FastAPI endpoints for scenario and pathway support
- `pipelines.foresight`: command-line access for scenario and pathway generation

## Evidence semantics

All outputs are labeled with model-level provenance to preserve the repository’s no-fabrication standard.

- `SCENARIO_ESTIMATE` for synthetic plausible futures
- `MODEL_DERIVED` for decision-support metrics
- `SYNTHETIC` for intentionally non-empirical assumptions
- `NOT_AVAILABLE` when a real evidence source is absent

## Scope and limitations

This implementation intentionally avoids claiming real-world future predictions. It supports:

- future scenario generation using explicit assumptions
- simple state evolution under policy assumptions
- pathway monitoring and trigger logic
- robustness/regret analysis for strategy comparison

It does not implement a full database-backed operational foresight platform, a production-grade 3D future-state dashboard, or a real multi-city long-run optimizer. Those would require verified urban datasets and a much larger integration effort.
