# Model Validation

Validation produces `PASS`, `WARN`, or `FAIL`. It checks artifact URI presence, lineage metadata, local artifact existence when a `file:` URI is supplied, and configured metric gates. Missing thresholds or metrics produce warnings rather than invented pass/fail values.
