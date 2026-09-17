from datetime import datetime, timedelta, timezone
from uuid import uuid4

import pytest

from mindforge.prediction_ledger import (
    PredictionCreated,
    PredictionLedgerManager,
    PredictionStatus,
)


def make_prediction(probability: float = 0.8) -> PredictionCreated:
    return PredictionCreated(
        user_id=uuid4(),
        task_id="recursion-001",
        context_manifest_id=uuid4(),
        actor_id="test-model",
        actor_version="v1",
        human_model_version=1,
        target="independent_success",
        predicted_probability=probability,
        uncertainty=0.1,
        evidence_quality=0.9,
        expires_at=datetime.now(timezone.utc) + timedelta(minutes=10),
    )


def test_resolved_prediction_calculates_brier():
    manager = PredictionLedgerManager(primary_attribution_threshold=0.8)
    prediction = make_prediction(0.8)

    result = manager.resolve(
        prediction=prediction,
        outcome=1.0,
        attribution_confidence=0.95,
    )

    assert result.status is PredictionStatus.RESOLVED
    assert result.brier_contribution == pytest.approx(0.04)
    assert result.log_loss_contribution is not None


def test_low_attribution_does_not_enter_primary_resolution():
    manager = PredictionLedgerManager(primary_attribution_threshold=0.8)
    prediction = make_prediction()

    result = manager.resolve(
        prediction=prediction,
        outcome=1.0,
        attribution_confidence=0.4,
    )

    assert result.status is PredictionStatus.CONTAMINATED
    assert result.brier_contribution is None
