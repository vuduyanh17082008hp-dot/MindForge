from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError

from mindforge.contracts import (
    ArtifactReference,
    ArtifactType,
    CognitiveBudget,
    ContextCapsule,
    Outcome,
    Prediction,
    PredictionError,
    PredictionErrorType,
    Provenance,
    UncertaintyLevel,
    UncertaintySummary,
)


@pytest.mark.parametrize('confidence', [-0.01, 1.01])
def test_prediction_rejects_invalid_confidence(
    provenance: Provenance, confidence: float
) -> None:
    with pytest.raises(ValidationError):
        Prediction(
            provenance=provenance,
            target='next response',
            expected_outcome='The learner asks for an example.',
            confidence=confidence,
            horizon=timedelta(minutes=5),
        )


def test_prediction_requires_positive_horizon(provenance: Provenance) -> None:
    with pytest.raises(ValidationError):
        Prediction(
            provenance=provenance,
            target='next response',
            expected_outcome='A question is asked.',
            confidence=0.5,
            horizon=timedelta(0),
        )


def test_prediction_error_types_remain_separate(provenance: Provenance) -> None:
    prediction_id = uuid4()
    outcome_error = PredictionError(
        provenance=provenance,
        error_type=PredictionErrorType.OUTCOME,
        prediction_id=prediction_id,
        description='The observed result differed from the expected result.',
    )
    structural_error = PredictionError(
        provenance=provenance,
        error_type=PredictionErrorType.STRUCTURAL,
        prediction_id=prediction_id,
        description='The represented state may omit a relevant distinction.',
    )

    assert outcome_error.error_type is PredictionErrorType.OUTCOME
    assert structural_error.error_type is PredictionErrorType.STRUCTURAL
    assert outcome_error.error_type is not structural_error.error_type


def test_context_capsule_holds_typed_references_without_full_history(
    provenance: Provenance,
    budget: CognitiveBudget,
    fixed_id: UUID,
) -> None:
    capsule = ContextCapsule(
        current_goal='Explain a concept using one relevant example.',
        relevant_observations=[
            ArtifactReference(
                artifact_id=fixed_id,
                artifact_type=ArtifactType.OBSERVATION,
            )
        ],
        uncertainty_summary=UncertaintySummary(
            level=UncertaintyLevel.MEDIUM,
            description='Only one relevant observation is available.',
        ),
        provenance=provenance,
        budget=budget,
    )

    assert capsule.relevant_observations[0].artifact_id == fixed_id
    assert capsule.relevant_observations[0].artifact_type is ArtifactType.OBSERVATION
    assert 'full_history' not in ContextCapsule.model_fields
    assert capsule.relevant_evidence == []


def test_context_capsule_rejects_reference_in_wrong_category(
    provenance: Provenance,
    budget: CognitiveBudget,
    fixed_id: UUID,
) -> None:
    with pytest.raises(ValidationError):
        ContextCapsule(
            current_goal='Use only relevant context.',
            relevant_observations=[
                ArtifactReference(
                    artifact_id=fixed_id,
                    artifact_type=ArtifactType.BELIEF,
                )
            ],
            provenance=provenance,
            budget=budget,
        )


def test_aware_timestamp_is_normalized_to_utc(provenance: Provenance) -> None:
    plus_eight = timezone(timedelta(hours=8))
    prediction = Prediction(
        provenance=provenance,
        created_at=datetime(2026, 9, 16, 16, 0, tzinfo=plus_eight),
        target='next response',
        expected_outcome='The user requests a second example.',
        confidence=0.5,
        horizon=timedelta(minutes=10),
    )

    assert prediction.created_at == datetime(2026, 9, 16, 8, 0, tzinfo=timezone.utc)
    assert prediction.created_at.utcoffset() == timedelta(0)


def test_naive_timestamp_is_rejected(provenance: Provenance) -> None:
    with pytest.raises(ValidationError):
        Outcome(
            provenance=provenance,
            observed_result='A later observation.',
            observed_at=datetime(2026, 9, 16, 8, 0),
        )


def test_expiry_must_follow_creation(provenance: Provenance) -> None:
    created_at = datetime(2026, 9, 16, 8, 0, tzinfo=timezone.utc)
    with pytest.raises(ValidationError):
        Outcome(
            provenance=provenance,
            created_at=created_at,
            expires_at=created_at,
            observed_result='An observation.',
        )

