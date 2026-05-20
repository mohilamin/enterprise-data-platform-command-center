from __future__ import annotations

from src.ingestion.loaders import load_catalog


def get_data_products():
    return load_catalog()
