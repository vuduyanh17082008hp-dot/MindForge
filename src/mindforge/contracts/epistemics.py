"""Contracts that keep epistemic categories explicit and revisable."""

from __future__ import annotations

from enum import StrEnum
from typing import Annotated
from uuid import UUID

from pydantic import Field, model_validator

from mindforge.contracts.base import CognitiveArtifact

UnitInterval = Annotated[float, Field(ge=0.0, le=1.0)]


class ObservationKind(StrEnum):
    USER_CLAIM = "user_claim"
    SYSTEM_OBSERVATION = "system_observation"
    TOOL_RESULT = "tool_result"
    EXTERNAL_SOURCE = "external_source"


class EpistemicStatus(StrEnum):
    OBSERVED = "observed"
    REPORTED = "reported"
    INFERRED = "inferred"
    HYPOTHESIZED = "hypothesized"
    PREDICTED = "predicted"
    UNKNOWN = "unknown"


class EvidenceQuality(StrEnum):
    UNKNOWN = "unknown"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class CalibrationStatus(StrEnum):
    UNASSESSED = "unassessed"
    CALIBRATED = "calibrated"
    MISCALIBRATED = "miscalibrated"
    INSUFFICIENT_DATA = "insufficient_data"


class HypothesisStatus(StrEnum):
    ACTIVE = "active"
    SUPPORTED = "supported"
    WEAKENED = "weakened"
    FALSIFIED = "falsified"
    RETIRED = "retired"


class Observation(CognitiveArtifact):
    """Something observed or reported, without any verified-truth claim."""

    kind: ObservationKind
    content: str = Field(min_length=1)
    epistemic_status: EpistemicStatus

    @model_validator(mode="after")
    def status_is_observational(self) -> Observation:
        allowed = {
            EpistemicStatus.OBSERVED,
            EpistemicStatus.REPORTED,
            EpistemicStatus.UNKNOWN,
        }
        if self.epistemic_status not in allowed:
            raise ValueError("an observation must be observed, reported, or unknown")
        if (
            self.kind is ObservationKind.USER_CLAIM
            and self.epistemic_status is not EpistemicStatus.REPORTED
        ):
            raise ValueError("a user claim must have reported epistemic status")
        return self


class Evidence(CognitiveArtifact):
    """Material offered in support of or against propositions."""

    content: str = Field(min_length=1)
    reliability: UnitInterval
    quality: EvidenceQuality = EvidenceQuality.UNKNOWN
    observation_ids: list[UUID] = Field(default_factory=list)
    supports: list[str] = Field(default_factory=list)
    contradicts: list[str] = Field(default_factory=list)


class Belief(CognitiveArtifact):
    """A revisable proposition held by the system, never a fact marker."""

    proposition: str = Field(min_length=1)
    confidence: UnitInterval
    supporting_evidence_ids: list[UUID] = Field(default_factory=list)
    contradicting_evidence_ids: list[UUID] = Field(default_factory=list)
    epistemic_status: EpistemicStatus = EpistemicStatus.INFERRED
    calibration_status: CalibrationStatus = CalibrationStatus.UNASSESSED

    @model_validator(mode="after")
    def status_is_belief_appropriate(self) -> Belief:
        if self.epistemic_status not in {
            EpistemicStatus.INFERRED,
            EpistemicStatus.UNKNOWN,
        }:
            raise ValueError("a belief must be inferred or unknown")
        return self


class Hypothesis(CognitiveArtifact):
    """A candidate explanation with explicit possible falsifiers."""

    claim: str = Field(min_length=1)
    confidence: UnitInterval
    estimated_probability: UnitInterval | None = None
    evidence_for: list[UUID] = Field(default_factory=list)
    evidence_against: list[UUID] = Field(default_factory=list)
    falsifiers: list[str] = Field(default_factory=list)
    predicted_observations: list[str] = Field(default_factory=list)
    status: HypothesisStatus = HypothesisStatus.ACTIVE
    epistemic_status: EpistemicStatus = EpistemicStatus.HYPOTHESIZED

    @model_validator(mode="after")
    def status_is_hypothetical(self) -> Hypothesis:
        if self.epistemic_status is not EpistemicStatus.HYPOTHESIZED:
            raise ValueError("a hypothesis must retain hypothesized epistemic status")
        return self

