"""Shared primitives for MindForge cognitive data contracts."""

from __future__ import annotations

from datetime import datetime, timezone
from enum import StrEnum
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    JsonValue,
    field_validator,
    model_validator,
)


def utc_now() -> datetime:
    """Return an aware UTC timestamp."""

    return datetime.now(timezone.utc)


def normalize_utc(value: datetime) -> datetime:
    """Reject naive datetimes and normalize aware values to UTC."""

    if value.tzinfo is None or value.utcoffset() is None:
        raise ValueError("timestamps must be timezone-aware")
    return value.astimezone(timezone.utc)


class MindForgeModel(BaseModel):
    """Strict base model used by all public contracts."""

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
    )


class ProvenanceKind(StrEnum):
    USER = "user"
    SYSTEM = "system"
    TOOL = "tool"
    EXTERNAL_SOURCE = "external_source"
    MEMORY = "memory"
    DERIVED_INFERENCE = "derived_inference"


class Scope(StrEnum):
    TURN = "turn"
    SESSION = "session"
    PERSISTENT = "persistent"
    EXTERNAL = "external"


class ArtifactType(StrEnum):
    OBSERVATION = "observation"
    EVIDENCE = "evidence"
    BELIEF = "belief"
    HYPOTHESIS = "hypothesis"
    PREDICTION = "prediction"
    OUTCOME = "outcome"
    PREDICTION_ERROR = "prediction_error"


class Provenance(MindForgeModel):
    """Traceable origin metadata; provenance is not a truth assertion."""

    kind: ProvenanceKind
    source_id: str | None = Field(default=None, min_length=1, max_length=256)
    reference: str | None = Field(default=None, min_length=1, max_length=2048)
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class ArtifactReference(MindForgeModel):
    """A typed reference to another cognitive artifact."""

    artifact_id: UUID
    artifact_type: ArtifactType


class MemoryReference(MindForgeModel):
    """Opaque reference to a versioned memory record."""

    reference: str = Field(min_length=1, max_length=512)
    version: str | None = Field(default=None, min_length=1, max_length=128)


class CognitiveArtifact(MindForgeModel):
    """Common identity, lifecycle, provenance, and scope metadata."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=utc_now)
    provenance: Provenance
    scope: Scope = Scope.TURN
    revisable: bool = True
    expires_at: datetime | None = None
    tags: set[str] = Field(default_factory=set)

    @field_validator("created_at", "expires_at")
    @classmethod
    def timestamps_are_aware_utc(cls, value: datetime | None) -> datetime | None:
        if value is None:
            return None
        return normalize_utc(value)

    @field_validator("tags")
    @classmethod
    def tags_are_non_empty(cls, value: set[str]) -> set[str]:
        if any(not tag.strip() for tag in value):
            raise ValueError("tags must not be empty")
        return value

    @model_validator(mode="after")
    def expiry_follows_creation(self) -> CognitiveArtifact:
        if self.expires_at is not None and self.expires_at <= self.created_at:
            raise ValueError("expires_at must be later than created_at")
        return self
