from __future__ import annotations

import json

import pandas as pd
from fastapi import FastAPI, HTTPException

from src.api.schemas import IncidentRequest
from src.common.paths import project_path
from src.pipeline.run_all import run_pipeline

app = FastAPI(title="Enterprise Data Platform Command Center")


def _csv(path: str) -> list[dict]:
    full = project_path(path)
    return pd.read_csv(full).to_dict(orient="records") if full.exists() else []


def _json(path: str) -> dict:
    full = project_path(path)
    return json.loads(full.read_text(encoding="utf-8")) if full.exists() else {}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "enterprise-data-platform-command-center"}


@app.get("/platform-summary")
def platform_summary() -> dict:
    return _json("data/scorecards/platform_health_scorecard.json")


@app.get("/data-products")
def data_products() -> list[dict]:
    return _csv("data/data_products/data_product_catalog.csv")


@app.get("/data-products/{data_product_id}")
def data_product_detail(data_product_id: str) -> dict:
    for row in _csv("data/scorecards/data_product_health_report.csv"):
        if row["data_product_id"] == data_product_id:
            return row
    raise HTTPException(status_code=404, detail="Data product not found")


@app.get("/incidents")
def incidents() -> list[dict]:
    return _csv("data/scorecards/cross_platform_incident_report.csv")


@app.get("/incidents/{incident_id}")
def incident_detail(incident_id: str) -> dict:
    for row in incidents():
        if row["incident_id"] == incident_id:
            return row
    raise HTTPException(status_code=404, detail="Incident not found")


@app.get("/governance-heatmap")
def governance_heatmap() -> list[dict]:
    return _csv("data/scorecards/governance_heatmap.csv")


@app.get("/ai-readiness")
def ai_readiness() -> dict:
    return _json("data/scorecards/ai_readiness_summary.json")


@app.get("/sla-report")
def sla_report() -> dict:
    return _json("data/scorecards/platform_sla_report.json")


@app.get("/lineage-impact")
def lineage_impact() -> dict:
    return _json("data/lineage/lineage_impact_graph.json")


@app.get("/executive-summary")
def executive_summary() -> dict:
    return _json("data/executive/executive_summary.json")


@app.get("/scorecards")
def scorecards() -> dict:
    return {
        "platform_health": _json("data/scorecards/platform_health_scorecard.json"),
        "enterprise_risk": _json("data/scorecards/enterprise_risk_summary.json"),
        "ai_readiness": _json("data/scorecards/ai_readiness_summary.json"),
    }


@app.post("/simulate-incident")
def simulate_incident(request: IncidentRequest) -> dict:
    return {
        "status": "simulated",
        "incident_type": request.incident_type,
        "data_product_id": request.data_product_id,
        "severity": request.severity,
    }


@app.post("/refresh-platform-health")
def refresh_platform_health() -> dict[str, object]:
    return run_pipeline()
