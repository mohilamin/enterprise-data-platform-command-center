from __future__ import annotations

import pandas as pd


def policy_violation_count(signals: pd.DataFrame) -> int:
    return int(signals.loc[signals["metric_name"].str.contains("policy_violations"), "metric_value"].sum())
