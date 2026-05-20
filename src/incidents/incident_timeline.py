from __future__ import annotations

import pandas as pd

from src.common.time import utc_now_iso


def build_incident_timeline(incidents: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for incident in incidents.itertuples(index=False):
        rows.append(
            {
                "incident_id": incident.incident_id,
                "event_sequence": 1,
                "timestamp": utc_now_iso(),
                "timeline_event_type": "correlated",
                "description": f"Correlated {incident.incident_type} across {incident.systems_involved}.",
            }
        )
    return pd.DataFrame(rows)
