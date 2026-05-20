from __future__ import annotations

import pandas as pd


def calculate_platform_health(data_product_health: pd.DataFrame) -> dict[str, object]:
    score = round(float(data_product_health["data_product_health_score"].mean()), 2)
    status = "healthy" if score >= 85 else "watch" if score >= 70 else "degraded" if score >= 50 else "critical"
    return {
        "platform_health_score": score,
        "status": status,
        "drivers": "Average data product health.",
        "recommended_action": "Prioritize degraded products.",
    }
