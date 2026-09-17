"""Empirical competence-boundary contracts for MindForge."""

from __future__ import annotations

from math import sqrt

from pydantic import ConfigDict, Field

from mindforge.contracts.base import MindForgeModel


class CompetenceProfile(MindForgeModel):
    """
    Empirical performance estimate for one actor/task configuration.

    This is task-scoped evidence about historical performance, not a universal
    intelligence or capability score.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )

    actor_id: str = Field(min_length=1, max_length=256)
    actor_version: str = Field(min_length=1, max_length=128)

    task_class: str = Field(min_length=1, max_length=256)
    domain: str = Field(min_length=1, max_length=128)
    tool_config_hash: str = Field(min_length=64, max_length=64)

    alpha: float = Field(default=1.0, gt=0.0)
    beta: float = Field(default=1.0, gt=0.0)

    total_evaluated: int = Field(default=0, ge=0)
    confident_failures: int = Field(default=0, ge=0)

    @property
    def posterior_mean(self) -> float:
        return self.alpha / (self.alpha + self.beta)

    @property
    def posterior_variance(self) -> float:
        alpha = self.alpha
        beta = self.beta

        return (
            alpha * beta
            / (
                ((alpha + beta) ** 2)
                * (alpha + beta + 1.0)
            )
        )

    @property
    def posterior_std(self) -> float:
        return sqrt(self.posterior_variance)

    def conservative_score(self, z: float = 1.0) -> float:
        """
        Return a conservative routing heuristic.

        This is not claimed to be an exact Bayesian credible lower bound.
        """

        if z < 0.0:
            raise ValueError("z must be non-negative")

        return max(
            0.0,
            self.posterior_mean - z * self.posterior_std,
        )

    def is_mature(self, *, min_evaluated: int) -> bool:
        """
        Return whether this profile meets a caller-defined evidence threshold.

        min_evaluated is a policy parameter, not a scientific constant.
        """

        if min_evaluated < 1:
            raise ValueError("min_evaluated must be at least 1")

        return self.total_evaluated >= min_evaluated

    def record_outcome(
        self,
        *,
        success: bool,
        evidence_weight: float = 1.0,
        confident_failure: bool = False,
    ) -> "CompetenceProfile":
        """
        Return an updated immutable competence profile.

        Fractional evidence weights are interpreted as weighted pseudo-counts.
        """

        if not 0.0 <= evidence_weight <= 1.0:
            raise ValueError("evidence_weight must be in [0, 1]")

        if success and confident_failure:
            raise ValueError(
                "confident_failure cannot be true for a successful outcome"
            )

        return self.model_copy(
            update={
                "alpha": (
                    self.alpha
                    + (evidence_weight if success else 0.0)
                ),
                "beta": (
                    self.beta
                    + (evidence_weight if not success else 0.0)
                ),
                "total_evaluated": self.total_evaluated + 1,
                "confident_failures": (
                    self.confident_failures
                    + int((not success) and confident_failure)
                ),
            }
        )
