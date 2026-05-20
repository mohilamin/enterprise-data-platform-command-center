from __future__ import annotations

from pydantic import BaseModel


class IncidentRequest(BaseModel):
    incident_type: str = "simulated_platform_incident"
    data_product_id: str = "DP-012"
    severity: str = "high"
