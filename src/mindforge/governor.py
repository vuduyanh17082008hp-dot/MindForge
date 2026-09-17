from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class GovernorDecision(str, Enum):
    ALLOW_FAST = "ALLOW_FAST"
    ALLOW_DEEP = "ALLOW_DEEP"
    REQUIRE_CLARIFICATION = "REQUIRE_CLARIFICATION"
    REQUIRE_RETRIEVAL = "REQUIRE_RETRIEVAL"
    REQUIRE_VERIFICATION = "REQUIRE_VERIFICATION"
    ABSTAIN = "ABSTAIN"
    BLOCK = "BLOCK"


class GovernorInput(BaseModel):
    task_risk: float = Field(ge=0.0, le=1.0)
    evidence_sufficiency: float = Field(ge=0.0, le=1.0)
    competence_score: float | None = Field(default=None, ge=0.0, le=1.0)
    competence_mature: bool = False
    unresolved_contradictions: int = Field(default=0, ge=0)
    budget_remaining_usd: float = Field(ge=0.0)
    estimated_fast_cost_usd: float = Field(ge=0.0)
    estimated_deep_cost_usd: float = Field(ge=0.0)
    retrieval_available: bool = True
    verification_available: bool = True
    safety_block: bool = False
    hard_policy_violation: bool = False


class GovernorResult(BaseModel):
    decision: GovernorDecision
    reasons: tuple[str, ...]


class ExternalMetacognitiveGovernor:
    """Small deterministic policy engine; thresholds are versioned policy."""

    def __init__(
        self,
        *,
        high_risk_threshold: float = 0.80,
        low_risk_threshold: float = 0.30,
        sufficient_evidence_threshold: float = 0.75,
        fast_competence_threshold: float = 0.75,
    ) -> None:
        self.high_risk_threshold = high_risk_threshold
        self.low_risk_threshold = low_risk_threshold
        self.sufficient_evidence_threshold = sufficient_evidence_threshold
        self.fast_competence_threshold = fast_competence_threshold

    def evaluate(self, state: GovernorInput) -> GovernorResult:
        if state.safety_block or state.hard_policy_violation:
            return GovernorResult(
                decision=GovernorDecision.BLOCK,
                reasons=("hard safety or policy constraint",),
            )

        if (
            state.task_risk >= self.high_risk_threshold
            and state.evidence_sufficiency < self.sufficient_evidence_threshold
        ):
            if state.verification_available:
                return GovernorResult(
                    decision=GovernorDecision.REQUIRE_VERIFICATION,
                    reasons=("high-risk task", "insufficient evidence"),
                )
            return GovernorResult(
                decision=GovernorDecision.ABSTAIN,
                reasons=("high-risk task", "verification unavailable"),
            )

        if state.unresolved_contradictions > 0:
            if state.verification_available:
                return GovernorResult(
                    decision=GovernorDecision.REQUIRE_VERIFICATION,
                    reasons=("unresolved contradiction",),
                )
            return GovernorResult(
                decision=GovernorDecision.ALLOW_DEEP,
                reasons=("unresolved contradiction requires deeper analysis",),
            )

        if state.evidence_sufficiency < self.sufficient_evidence_threshold:
            if state.retrieval_available:
                return GovernorResult(
                    decision=GovernorDecision.REQUIRE_RETRIEVAL,
                    reasons=("evidence insufficient",),
                )
            return GovernorResult(
                decision=GovernorDecision.REQUIRE_CLARIFICATION,
                reasons=("evidence insufficient and retrieval unavailable",),
            )

        if state.budget_remaining_usd < state.estimated_fast_cost_usd:
            return GovernorResult(
                decision=GovernorDecision.ABSTAIN,
                reasons=("insufficient minimum execution budget",),
            )

        competence_known = (
            state.competence_score is not None and state.competence_mature
        )
        if (
            competence_known
            and state.competence_score >= self.fast_competence_threshold
            and state.task_risk <= self.low_risk_threshold
        ):
            return GovernorResult(
                decision=GovernorDecision.ALLOW_FAST,
                reasons=("low risk", "mature empirical competence"),
            )

        if state.budget_remaining_usd >= state.estimated_deep_cost_usd:
            return GovernorResult(
                decision=GovernorDecision.ALLOW_DEEP,
                reasons=("FAST authority not established",),
            )

        return GovernorResult(
            decision=GovernorDecision.ALLOW_FAST,
            reasons=("DEEP exceeds budget; FAST is the remaining safe route",),
        )
