from __future__ import annotations

from uuid import uuid4

import pytest
from pydantic import ValidationError

from mindforge.contracts import (
    Belief,
    EpistemicStatus,
    Evidence,
    EvidenceQuality,
    Hypothesis,
    Observation,
    ObservationKind,
    Provenance,
)


def test_user_claim_is_reported_observation_without_fact_marker(
    provenance: Provenance,
) -> None:
    observation = Observation(
        provenance=provenance,
        kind=ObservationKind.USER_CLAIM,
        content='I always learn better visually.',
        epistemic_status=EpistemicStatus.REPORTED,
    )

    assert observation.kind is ObservationKind.USER_CLAIM
    assert observation.epistemic_status is EpistemicStatus.REPORTED
    assert 'fact' not in Observation.model_fields
    assert 'is_true' not in Observation.model_fields


def test_user_claim_cannot_be_marked_observed(provenance: Provenance) -> None:
    with pytest.raises(ValidationError):
        Observation(
            provenance=provenance,
            kind=ObservationKind.USER_CLAIM,
            content='I prefer short examples.',
            epistemic_status=EpistemicStatus.OBSERVED,
        )


@pytest.mark.parametrize('reliability', [0.0, 1.0])
def test_evidence_accepts_reliability_boundaries(
    provenance: Provenance, reliability: float
) -> None:
    evidence = Evidence(
        provenance=provenance,
        content='A bounded observation.',
        reliability=reliability,
        quality=EvidenceQuality.UNKNOWN,
    )
    assert evidence.reliability == reliability


@pytest.mark.parametrize('reliability', [-0.01, 1.01])
def test_evidence_rejects_reliability_outside_unit_interval(
    provenance: Provenance, reliability: float
) -> None:
    with pytest.raises(ValidationError):
        Evidence(
            provenance=provenance,
            content='An invalid reliability value.',
            reliability=reliability,
        )


@pytest.mark.parametrize('confidence', [-0.01, 1.01])
def test_belief_rejects_invalid_confidence(
    provenance: Provenance, confidence: float
) -> None:
    with pytest.raises(ValidationError):
        Belief(
            provenance=provenance,
            proposition='A revisable proposition.',
            confidence=confidence,
        )


@pytest.mark.parametrize('confidence', [-0.01, 1.01])
def test_hypothesis_rejects_invalid_confidence(
    provenance: Provenance, confidence: float
) -> None:
    with pytest.raises(ValidationError):
        Hypothesis(
            provenance=provenance,
            claim='A candidate explanation.',
            confidence=confidence,
        )


def test_hypothesis_keeps_evidence_for_and_against_distinct(
    provenance: Provenance,
) -> None:
    supporting_id = uuid4()
    contradicting_id = uuid4()
    hypothesis = Hypothesis(
        provenance=provenance,
        claim='Worked examples improve recall in this context.',
        confidence=0.6,
        evidence_for=[supporting_id],
        evidence_against=[contradicting_id],
    )

    assert hypothesis.evidence_for == [supporting_id]
    assert hypothesis.evidence_against == [contradicting_id]
    assert hypothesis.evidence_for != hypothesis.evidence_against


def test_hypothesis_probability_does_not_replace_confidence(
    provenance: Provenance,
) -> None:
    hypothesis = Hypothesis(
        provenance=provenance,
        claim='A candidate explanation.',
        confidence=0.3,
        estimated_probability=0.8,
    )

    assert hypothesis.confidence == 0.3
    assert hypothesis.estimated_probability == 0.8


def test_unknown_fields_are_rejected(provenance: Provenance) -> None:
    with pytest.raises(ValidationError):
        Observation(
            provenance=provenance,
            kind=ObservationKind.SYSTEM_OBSERVATION,
            content='A measured event.',
            epistemic_status=EpistemicStatus.OBSERVED,
            is_true=True,
        )

