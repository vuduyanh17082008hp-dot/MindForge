from __future__ import annotations

from datetime import timedelta
from typing import Any

import pytest

from mindforge.contracts import (
    ArtifactReference,
    ArtifactType,
    Belief,
    CognitiveBudget,
    CognitiveRoute,
    ContextCapsule,
    EpistemicStatus,
    Evidence,
    Hypothesis,
    Observation,
    ObservationKind,
    Outcome,
    Prediction,
    PredictionError,
    PredictionErrorType,
    Provenance,
    RouteMode,
)


def build_models(provenance: Provenance, budget: CognitiveBudget) -> list[Any]:
    observation = Observation(
        provenance=provenance,
        kind=ObservationKind.USER_CLAIM,
        content='I prefer examples before definitions.',
        epistemic_status=EpistemicStatus.REPORTED,
    )
    evidence = Evidence(
        provenance=provenance,
        content='The learner completed the example correctly.',
        reliability=0.75,
        observation_ids=[observation.id],
    )
    belief = Belief(
        provenance=provenance,
        proposition='Examples may currently support understanding.',
        confidence=0.6,
        supporting_evidence_ids=[evidence.id],
    )
    hypothesis = Hypothesis(
        provenance=provenance,
        claim='Examples reduce initial ambiguity in this context.',
        confidence=0.55,
        evidence_for=[evidence.id],
    )
    prediction = Prediction(
        provenance=provenance,
        target='next exercise',
        expected_outcome='The learner completes the first step.',
        confidence=0.65,
        horizon=timedelta(minutes=15),
    )
    outcome = Outcome(
        provenance=provenance,
        prediction_id=prediction.id,
        observed_result='The learner completed the first step.',
    )
    prediction_error = PredictionError(
        provenance=provenance,
        error_type=PredictionErrorType.OUTCOME,
        prediction_id=prediction.id,
        outcome_id=outcome.id,
        description='Example error artifact for round-trip coverage.',
    )
    capsule = ContextCapsule(
        current_goal='Prepare the next explanation.',
        relevant_observations=[
            ArtifactReference(
                artifact_id=observation.id,
                artifact_type=ArtifactType.OBSERVATION,
            )
        ],
        provenance=provenance,
        budget=budget,
    )
    route = CognitiveRoute(
        mode=RouteMode.FAST,
        selected_modules=['response.compose'],
    )
    return [
        observation,
        evidence,
        belief,
        hypothesis,
        prediction,
        outcome,
        prediction_error,
        capsule,
        budget,
        route,
    ]


def test_major_models_round_trip_without_semantic_type_loss(
    provenance: Provenance, budget: CognitiveBudget
) -> None:
    for model in build_models(provenance, budget):
        restored = type(model).model_validate_json(model.model_dump_json())
        assert type(restored) is type(model)
        assert restored == model

    restored_observation = Observation.model_validate_json(
        build_models(provenance, budget)[0].model_dump_json()
    )
    assert restored_observation.kind is ObservationKind.USER_CLAIM
    assert restored_observation.epistemic_status is EpistemicStatus.REPORTED

