# Research and Engineering Risks

All mitigations below are directions for future work unless explicitly marked implemented. The foundation currently provides representational constraints and tests, not operational safeguards.

## Sycophancy

**Risk:** The system mirrors a user's beliefs or preferences instead of giving warranted disagreement.  
**Mechanism:** Personalization rewards agreement, and prior user claims are treated as truth.  
**Mitigation direction:** Preserve reported claims as observations, retain contradictory evidence, evaluate disagreement quality, and make correction behavior explicit.  
**Current status:** Partially represented in contracts; behavioral mitigation is not implemented.

## Self-echo chamber

**Risk:** Earlier system inferences are retrieved as if they were independent evidence.  
**Mechanism:** Derived content loses provenance and recursively reinforces itself.  
**Mitigation direction:** Track derived-inference provenance, distinguish primary observations from derived artifacts, and detect circular support graphs.  
**Current status:** Provenance categories are implemented; support-graph checks are not.

## Memory corruption

**Risk:** Incorrect or malicious content becomes persistent and influences later interactions.  
**Mechanism:** Unvalidated in-place writes or weak conflict handling.  
**Mitigation direction:** Use versioned writes, structured delta proposals, trusted validation, conflict checks, rollback, and offline consolidation.  
**Current status:** Architecture documented; memory is not implemented.

## Context collapse

**Risk:** Important qualifications, time boundaries, or contradictions disappear from working context.  
**Mechanism:** Aggressive selection or compression creates a misleading Context Capsule.  
**Mitigation direction:** Retain provenance and uncertainty, test retrieval recall, preserve unresolved contradictions, and allow clarification.  
**Current status:** Context Capsule contract implemented; construction and evaluation are not.

## Persona drift

**Risk:** The agent's behavior changes while appearing to be change in the human.  
**Mechanism:** Model, prompt, policy, or tool changes alter interpretation and response patterns.  
**Mitigation direction:** Version agent configuration, run regression evaluations, and explicitly consider Agent Drift in error analysis.  
**Current status:** Taxonomy documented; detection is not implemented.

## Overconfident routing

**Risk:** A FAST route skips needed verification or deliberation.  
**Mechanism:** Complexity, stakes, ambiguity, or novelty is underestimated.  
**Mitigation direction:** Require inspectable reason codes, escalation triggers, calibration checks, conservative high-stakes policies, and route-quality evaluation.  
**Current status:** Route flags and reason codes are implemented; routing is not.

## Privacy of persistent human models

**Risk:** Sensitive, incorrect, or unwanted personal representations persist or leak.  
**Mechanism:** Excess collection, indefinite retention, broad access, or opaque inference.  
**Mitigation direction:** Data minimization, purpose limitation, consent, expiry, access control, deletion and correction paths, audit logs, and privacy review.  
**Current status:** Scope, expiry, and provenance fields exist; storage safeguards are not implemented.

## Clarification fatigue

**Risk:** Repeated questions burden the user and reduce utility.  
**Mechanism:** The system seeks certainty without pricing interruption or remembering prior answers appropriately.  
**Mitigation direction:** Budget clarification, estimate decision value, batch questions, accept bounded uncertainty, and measure interruption cost.  
**Current status:** Clarification can be requested by a route contract; policy is not implemented.

## Latency

**Risk:** Deliberative processing makes routine interaction too slow.  
**Mechanism:** Every module runs on every turn or runtime limits are ignored.  
**Mitigation direction:** Route early, keep FAST genuinely bounded, enforce explicit latency budgets, and measure end-to-end tails.  
**Current status:** Budget and FAST/DEEP contracts are implemented; enforcement is not.

## Compute cost

**Risk:** Adaptation consumes unjustified model, token, or tool resources.  
**Mechanism:** Unbounded deliberation, retries, parallelism, or consolidation.  
**Mitigation direction:** Enforce resource budgets, cap retries, evaluate marginal benefit, and use selective modules.  
**Current status:** Finite budget fields validate; runtime accounting is not implemented.

## False confidence in human modelling

**Risk:** Provisional representations are treated as accurate descriptions of a person.  
**Mechanism:** Confidence is confused with truth, competence, evidence quality, or calibration.  
**Mitigation direction:** Keep categories separate, expose evidence and contradictions, test predictions, support correction, and avoid diagnostic claims.  
**Current status:** Type distinctions are implemented; reliable modelling is an open research problem.

