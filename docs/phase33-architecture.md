# Phase 33 Architecture

## Audit summary

The repository already contains a valid evidence-first foundation: graph-based urban network intelligence, adaptive strategy loops, causal analysis, policy experimentation, behavioral modeling, foresight, and AI assistant tooling. The Phase 33 layer extends those components rather than duplicating them.

## New economic layer

### Data contracts

The new economic package introduces explicit schemas for economic observations, industry factors, trade, freight, commodity, and resource-flow indicators. These contracts preserve the reporting semantics used across CITYPULSE: observed, modeled, simulated, scenario-based, and unsupported.

### Economic profiles

City economic profiles are lightweight model-derived summaries built from available metadata only. They never fabricate actual employment or trade values when source data is missing.

### Supply-chain graph

The supply-chain graph uses explicit nodes and weighted relationships to represent dependency, supplier, production, and distribution structure. It is designed to integrate cleanly with the existing network graph and risk/adaptive layers.

### Shock simulation

Economic shocks are represented as scenario estimates with severity, duration, affected sectors, and explicit caveats about simulation status. This supports cross-domain propagation into mobility, energy, and network risk without pretending the outcomes are observed data.

### Resilience and specialization

The resilience engine computes dimension-wise summaries rather than a single normative score, preserving distributional and uncertainty complexity. The specialization engine exposes a location quotient-like signal for sector concentration using a clear model-derived status.

## Integration points

- Existing network graph: dependency and cascade analysis
- Causal engine: evidence and eligibility checks for economic intervention claims
- Policy engine: scenario and trade-off handling
- Foresight engine: future economic scenario framing
- Adaptive strategy: trigger and review loops
- AI assistant: evidence-aware economic tooling
- API layer: compact route surface under `/api/v1/economy`
