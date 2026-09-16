# MindForge Data Contracts v1

Schema reference for the first foundation contracts.

These contracts represent artifacts; they do not implement inference, routing, learning, memory, or runtime behavior. Unknown fields are rejected. IDs are UUIDs. Timestamps require a timezone and normalize to UTC.

## Shared metadata

`Provenance` distinguishes user, system, tool, external source, memory, and derived-inference origins. It supports traceability but does not establish truth. `Scope` distinguishes turn, session, persistent, and external lifetimes. Typed artifact references preserve the category of a referenced UUID.

Confidence, probability, evidence reliability, evidence quality, uncertainty, and calibration have separate representations. No invariant equates them. Cognitive artifacts include identity, creation time, provenance, scope, revisability, optional expiry, and tags. Expiry must follow creation.

## Observation

**Semantic meaning:** Something observed or reported, categorized as a user claim, system observation, tool result, or external source.

**Invariants:** User claims have `reported` status. Other observations may be `observed`, `reported`, or `unknown`.

**What it does not mean:** An observation is not a verified fact.

**Important validation:** Content is non-empty; inferred, hypothesized, and predicted statuses are rejected; undeclared fields such as `is_true` are forbidden.

```json
{
  "provenance": {"kind": "user"},
  "kind": "user_claim",
  "content": "I learn diagrams more easily with spoken explanation.",
  "epistemic_status": "reported"
}
```

## Belief

**Semantic meaning:** A revisable proposition held by the system and linked to evidence.

**Invariants:** Confidence is in `[0, 1]`; support and contradiction references stay separate; calibration has its own status.

**What it does not mean:** A belief is not a fact, diagnosis, trait, or guarantee. Confidence does not establish competence.

**Important validation:** Proposition is non-empty, confidence is bounded, and status is `inferred` or `unknown`.

```json
{
  "provenance": {"kind": "derived_inference"},
  "proposition": "Audio may support comprehension in this session.",
  "confidence": 0.62,
  "supporting_evidence_ids": [],
  "contradicting_evidence_ids": [],
  "epistemic_status": "inferred"
}
```

## Hypothesis

**Semantic meaning:** A candidate explanation that can be challenged by evidence and falsifiers.

**Invariants:** Confidence and optional estimated probability are independently bounded. Evidence for and against stay separate. Status remains hypothesized.

**What it does not mean:** A hypothesis is not established. Estimated probability does not imply Bayesian updating exists.

**Important validation:** Claim is non-empty; confidence and probability are in `[0, 1]`; status is explicit.

```json
{
  "provenance": {"kind": "derived_inference"},
  "claim": "Combined formats improve near-term recall here.",
  "confidence": 0.55,
  "estimated_probability": 0.65,
  "evidence_for": [],
  "evidence_against": [],
  "falsifiers": ["Matched trials show worse recall."],
  "predicted_observations": [],
  "status": "active"
}
```

## Evidence

**Semantic meaning:** Material offered in support of or against propositions, optionally linked to observations.

**Invariants:** Reliability is in `[0, 1]`. Quality is separate. Supports and contradictions stay separate.

**What it does not mean:** Evidence is not automatically a belief. Reliability is not truth, confidence, or calibration.

**Important validation:** Content is non-empty and reliability is bounded.

```json
{
  "provenance": {"kind": "tool"},
  "content": "Four of five questions were correct.",
  "reliability": 0.8,
  "quality": "medium",
  "supports": ["Audio may help in this session."],
  "contradicts": []
}
```

## Prediction

**Semantic meaning:** An expected future observation or outcome for a target, positive horizon, and context.

**Invariants:** Confidence is bounded; status and calibration are explicit; epistemic status stays predicted.

**What it does not mean:** A prediction is not truth. Confidence is not empirical calibration.

**Important validation:** Target and expected outcome are non-empty; horizon is positive; confidence is in `[0, 1]`.

```json
{
  "provenance": {"kind": "derived_inference"},
  "target": "next recall check",
  "expected_outcome": "Three of four relationships recalled.",
  "confidence": 0.58,
  "horizon": "PT30M",
  "context": {"format": "diagram-plus-audio"}
}
```

## Outcome

**Semantic meaning:** What was later observed, optionally linked to a prediction and evidence.

**Invariants:** Observation time is timezone-aware and normalizes to UTC.

**What it does not mean:** An outcome does not determine why a prediction succeeded or failed.

**Important validation:** Observed result is non-empty and timestamps are aware.

```json
{
  "provenance": {"kind": "tool"},
  "prediction_id": "50000000-0000-4000-8000-000000000001",
  "observed_result": "Two of four relationships recalled.",
  "observed_at": "2026-09-16T08:45:00Z"
}
```

## PredictionError

**Semantic meaning:** A recorded outcome mismatch or evidence of a possible structural problem.

**Invariants:** Type is `outcome` or `structural`. Optional magnitude is bounded. Attribution entries remain candidates.

**What it does not mean:** Prediction error does not prove a cause or perform module-level credit assignment.

**Important validation:** Prediction ID and description are required; magnitude and candidate confidence are bounded.

```json
{
  "provenance": {"kind": "derived_inference"},
  "error_type": "outcome",
  "prediction_id": "50000000-0000-4000-8000-000000000001",
  "description": "Observed recall was below expectation.",
  "magnitude": 0.5,
  "attribution_candidates": []
}
```

## ContextCapsule

**Semantic meaning:** Curated turn context with typed artifact references, memory references, model/session references, uncertainty, provenance, and budget.

**Invariants:** Each relevant-artifact field accepts only its matching artifact type. Goal, provenance, and budget are required.

**What it does not mean:** A capsule is not the complete persistent history or proof that selected context is sufficient.

**Important validation:** Reference categories cannot be mixed, timestamps are aware, and budget constraints apply.

```json
{
  "current_goal": "Choose the next explanation format.",
  "relevant_observations": [{
    "artifact_id": "10000000-0000-4000-8000-000000000001",
    "artifact_type": "observation"
  }],
  "provenance": {"kind": "system"},
  "budget": {
    "max_latency_ms": 800,
    "max_model_calls": 1,
    "max_tokens": 1200,
    "max_parallel_modules": 2,
    "max_tool_calls": 0,
    "max_reasoning_depth": 2
  }
}
```

## CognitiveBudget

**Semantic meaning:** Explicit finite upper bounds for a routed unit of cognition.

**Invariants:** Latency and parallel-module limits are positive. Calls, tokens, tool calls, and reasoning depth are non-negative. Every field is required.

**What it does not mean:** A budget does not execute, schedule, meter, or enforce work.

**Important validation:** Negative values, zero latency, and zero parallel capacity are rejected. There is no unlimited default.

```json
{
  "max_latency_ms": 250,
  "max_model_calls": 0,
  "max_tokens": 0,
  "max_parallel_modules": 1,
  "max_tool_calls": 0,
  "max_reasoning_depth": 0
}
```

## CognitiveRoute

**Semantic meaning:** A domain-agnostic FAST or DEEP decision with module identifiers, reasons, and trust requirements.

**Invariants:** Mode is `fast` or `deep`. Module IDs are unique lowercase identifiers using letters, digits, dots, underscores, or hyphens. No Dante-specific module list exists.

**What it does not mean:** A route does not execute modules, guarantee latency, or certify correctness.

**Important validation:** Duplicate or malformed module IDs and empty reasons are rejected. Domain implementations may provide valid custom IDs.

```json
{
  "mode": "deep",
  "selected_modules": ["human_model", "education.explanation-planner"],
  "reason_codes": ["ambiguity", "verification_needed"],
  "reasons": ["The preferred format is uncertain here."],
  "requires_calibration": true,
  "requires_verification": true,
  "requires_human_clarification": false
}
```

## Compatibility policy

The project is pre-runtime. Once artifacts are persisted, breaking changes require an explicit schema-version decision and migration plan. Evolution must preserve epistemic distinctions rather than flatten them for convenience.
