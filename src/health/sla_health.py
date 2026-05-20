from __future__ import annotations

import pandas as pd


def calculate_sla_health(signals: pd.DataFrame) -> pd.DataFrame:
    sla = signals.loc[signals["metric_name"].str.contains("sla|freshness", regex=True)].copy()
    sla["sla_met"] = sla["status"].isin(["healthy", "watch"])
    return sla
