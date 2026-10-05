# Scenario Methodology

Scenario execution follows a deterministic order: changes are applied in the order listed in the scenario, each to a deep copy of the baseline state. Supported transformations are explicit multipliers, graph edge state changes, lane reductions, hypothetical edge records, weather perturbations, and transit-change records.

For a numeric metric, the reported delta is:

`absolute_delta = scenario_value - baseline_value`

When the baseline is non-zero:

`percentage_delta = absolute_delta / baseline_value * 100`

These are model-state comparisons. They are not causal estimates, observed outcomes, or guarantees.
