from __future__ import annotations

import pytest

from src.pipeline.run_all import run_pipeline


@pytest.fixture(scope="session")
def built_platform():
    return run_pipeline()
