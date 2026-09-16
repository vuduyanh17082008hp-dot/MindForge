"""Resource-budget and route-decision contracts; no execution logic."""

from __future__ import annotations

from enum import StrEnum

from pydantic import Field, field_validator

from mindforge.contracts.base import MindForgeModel


class RouteMode(StrEnum):
    FAST = "fast"
    DEEP = "deep"


class RouteReasonCode(StrEnum):
    LOW_COMPLEXITY = "low_complexity"
    HIGH_STAKES = "high_stakes"
    AMBIGUITY = "ambiguity"
    VERIFICATION_NEEDED = "verification_needed"
    USER_REQUEST = "user_request"
    RESOURCE_LIMIT = "resource_limit"
    NOVELTY = "novelty"


class CognitiveBudget(MindForgeModel):
    """Explicit finite bounds available to cognition for one routed unit."""

    max_latency_ms: int = Field(gt=0, strict=True)
    max_model_calls: int = Field(ge=0, strict=True)
    max_tokens: int = Field(ge=0, strict=True)
    max_parallel_modules: int = Field(gt=0, strict=True)
    max_tool_calls: int = Field(ge=0, strict=True)
    max_reasoning_depth: int = Field(ge=0, strict=True)


class CognitiveRoute(MindForgeModel):
    """A domain-agnostic route decision that does not execute cognition."""

    mode: RouteMode
    selected_modules: list[str] = Field(default_factory=list)
    reason_codes: list[RouteReasonCode] = Field(default_factory=list)
    reasons: list[str] = Field(default_factory=list)
    requires_calibration: bool = False
    requires_verification: bool = False
    requires_human_clarification: bool = False

    @field_validator("selected_modules")
    @classmethod
    def modules_are_domain_agnostic_identifiers(cls, value: list[str]) -> list[str]:
        if len(value) != len(set(value)):
            raise ValueError("selected_modules must not contain duplicates")
        for module_id in value:
            if not module_id or len(module_id) > 128:
                raise ValueError("module identifiers must contain 1 to 128 characters")
            first, *rest = module_id
            allowed_rest = set("abcdefghijklmnopqrstuvwxyz0123456789_.-")
            if first not in set("abcdefghijklmnopqrstuvwxyz") or any(
                character not in allowed_rest for character in rest
            ):
                raise ValueError(
                    "module identifiers must start with a lowercase letter and use "
                    "lowercase letters, digits, dots, underscores, or hyphens"
                )
        return value

    @field_validator("reasons")
    @classmethod
    def reasons_are_non_empty(cls, value: list[str]) -> list[str]:
        if any(not reason for reason in value):
            raise ValueError("reasons must not be empty")
        return value
