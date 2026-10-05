# Phase 12 Decision Engine

The decision layer evaluates explicit candidate metrics and preserves trade-offs. It does not choose a political outcome or declare a universal best option.

```mermaid
flowchart LR
    Problem[Decision problem] --> Candidates[Candidate scenarios]
    Candidates --> Evaluate[Measured objective and constraint evaluation]
    Evaluate --> Pareto[Pareto filtering]
    Evaluate --> Sensitivity[Sensitivity analysis]
    Evaluate --> Robustness[Robustness summary]
    Pareto --> Report[Decision report]
```

When simulation integration is available, candidates can carry Phase 11 scenario definitions. In this checkout, the scenario engine and decision engine are independently testable, but no real city-state data or risk engine exists for end-to-end urban optimization.
