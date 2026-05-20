from __future__ import annotations

import pandas as pd


def correlate_incidents(incidents: pd.DataFrame, signals: pd.DataFrame) -> pd.DataFrame:
    correlated = incidents.copy()
    correlated["related_signal_count"] = correlated["data_product_id"].map(
        lambda product_id: int((signals["data_product_id"] == product_id).sum())
    )
    correlated["correlation_reason"] = "Data product has related degraded or risk signals."
    return correlated
