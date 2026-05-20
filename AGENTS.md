# AGENTS.md

You are building a production-style Data Engineering + AI Platform + Governance + Observability project.

Project name:
Enterprise Data Platform Command Center

Primary goal:
Build a local enterprise data platform command center that simulates a unified control plane for data quality, pipeline reliability, RAG evaluation, fraud MLOps, semantic metric trust, and AI governance risk.

## Build Principles

- Write clean, modular, production-style Python.
- Use Python 3.12.
- Use synthetic data only.
- Do not require external services in V0.1.
- Keep V0.1 deterministic and locally runnable.
- Every score must be explainable.
- Every incident must include system, severity, impact, and recommended action.
- Every major platform signal must map to a data product.
- Tests must cover generation, normalization, scoring, incidents, scorecards, API, and full pipeline.

## Commit Message Requirements

- Do not use generic AI-like commit messages.
- Use professional, scoped commit messages.
- Prefer Conventional Commit style, such as `feat(platform): add unified health scoring engine`.

## Definition of Done

Code runs locally, tests pass, ruff passes, README is updated, catalog exists, platform signals exist, incidents exist, normalized model exists, scorecards exist, lineage graphs exist, API and dashboard can run, and no real sensitive data is used.
