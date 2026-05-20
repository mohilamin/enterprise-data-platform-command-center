from __future__ import annotations


def severity_score(severity: str) -> int:
    return {"low": 25, "medium": 50, "high": 75, "critical": 95}.get(severity, 50)
