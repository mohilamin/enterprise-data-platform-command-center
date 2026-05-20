from __future__ import annotations

import pandas as pd

from src.storage.duckdb_store import write_warehouse


def load_command_center_warehouse(tables: dict[str, pd.DataFrame]) -> None:
    write_warehouse(tables)
