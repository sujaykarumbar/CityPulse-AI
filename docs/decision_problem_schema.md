# Decision Problem Schema

A decision problem supplies objectives, optional constraints, and candidate scenarios with measured metric values. Objective weights must sum to 1.0. Candidate metrics that are absent are marked `not_run` or `not_available`; values are never fabricated.

Pareto dominance is direction-aware: a candidate must be no worse on every configured objective and strictly better on at least one.
