"""Runtime reproducibility contracts for MindForge."""

from __future__ import annotations

from hashlib import sha256
import json
from typing import Any
from uuid import UUID, uuid4

from pydantic import ConfigDict, Field, field_validator

from mindforge.contracts.base import MindForgeModel, utc_now


class ContextManifest(MindForgeModel):
    """
    Lightweight reproducibility record for one cognitive decision.

    The manifest identifies the state and versioned artifacts used to build a
    turn without duplicating the full conversation or ContextCapsule.
    """

    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
        validate_assignment=True,
        frozen=True,
    )

    manifest_id: UUID = Field(default_factory=uuid4)
    user_id: UUID
    session_id: UUID
    task_id: str | None = Field(default=None, min_length=1, max_length=256)

    input_hash: str = Field(min_length=64, max_length=64)

    human_model_version: int = Field(ge=0)
    session_state_version: int = Field(ge=0)

    evidence_ids: tuple[str, ...] = ()
    active_belief_ids: tuple[UUID, ...] = ()

    task_version: str = Field(min_length=1, max_length=128)
    policy_version: str = Field(min_length=1, max_length=128)
    actor_id: str = Field(min_length=1, max_length=256)
    actor_version: str = Field(min_length=1, max_length=128)
    retrieval_version: str | None = Field(
        default=None,
        min_length=1,
        max_length=128,
    )

    selected_feature_keys: tuple[str, ...] = ()
    created_at: object = Field(default_factory=utc_now)

    manifest_hash: str = Field(min_length=64, max_length=64)

    @field_validator("input_hash", "manifest_hash")
    @classmethod
    def hashes_are_sha256_hex(cls, value: str) -> str:
        if len(value) != 64:
            raise ValueError("SHA-256 hashes must contain 64 hexadecimal characters")

        try:
            int(value, 16)
        except ValueError as exc:
            raise ValueError("hash must be hexadecimal") from exc

        return value.lower()

    @staticmethod
    def hash_text(text: str) -> str:
        """Return a SHA-256 integrity digest for text."""

        return sha256(text.encode("utf-8")).hexdigest()

    @classmethod
    def build(
        cls,
        *,
        user_id: UUID,
        session_id: UUID,
        user_input: str,
        human_model_version: int,
        session_state_version: int,
        task_version: str,
        policy_version: str,
        actor_id: str,
        actor_version: str,
        task_id: str | None = None,
        evidence_ids: tuple[str, ...] = (),
        active_belief_ids: tuple[UUID, ...] = (),
        retrieval_version: str | None = None,
        selected_feature_keys: tuple[str, ...] = (),
    ) -> "ContextManifest":
        manifest_id = uuid4()
        created_at = utc_now()
        input_hash = cls.hash_text(user_input)

        payload: dict[str, Any] = {
            "manifest_id": str(manifest_id),
            "user_id": str(user_id),
            "session_id": str(session_id),
            "task_id": task_id,
            "input_hash": input_hash,
            "human_model_version": human_model_version,
            "session_state_version": session_state_version,
            "evidence_ids": list(evidence_ids),
            "active_belief_ids": [str(item) for item in active_belief_ids],
            "task_version": task_version,
            "policy_version": policy_version,
            "actor_id": actor_id,
            "actor_version": actor_version,
            "retrieval_version": retrieval_version,
            "selected_feature_keys": list(selected_feature_keys),
            "created_at": created_at.isoformat(),
        }

        canonical = json.dumps(
            payload,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        ).encode("utf-8")

        manifest_hash = sha256(canonical).hexdigest()

        return cls(
            manifest_id=manifest_id,
            user_id=user_id,
            session_id=session_id,
            task_id=task_id,
            input_hash=input_hash,
            human_model_version=human_model_version,
            session_state_version=session_state_version,
            evidence_ids=evidence_ids,
            active_belief_ids=active_belief_ids,
            task_version=task_version,
            policy_version=policy_version,
            actor_id=actor_id,
            actor_version=actor_version,
            retrieval_version=retrieval_version,
            selected_feature_keys=selected_feature_keys,
            created_at=created_at,
            manifest_hash=manifest_hash,
        )
