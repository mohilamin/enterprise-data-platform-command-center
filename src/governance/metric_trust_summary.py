from __future__ import annotations

import pandas as pd


def semantic_trust_average(signals: pd.DataFrame) -> float:
    subset = signals.loc[signals["metric_name"].str.contains("semantic_trust|lineage")]
    return round(float(subset["metric_value"].mean()), 2)
