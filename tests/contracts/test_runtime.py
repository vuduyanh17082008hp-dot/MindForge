from uuid import uuid4

from mindforge.contracts.runtime import ContextManifest


def test_context_manifest_builds_reproducibility_metadata():
    user_id = uuid4()
    session_id = uuid4()

    manifest = ContextManifest.build(
        user_id=user_id,
        session_id=session_id,
        user_input="Explain recursion with one example.",
        human_model_version=3,
        session_state_version=7,
        task_version="recursion-v1",
        policy_version="governor-v1",
        actor_id="test-model",
        actor_version="2026-09",
        evidence_ids=("evidence-1", "evidence-2"),
        selected_feature_keys=("human_model", "prediction"),
    )

    assert manifest.user_id == user_id
    assert manifest.session_id == session_id
    assert manifest.human_model_version == 3
    assert manifest.session_state_version == 7
    assert len(manifest.input_hash) == 64
    assert len(manifest.manifest_hash) == 64

    assert manifest.input_hash == ContextManifest.hash_text(
        "Explain recursion with one example."
    )


def test_context_manifest_input_hash_is_stable():
    text = "same input"

    first = ContextManifest.hash_text(text)
    second = ContextManifest.hash_text(text)

    assert first == second
    assert len(first) == 64
