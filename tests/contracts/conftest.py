from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

import pytest

from mindforge.contracts import CognitiveBudget, Provenance, ProvenanceKind


@pytest.fixture
def provenance() -> Provenance:
    return Provenance(kind=ProvenanceKind.USER, source_id='test-user')


@pytest.fixture
def budget() -> CognitiveBudget:
    return CognitiveBudget(
        max_latency_ms=500,
        max_model_calls=1,
        max_tokens=1000,
        max_parallel_modules=2,
        max_tool_calls=1,
        max_reasoning_depth=2,
    )


@pytest.fixture
def fixed_id() -> UUID:
    return UUID('12345678-1234-5678-9234-567812345678')


@pytest.fixture
def aware_time() -> datetime:
    return datetime(2026, 9, 16, 8, 0, tzinfo=timezone.utc)
