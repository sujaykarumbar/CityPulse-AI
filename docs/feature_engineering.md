# Feature Engineering

The feature layer is split into temporal, domain, spatial, and leakage modules. Temporal cyclical encodings map periodic values onto a circle, so hour 23 and hour 0 remain close numerically.

Features are generated only when their source columns exist. No city coordinates, holidays, road capacity, or target values are fabricated. Every pipeline output includes a feature version and generation timestamp in its report.
