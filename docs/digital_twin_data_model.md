# Digital Twin Data Model

The frontend is prepared for these backend entities:

- Building: footprint plus optional height, levels, type, and zone.
- Road and road segment: geometry plus stable identifier and optional traffic properties.
- Zone: polygon geometry and stable zone identifier.
- Transit: stop or route geometry when supplied.
- Risk event: backend-provided location, lifecycle, severity, and mode.
- Scenario impact: backend-provided baseline/scenario/difference geometry and metrics.

All geometry must arrive through a backend API as validated GeoJSON or a documented 3D Tiles endpoint. Missing fields remain unavailable.
