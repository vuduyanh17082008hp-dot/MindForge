"""Turn context, prediction, outcome, and prediction-error contracts."""

from __future__ import annotations

from datetime import datetime, timedelta
from enum import StrEnum
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import Field, JsonValue, field_validator, model_validator

from mindforge.contracts.base import (
    ArtifactReference,
    ArtifactType,
    CognitiveArtifact,
    MemoryReference,
    MindForgeModel,
    Provenance,
    normalize_utc,
    utc_now,
)
from mindforge.contracts.epistemics import CalibrationStatus, EpistemicStatus
from mindforge.contracts.routing import CognitiveBudget

UnitInterval = Annotated[float, Field(ge=0.0, le=1.0)]


class PredictionStatus(StrEnum):
    OPEN = "open"
    RESOLVED = "resolved"
    EXPIRED = "expired"
    CANCELLED = "cancelled"


class PredictionErrorType(StrEnum):
    OUTCOME = "outcome"
    STRUCTURAL = "structural"


class UncertaintyLevel(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class UncertaintySummary(MindForgeModel):
    """Qualitative uncertainty statement, separate from confidence."""

    level: UncertaintyLevel
    description: str = Field(min_length=1)
    unresolved_questions: list[str] = Field(default_factory=list)


class AttributionCandidate(MindForgeModel):
    """A possible contributor to error, not a proven cause."""

    component_id: str = Field(min_length=1, max_length=128)
    rationale: str = Field(min_length=1)
    confidence: UnitInterval | None = None


class Prediction(CognitiveArtifact):
    """An expected future observation or outcome; never a truth assertion."""

    target: str = Field(min_length=1)
    expected_outcome: str = Field(min_length=1)
    confidence: UnitInterval
    horizon: timedelta = Field(gt=timedelta(0))
    context: dict[str, JsonValue] = Field(default_factory=dict)
    status: PredictionStatus = PredictionStatus.OPEN
    epistemic_status: EpistemicStatus = EpistemicStatus.PREDICTED
    calibration_status: CalibrationStatus = CalibrationStatus.UNASSESSED

    @model_validator(mode="after")
    def status_is_predictive(self) -> Prediction:
        if self.epistemic_status is not EpistemicStatus.PREDICTED:
            raise ValueError("a prediction must retain predicted epistemic status")
        return self


class Outcome(CognitiveArtifact):
    """A later observation; it does not explain why a prediction succeeded or failed."""

    prediction_id: UUID | None = None
    observed_result: str = Field(min_length=1)
    observed_at: datetime = Field(default_factory=utc_now)
    evidence_ids: list[UUID] = Field(default_factory=list)

    @field_validator("observed_at")
    @classmethod
    def observed_at_is_aware_utc(cls, value: datetime) -> datetime:
        return normalize_utc(value)


class PredictionError(CognitiveArtifact):
    """A recorded mismatch or suspected structural fault."""

    error_type: PredictionErrorType
    prediction_id: UUID
    outcome_id: UUID | None = None
    description: str = Field(min_length=1)
    magnitude: UnitInterval | None = None
    attribution_candidates: list[AttributionCandidate] = Field(default_factory=list)


class ContextCapsule(MindForgeModel):
    """Curated turn context, intentionally smaller than persistent history."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    current_goal: str = Field(min_length=1)
    relevant_observations: list[ArtifactReference] = Field(default_factory=list)
    relevant_evidence: list[ArtifactReference] = Field(default_factory=list)
    relevant_beliefs: list[ArtifactReference] = Field(default_factory=list)
    relevant_hypotheses: list[ArtifactReference] = Field(default_factory=list)
    relevant_predictions: list[ArtifactReference] = Field(default_factory=list)
    retrieved_memory_references: list[MemoryReference] = Field(default_factory=list)
    human_model_version: str | None = Field(default=None, min_length=1, max_length=128)
    common_ground_session_reference: str | None = Field(
        default=None, min_length=1, max_length=512
    )
    uncertainty_summary: UncertaintySummary | None = None
    provenance: Provenance
    budget: CognitiveBudget

    @field_validator("created_at")
    @classmethod
    def created_at_is_aware_utc(cls, value: datetime) -> datetime:
        return normalize_utc(value)

    @model_validator(mode="after")
    def reference_types_match_fields(self) -> ContextCapsule:
        expected_types = {
            "relevant_observations": ArtifactType.OBSERVATION,
            "relevant_evidence": ArtifactType.EVIDENCE,
            "relevant_beliefs": ArtifactType.BELIEF,
            "relevant_hypotheses": ArtifactType.HYPOTHESIS,
            "relevant_predictions": ArtifactType.PREDICTION,
        }
        for field_name, expected_type in expected_types.items():
            references = getattr(self, field_name)
            if any(reference.artifact_type is not expected_type for reference in references):
                raise ValueError(f"{field_name} must contain only {expected_type.value} references")
        return self
