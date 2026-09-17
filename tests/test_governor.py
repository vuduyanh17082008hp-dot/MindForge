from mindforge.governor import (
    ExternalMetacognitiveGovernor,
    GovernorDecision,
    GovernorInput,
)


def base_input(**overrides):
    data = dict(
        task_risk=0.10,
        evidence_sufficiency=0.90,
        competence_score=0.90,
        competence_mature=True,
        unresolved_contradictions=0,
        budget_remaining_usd=1.0,
        estimated_fast_cost_usd=0.001,
        estimated_deep_cost_usd=0.01,
        retrieval_available=True,
        verification_available=True,
        safety_block=False,
        hard_policy_violation=False,
    )
    data.update(overrides)
    return GovernorInput(**data)


def test_blocks_hard_safety_constraint():
    governor = ExternalMetacognitiveGovernor()
    result = governor.evaluate(base_input(safety_block=True))
    assert result.decision is GovernorDecision.BLOCK


def test_requires_verification_for_high_risk_insufficient_evidence():
    governor = ExternalMetacognitiveGovernor()
    result = governor.evaluate(
        base_input(task_risk=0.95, evidence_sufficiency=0.20)
    )
    assert result.decision is GovernorDecision.REQUIRE_VERIFICATION


def test_allows_fast_only_with_mature_competence():
    governor = ExternalMetacognitiveGovernor()
    result = governor.evaluate(base_input())
    assert result.decision is GovernorDecision.ALLOW_FAST

    immature = governor.evaluate(base_input(competence_mature=False))
    assert immature.decision is GovernorDecision.ALLOW_DEEP
