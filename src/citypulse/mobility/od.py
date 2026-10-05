from __future__ import annotations

import pandas as pd


def build_od_matrix(
    df: pd.DataFrame,
    timestamp_column: str,
    origin_column: str,
    destination_column: str,
    demand_column: str | None = None,
    frequency: str = "h",
) -> pd.DataFrame:
    """Return privacy-aware aggregated OD flows, never individual trip output."""

    required = [timestamp_column, origin_column, destination_column]
    missing = [column for column in required if column not in df.columns]
    if missing:
        raise ValueError(f"OD construction requires columns: {', '.join(missing)}")
    working = df.copy()
    working[timestamp_column] = pd.to_datetime(working[timestamp_column], errors="coerce", utc=True)
    working = working.dropna(subset=required)
    working["time_bucket"] = working[timestamp_column].dt.floor(frequency)
    if demand_column and demand_column in working.columns:
        working["flow_value"] = pd.to_numeric(working[demand_column], errors="coerce").fillna(0)
        aggregation = "sum"
    else:
        working["flow_value"] = 1.0
        aggregation = "count"
    od = (
        working.groupby(["time_bucket", origin_column, destination_column], as_index=False)["flow_value"]
        .agg(trip_count=aggregation)
        .rename(columns={origin_column: "origin_id", destination_column: "destination_id"})
    )
    inflow = od.groupby(["time_bucket", "destination_id"], as_index=False)["trip_count"].sum()
    inflow = inflow.rename(columns={"destination_id": "zone_id", "trip_count": "inflow"})
    outflow = od.groupby(["time_bucket", "origin_id"], as_index=False)["trip_count"].sum()
    outflow = outflow.rename(columns={"origin_id": "zone_id", "trip_count": "outflow"})
    zone_flow = inflow.merge(outflow, on=["time_bucket", "zone_id"], how="outer").fillna(0)
    zone_flow["net_flow"] = zone_flow["inflow"] - zone_flow["outflow"]
    return od, zone_flow
