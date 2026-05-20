from __future__ import annotations

import json

import pandas as pd

from src.common.paths import ensure_dir, project_path
from src.lineage.dependency_graph import build_dependency_edges
from src.lineage.impact_graph import build_impact_edges


def export_graphs(signals: pd.DataFrame, catalog: pd.DataFrame, incidents: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    nodes, edges = build_dependency_edges(signals, catalog)
    impact_edges = build_impact_edges(incidents)
    all_edges = pd.concat([edges, impact_edges], ignore_index=True)
    out = ensure_dir(project_path("data/lineage"))
    nodes.to_csv(out / "dependency_nodes.csv", index=False)
    all_edges.to_csv(out / "dependency_edges.csv", index=False)
    graph = {"nodes": nodes.to_dict(orient="records"), "edges": all_edges.to_dict(orient="records")}
    (out / "system_dependency_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    (out / "lineage_impact_graph.json").write_text(json.dumps(graph, indent=2), encoding="utf-8")
    return nodes, all_edges
