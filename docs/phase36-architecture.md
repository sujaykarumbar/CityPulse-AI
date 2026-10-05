# Phase 36 — Public Services, Human Wellbeing & Service Accessibility Digital Twin

## Problem

The CityPulse platform already models physical infrastructure, mobility, energy, environment, economic systems, networks, risk, and policy. However, the platform lacked a dedicated public-services layer that could separate facility presence from service access, service quality, demand, capacity, equity, and resilience.

## Objectives

- Model public-service facilities as explicit digital-twin objects.
- Compute accessibility using configurable thresholds and modeled travel proxies.
- Separate facility presence from quality, capacity, utilization, and outcome measures.
- Connect public service coverage to population demand and equity analysis.
- Support service disruption and resilience simulation without claiming unverified causal effects.
- Expose evidence-first APIs and scenario logic for service planning.

## Architecture

The public-services domain is intentionally additive to the existing CityPulse stack rather than a replacement. It sits alongside the network, environmental, economic, policy, foresight, and adaptive layers.

```
Population / Behavior / Mobility
        ↓
Public Service Demand
        ↓
Facilities
        ↓
Capacity / Utilization
        ↓
Accessibility / Coverage
        ↓
Equity / Service Gaps
        ↓
Resilience / Simulation
        ↓
Policy / Optimization / Foresight
        ↓
Human Review
```

## Data model

The service layer distinguishes several dimensions:

- Location and geometry
- Service taxonomy and facility status
- Demand estimates and usage proxies
- Capacity and operational availability
- Accessibility by threshold and mode
- Equity and distributional analysis
- Resilience under service shock scenarios

## Service taxonomy

Service categories are configurable and are not assumed to exist in every city. Common categories include:

- EDUCATION
- HEALTHCARE
- EMERGENCY
- FIRE
- POLICE
- WASTE
- WATER_SERVICE
- SANITATION
- PUBLIC_TRANSPORT
- SOCIAL_SERVICE
- ADMINISTRATIVE
- PARKS
- RECREATION
- LIBRARIES
- COMMUNITY_CENTERS
- PUBLIC_HOUSING
- ENERGY_SERVICE
- DIGITAL_PUBLIC_SERVICE

## Facility model

Facilitiy records contain:

- facility_id
- service_type
- name
- geometry
- latitude/longitude
- administrative_area
- ownership
- operational_status
- capacity
- capacity_unit
- opening_hours
- source
- source_timestamp
- confidence

Each facility record retains provenance for source and transformation details.

## Accessibility model

Accessibility is treated as a modeled quantity, not proof of service quality. It can be computed using threshold-based travel proxies, nearest-facility approximations, and time-distance curves. This means:

- model-derived proximity is not the same as actual service quality
- a facility being nearby is not proof of adequate care or access
- multimodal accessibility requires real transport data; otherwise, the model remains conservative and labeled

## Demand model

Service demand may use:

- direct observations
- model estimates
- population-based proxies
- historical utilization patterns

All estimates must be labeled as `DIRECT_OBSERVATION`, `PROXY`, or `MODEL_ESTIMATE`.

## Capacity model

Capacity is separated from demand and service quality. The system tracks:

- nominal capacity
- available capacity
- current load
- forecast load
- capacity utilization
- capacity alert status

## Equity model

Equity analysis is distribution-based. It studies mean, median, and percentile access across areas or groups without over-interpreting disparities as discrimination unless the evidence supports that statement.

## Simulation integration

The public-services domain integrates with existing scenario/simulation logic through model-only disruption scenarios. It can simulate:

- facility closure
- transport disruption
- service demand shock
- budget constraint
- infrastructure degradation

Every scenario remains explicitly labeled as `MODEL_DERIVED` or `SIMULATED` rather than a recorded historical event.

## Causal integration

The system does not infer causal effectiveness from service location alone. It distinguishes between:

- observed access
- correlated trends
- predictive modeling
- simulated scenarios
- causal evidence
- assumed relationships
- unknown outcomes

## Decision integration

Facility optimization returns Pareto-style candidate trade-offs rather than a single universal answer. Users can compare objective weights for coverage, equity, resilience, and cost.

## API architecture

The public-services router exposes the domain under the standard FastAPI patterns used across CityPulse:

- /api/v1/services
- /api/v1/services/facilities
- /api/v1/services/accessibility/analyze
- /api/v1/services/demand
- /api/v1/services/demand/forecast
- /api/v1/services/capacity
- /api/v1/services/equity
- /api/v1/services/resilience
- /api/v1/services/scenarios/run
- /api/v1/services/optimization/location

## Frontend architecture

The front-end surface is designed as a service-lab rather than a standalone application. It supports:

- service overview
- facility explorer
- accessibility analysis
- service gaps
- equity summaries
- resilience drill-downs
- optimization trade-offs

## Validation

Validation focuses on:

- registry correctness
- facility provenance
- accessibility thresholds
- capacity status logic
- resilience scoring
- API availability
- scenario reproducibility

## Governance, privacy and security

- No identifiable individual data is reconstructed.
- Facility and service data are kept at aggregate or anonymized levels when possible.
- Inputs and outputs are explicitly labeled with provenance and uncertainty.
- Unauthorized access is prevented using the project’s existing API and security conventions.

## Limitations

This Phase 36 implementation intentionally does not claim real-world facility counts, waiting times, service quality, or causal policy effectiveness without source evidence. Where data is absent, the system uses `NOT_AVAILABLE` or `GROUND_TRUTH_NOT_AVAILABLE` semantics and clearly marks the result as model-derived.
