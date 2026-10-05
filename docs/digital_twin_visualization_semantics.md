# Visualization Semantics

- Color identifies a configured layer or backend classification; it is not a universal severity scale.
- Extrusion, when added, is a visualization transform and not physical elevation unless sourced from terrain/building data.
- Opacity controls visibility and does not represent probability.
- Animation represents playback or backend event updates, never certainty.
- `OBSERVED`, `FORECAST`, and `SIMULATED` are separate modes and must not be blended.
- Marker size is a display parameter unless the backend explicitly provides an impact radius.
