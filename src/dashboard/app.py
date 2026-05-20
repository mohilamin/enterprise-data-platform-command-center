from __future__ import annotations

import json

import pandas as pd
import streamlit as st

from src.common.paths import project_path


def _csv(path: str) -> pd.DataFrame:
    full = project_path(path)
    return pd.read_csv(full) if full.exists() else pd.DataFrame()


def _json(path: str) -> dict:
    full = project_path(path)
    return json.loads(full.read_text(encoding="utf-8")) if full.exists() else {}


st.set_page_config(page_title="Enterprise Data Platform Command Center", layout="wide")
st.title("Enterprise Data Platform Command Center")
summary = _json("data/scorecards/platform_health_scorecard.json")
risk = _json("data/scorecards/enterprise_risk_summary.json")
tabs = st.tabs(
    [
        "Executive Overview",
        "Platform Health",
        "Data Product Health",
        "AI Readiness",
        "Governance Heatmap",
        "Cross-System Incidents",
        "SLA Compliance",
        "RAG Quality Risk",
        "Fraud MLOps Risk",
        "Semantic Metric Trust",
        "Pipeline Reliability",
        "Data Quality Status",
        "Lineage Impact Graph",
        "Executive Summary",
    ]
)
with tabs[0]:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Platform Health", summary.get("platform_health_score", 0))
    c2.metric("Status", summary.get("status", "unknown"))
    c3.metric("Incidents", risk.get("total_incidents", 0))
    c4.metric("Critical Incidents", risk.get("critical_incidents", 0))
with tabs[1]:
    st.json(summary)
with tabs[2]:
    st.dataframe(_csv("data/scorecards/data_product_health_report.csv"), use_container_width=True)
with tabs[3]:
    st.json(_json("data/scorecards/ai_readiness_summary.json"))
with tabs[4]:
    st.dataframe(_csv("data/scorecards/governance_heatmap.csv"), use_container_width=True)
with tabs[5]:
    st.dataframe(_csv("data/scorecards/cross_platform_incident_report.csv"), use_container_width=True)
with tabs[6]:
    st.json(_json("data/scorecards/platform_sla_report.json"))
with tabs[7]:
    st.dataframe(_csv("data/raw_signals/rag_quality_signals.csv"), use_container_width=True)
with tabs[8]:
    st.dataframe(_csv("data/raw_signals/fraud_mlops_signals.csv"), use_container_width=True)
with tabs[9]:
    st.dataframe(_csv("data/raw_signals/semantic_metrics_signals.csv"), use_container_width=True)
with tabs[10]:
    st.dataframe(_csv("data/raw_signals/pipeline_reliability_signals.csv"), use_container_width=True)
with tabs[11]:
    st.dataframe(_csv("data/raw_signals/data_quality_signals.csv"), use_container_width=True)
with tabs[12]:
    st.json(_json("data/lineage/lineage_impact_graph.json"))
with tabs[13]:
    st.json(_json("data/executive/executive_summary.json"))
