from __future__ import annotations


def domain_status(domain: str) -> str:
    return "governed" if domain else "unknown"
