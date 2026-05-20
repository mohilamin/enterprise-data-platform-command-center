from __future__ import annotations

import pandas as pd


def ai_governance_average(signals: pd.DataFrame) -> float:
    subset = signals.loc[signals["system_name"] == "ai_data_governance_gateway"]
    return round(float(subset["metric_value"].mean()), 2)
