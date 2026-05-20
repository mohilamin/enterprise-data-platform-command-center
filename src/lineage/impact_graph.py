from __future__ import annotations

import pandas as pd


def build_impact_edges(incidents: pd.DataFrame) -> pd.DataFrame:
    return (
        incidents[["incident_id", "data_product_id"]]
        .rename(columns={"incident_id": "source", "data_product_id": "target"})
        .assign(relationship="impacts")
    )
