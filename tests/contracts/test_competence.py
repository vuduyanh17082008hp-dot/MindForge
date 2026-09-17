import pytest

from mindforge.contracts.competence import CompetenceProfile


def make_profile() -> CompetenceProfile:
    return CompetenceProfile(
        actor_id="test-model",
        actor_version="v1",
        task_class="dsa_recursion",
        domain="learning",
        tool_config_hash="0" * 64,
    )


def test_competence_profile_updates_immutably():
    original = make_profile()

    updated = original.record_outcome(
        success=True,
        evidence_weight=0.5,
    )

    assert original.alpha == pytest.approx(1.0)
    assert original.beta == pytest.approx(1.0)
    assert original.total_evaluated == 0

    assert updated.alpha == pytest.approx(1.5)
    assert updated.beta == pytest.approx(1.0)
    assert updated.total_evaluated == 1
    assert updated.posterior_mean > original.posterior_mean


def test_competence_profile_rejects_invalid_confident_failure():
    profile = make_profile()

    with pytest.raises(
        ValueError,
        match="confident_failure cannot be true",
    ):
        profile.record_outcome(
            success=True,
            confident_failure=True,
        )
