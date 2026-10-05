# Data Quality

The Phase 3 score is a transparent weighted combination:

`score = 100 * (0.35 completeness + 0.30 validity + 0.20 uniqueness + 0.15 consistency)`

- **Completeness**: non-null cells divided by all cells.
- **Validity**: rows satisfying coordinate, timestamp, and non-negative measurement rules divided by total rows.
- **Uniqueness**: one minus exact duplicate rows divided by total rows.
- **Consistency**: normalized snake_case column names divided by total columns.

A score is a diagnostic, not a claim that the data is scientifically correct. Invalid coordinates and timestamps are rejected by cleaning; missing values are retained for an explicit downstream strategy rather than silently invented.

## Outliers

Phase 3 flags quality problems and produces descriptive profiles. The pipeline adds IQR and z-score boolean flags for configured numeric measurements; it does not delete legitimate extreme events. Isolation Forest remains an optional later comparison once source schemas and temporal resolution are established in Phase 2.
