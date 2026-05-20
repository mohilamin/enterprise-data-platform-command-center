from __future__ import annotations

import pandas as pd


def build_dependency_edges(signals: pd.DataFrame, catalog: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    system_nodes = signals[["system_name"]].drop_duplicates().rename(columns={"system_name": "node_id"})
    system_nodes["node_type"] = "system"
    product_nodes = catalog[["data_product_id", "name"]].rename(columns={"data_product_id": "node_id"})
    product_nodes["node_type"] = "data_product"
    product_nodes["label"] = product_nodes["name"]
    system_nodes["label"] = system_nodes["node_id"]
    nodes = pd.concat(
        [system_nodes[["node_id", "label", "node_type"]], product_nodes[["node_id", "label", "node_type"]]], ignore_index=True
    )
    edges = (
        signals[["system_name", "data_product_id"]].drop_duplicates().rename(columns={"system_name": "source", "data_product_id": "target"})
    )
    edges["relationship"] = "emits_signal_for"
    return nodes, edges
