from __future__ import annotations

import pandas as pd


def quality_score(signals: pd.DataFrame) -> float:
    quality = signals.loc[signals["metric_name"].str.contains("quality|freshness|quarantine", regex=True)]
    return round(float(quality["metric_value"].mean()), 2)
