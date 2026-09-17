from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum
from math import log
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field


class PredictionStatus(str, Enum):
    PENDING = "PENDING"
    RESOLVED = "RESOLVED"
    EXPIRED = "EXPIRED"
    UNOBSERVABLE = "UNOBSERVABLE"
    CONTAMINATED = "CONTAMINATED"
    INVALIDATED = "INVALIDATED"


class PredictionCreated(BaseModel):
    model_config = ConfigDict(frozen=True)

    prediction_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    task_id: str
    attempt_id: UUID | None = None
    action_id: UUID | None = None
    context_manifest_id: UUID
    actor_id: str
    actor_version: str
    human_model_version: int = Field(ge=0)
    target: str
    predicted_probability: float = Field(ge=0.0, le=1.0)
    uncertainty: float = Field(ge=0.0)
    evidence_quality: float = Field(ge=0.0, le=1.0)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    expires_at: datetime
    status: PredictionStatus = PredictionStatus.PENDING


class PredictionResolved(BaseModel):
    model_config = ConfigDict(frozen=True)

    resolution_id: UUID = Field(default_factory=uuid4)
    prediction_id: UUID
    status: PredictionStatus
    observed_outcome: float | None = Field(default=None, ge=0.0, le=1.0)
    attribution_confidence: float = Field(ge=0.0, le=1.0)
    brier_contribution: float | None = None
    log_loss_contribution: float | None = None
    resolved_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    reason: str


class PredictionLedgerManager:
    def __init__(
        self,
        *,
        primary_attribution_threshold: float = 0.80,
        epsilon: float = 1e-12,
    ) -> None:
        if not 0.0 <= primary_attribution_threshold <= 1.0:
            raise ValueError("primary_attribution_threshold must be in [0, 1]")
        self.primary_attribution_threshold = primary_attribution_threshold
        self.epsilon = epsilon

    def resolve(
        self,
        *,
        prediction: PredictionCreated,
        outcome: float | None,
        attribution_confidence: float,
        observable: bool = True,
        contaminated: bool = False,
        now: datetime | None = None,
    ) -> PredictionResolved:
        now = now or datetime.now(timezone.utc)

        if contaminated:
            return PredictionResolved(
                prediction_id=prediction.prediction_id,
                status=PredictionStatus.CONTAMINATED,
                attribution_confidence=attribution_confidence,
                reason="ambiguous intervention contaminated attribution",
            )
        if not observable:
            return PredictionResolved(
                prediction_id=prediction.prediction_id,
                status=PredictionStatus.UNOBSERVABLE,
                attribution_confidence=attribution_confidence,
                reason="outcome not reliably observable",
            )
        if now > prediction.expires_at:
            return PredictionResolved(
                prediction_id=prediction.prediction_id,
                status=PredictionStatus.EXPIRED,
                attribution_confidence=attribution_confidence,
                reason="outcome outside prediction validity window",
            )
        if outcome is None:
            raise ValueError("outcome is required for a resolved prediction")
        if attribution_confidence < self.primary_attribution_threshold:
            return PredictionResolved(
                prediction_id=prediction.prediction_id,
                status=PredictionStatus.CONTAMINATED,
                observed_outcome=outcome,
                attribution_confidence=attribution_confidence,
                reason="attribution below primary-analysis threshold",
            )

        p = prediction.predicted_probability
        clipped_p = min(1.0 - self.epsilon, max(self.epsilon, p))
        brier = (p - outcome) ** 2
        log_loss = -(
            outcome * log(clipped_p)
            + (1.0 - outcome) * log(1.0 - clipped_p)
        )
        return PredictionResolved(
            prediction_id=prediction.prediction_id,
            status=PredictionStatus.RESOLVED,
            observed_outcome=outcome,
            attribution_confidence=attribution_confidence,
            brier_contribution=brier,
            log_loss_contribution=log_loss,
            reason="resolved with sufficient attribution confidence",
        )
