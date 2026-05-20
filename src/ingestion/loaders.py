from __future__ import annotations

import pandas as pd

from src.common.paths import project_path


def load_catalog() -> pd.DataFrame:
    return pd.read_csv(project_path("data/data_products/data_product_catalog.csv"))


def load_platform_signals() -> pd.DataFrame:
    return pd.read_csv(project_path("data/raw_signals/system_health_signals.csv"))


def load_incidents() -> pd.DataFrame:
    return pd.read_csv(project_path("data/incidents/platform_incidents.csv"))
