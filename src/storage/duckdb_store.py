from __future__ import annotations

import duckdb
import pandas as pd

from src.common.paths import ensure_dir, project_path


def write_warehouse(tables: dict[str, pd.DataFrame]) -> None:
    path = project_path("data/warehouse/enterprise_command_center.duckdb")
    ensure_dir(path.parent)
    with duckdb.connect(str(path)) as conn:
        for name, frame in tables.items():
            conn.register("frame_view", frame)
            conn.execute(f"CREATE OR REPLACE TABLE {name} AS SELECT * FROM frame_view")
            conn.unregister("frame_view")
