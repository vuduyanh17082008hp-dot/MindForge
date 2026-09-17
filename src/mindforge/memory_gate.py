from __future__ import annotations

from datetime import datetime, timezone
from enum import Enum

from pydantic import BaseModel, Field


class MemoryDecision(str, Enum):
    USE = "USE"
    CONTEXTUALIZE = "CONTEXTUALIZE"
    VERIFY = "VERIFY"
    QUARANTINE = "QUARANTINE"
    REJECT = "REJECT"


class MemoryCandidate(BaseModel):
    memory_id: str
    domain: str
    scope: str
    status: str
    provenance: str | None = None
    created_at: datetime
    last_verified_at: datetime | None = None
    expires_at: datetime | None = None
    contradicted_by_current_evidence: bool = False
    reliability: float = Field(default=0.5, ge=0.0, le=1.0)


class MemoryContext(BaseModel):
    domain: str
    scope: str
    minimum_reliability: float = Field(default=0.5, ge=0.0, le=1.0)
    high_stakes: bool = False


class MemoryGateResult(BaseModel):
    decision: MemoryDecision
    reasons: tuple[str, ...]


class ReconstructiveMemoryGate:
    def evaluate(
        self,
        candidate: MemoryCandidate,
        context: MemoryContext,
    ) -> MemoryGateResult:
        now = datetime.now(timezone.utc)

        if candidate.status in {"REJECTED", "INVALIDATED"}:
            return MemoryGateResult(
                decision=MemoryDecision.REJECT,
                reasons=("memory status prohibits reuse",),
            )
        if candidate.expires_at is not None and candidate.expires_at <= now:
            return MemoryGateResult(
                decision=MemoryDecision.QUARANTINE,
                reasons=("memory expired",),
            )
        if candidate.contradicted_by_current_evidence:
            return MemoryGateResult(
                decision=MemoryDecision.VERIFY if context.high_stakes
                else MemoryDecision.QUARANTINE,
                reasons=("current evidence contradicts retrieved memory",),
            )
        if candidate.provenance is None:
            return MemoryGateResult(
                decision=MemoryDecision.VERIFY,
                reasons=("missing provenance",),
            )
        if candidate.reliability < context.minimum_reliability:
            return MemoryGateResult(
                decision=MemoryDecision.VERIFY,
                reasons=("reliability below policy threshold",),
            )
        if candidate.domain != context.domain:
            return MemoryGateResult(
                decision=MemoryDecision.REJECT,
                reasons=("domain mismatch",),
            )
        if candidate.scope != context.scope:
            return MemoryGateResult(
                decision=MemoryDecision.CONTEXTUALIZE,
                reasons=("scope mismatch",),
            )
        return MemoryGateResult(
            decision=MemoryDecision.USE,
            reasons=("memory satisfies current constraints",),
        )
