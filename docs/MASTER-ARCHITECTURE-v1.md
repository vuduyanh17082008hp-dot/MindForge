# MindForge Master Architecture v1

**Status:** Canonical foundation architecture  
**Scope:** Research architecture and typed schema boundary; no cognitive runtime  
**Version:** 1.0

## 1. Project thesis

MindForge is an adaptive human-AI cognitive architecture intended to build, test, predict with, and revise a model of the human it works with over time. Its central commitment is correction: the system should expose its assumptions, connect them to evidence, test expectations against outcomes, and revise them when warranted.

The core loop is:

`OBSERVE → MODEL → HYPOTHESIZE → PREDICT → ACT → EVALUATE → REVISE → repeat`

The thesis is that evidence-linked, revisable human modelling combined with selective cognition may improve adaptation over conversation-history-only personalization without requiring every cognitive component on every interaction. This remains unproven.

## 2. Research question

> How can an AI system adapt to a changing individual while remaining evidence-calibrated, correctable, computationally efficient, and supportive of human autonomy?

## 3. What MindForge is

MindForge is a standalone research-engineering project for studying adaptive human-AI collaboration. It defines architectural boundaries, epistemic distinctions, resource constraints, prediction and evaluation concepts, and versioned learning principles. The initial implementation is a provider-neutral typed schema layer.

## 4. What MindForge is not

MindForge is not a claim of AGI, consciousness, mind reading, psychological diagnosis, faithful simulation of an individual, solved human cognition, or solved theory of mind. It is not a model provider, workflow engine, application UI, or database. Its provisional human models must not be treated as ground truth about a person.

## 5. Three-loop architecture

The architecture uses three loops operating at different time scales. It is not a 30–40-stage serial pipeline.

```text
                      TRUST / CONSTITUTION
                              │
                              ▼
                       LOOP A — FRAME
                              │
                       Context Capsule
                              │
                              ▼
                    Router + Budget
                       │          │
                     FAST       DEEP
                       │          │
                       │          ▼
                       │   LOOP B — DELIBERATE
                       │   Shared Workspace
                       │   Human Model
                       │   Hypotheses
                       │   Beliefs
                       │   Predictions
                       │   Simulation
                       │   Normative constraints
                       │
                       └─────┬────┘
                             ▼
                      Epistemic Gate
                             │
                             ▼
                       Output Guard
                             │
                             ▼
                           ACTION
                             │
                             ▼
                           OUTCOME
                             │
                             ▼
                      Prediction Error
                      │              │
                Outcome PE      Structural PE
                      └──────┬───────┘
                             ▼
                       LOOP C — LEARN
                 retry / reflect / consolidate
                             │
                             └──────────────↺
```

### Loop A — Frame

Loop A operates per turn. Input or perception informs retrieval, which produces a curated Context Capsule. Salience and relevance selection feed an early Router with an explicit Cognitive Budget. Early routing is essential: a FAST interaction must be able to avoid deep deliberative machinery.

The Context Capsule is bounded working context, not a dump of the complete persistent history. Intake trust constraints apply before observations enter downstream reasoning.

### Loop B — Deliberate

Loop B is invoked selectively. It contains a shared Cognitive Workspace: a limited bus or blackboard through which modules may exchange structured artifacts. The workspace is not a pipeline stage, and its possible participants do not imply a fixed execution order.

Potential future participants include the Human Model, Common Ground, Hypothesis Engine, Belief State, Prediction, Simulation, epistemic reasoning, normative constraints, and calibration. They are conceptual participants in v1 and are not implemented.

### Loop C — Learn

Loop C separates learning by time scale:

- Turn level: bounded retry after a local, recoverable failure.
- Session level: structured reflection over interaction outcomes.
- Offline: consolidation, contradiction resolution, drift triage, versioned model updates, and memory-delta merges.

Learning is never represented as one unbounded synchronous per-turn loop.

## 6. Cross-cutting constitution

The constitution applies during intake, cognition, action generation, output, and persistence. It is not a final filter attached after reasoning.

The foundation preserves these distinctions in types and validation:

- Fact is not Belief.
- Belief is not Inference.
- Inference is not Diagnosis.
- Prediction is not Truth.
- State is not Trait.
- Confidence is not Competence.
- Memory is not Current Reality.
- Population Prior is not Individual Truth.

The foundation contains no `Fact` or `Diagnosis` cognitive type. User claims remain reported observations. Beliefs, hypotheses, predictions, evidence quality, confidence, uncertainty, and calibration have separate representations. Future normative controls must remain active at every trust boundary and support correction, consent, privacy, and user override.

## 7. FAST and DEEP

FAST is a low-latency route for work that can be completed within a small explicit budget and without shared-workspace deliberation. It may still require verification or clarification when the route contract says so.

DEEP may activate selected deliberative modules through the shared workspace. DEEP does not mean every module runs. Route decisions must be inspectable and constrained by budget. Neither route is implemented in v1; only its data contract exists.

## 8. Cognitive Resource Budget

Resource-rational cognition requires explicit finite bounds. `CognitiveBudget` represents maximum latency, model calls, tokens, parallel modules, tool calls, and reasoning depth. It contains no hidden unlimited sentinel. A future router must consume or refine this budget without silently expanding it. The current implementation validates budgets but does not enforce them at runtime.

## 9. Cognitive Workspace

The Cognitive Workspace is a bounded shared bus for structured cognitive artifacts. Modules may publish, inspect, challenge, or refine artifacts subject to their permissions and budget. It should make provenance and disagreement visible while avoiding a rigid serial pipeline. Capacity, arbitration, concurrency, and measurable value remain experimental.

## 10. Human Model System

Future MindForge uses one Human Model System with scoped views rather than four unrelated models:

1. **Persistent Human Model:** versioned, long-lived representations of tendencies, capabilities, and knowledge.
2. **Session Common Ground:** the current shared goal, assumptions, commitments, and unresolved questions.
3. **Short-Horizon Predictor:** expected near-term response, misunderstanding, or behavior within a stated context.
4. **Change Detector:** candidates for Human Drift, Model Drift, or Agent Drift.

These views must keep transient state separate from enduring trait claims. The system does not currently know how to reliably distinguish genuine human change from degradation of its model. That is an open research question, not a solved capability.

## 11. Epistemic Action

An epistemic action is chosen partly to improve the system's knowledge rather than only to complete the immediate task. Examples include asking a targeted clarification, checking an external source, or selecting a reversible action that discriminates between hypotheses. A future Epistemic Gate should weigh expected information gain, human cost, privacy, risk, and cognitive budget. No epistemic-action policy exists in v1.

## 12. Output and trust boundary

Before an action reaches the user or an external system, the Epistemic Gate and Output Guard conceptually check whether uncertainty is represented, claims are supported at an appropriate level, constraints are respected, and the action preserves user control. This boundary cannot repair unsafe or invalid reasoning by itself; trust constraints also operate upstream. No output runtime is implemented.

## 13. Outcome evaluation

An Outcome records what was later observed, with provenance and optional evidence references. Evaluation compares a prediction with an outcome under the original context and horizon. An outcome does not automatically reveal why an expectation succeeded or failed, and a single success does not establish calibration or competence.

## 14. Outcome Prediction Error

Outcome Prediction Error records a mismatch between the expected and observed result. It can indicate that a prediction was wrong in that instance. It does not by itself show that the underlying human model or reasoning structure was wrong.

## 15. Structural Prediction Error

Structural Prediction Error records evidence that the underlying state representation, assumptions, or model structure may be inadequate. It may name attribution candidates, but those remain hypotheses rather than proven module-level causes. Automatic credit assignment across cognitive modules is not claimed.

## 16. Multi-timescale learning

Turn retries must be bounded and local. Session reflection may summarize patterns and propose changes without immediately rewriting persistent models. Offline learning may check contradictions, compare versions, triage drift, and merge approved deltas. These time scales require separate policies, evidence thresholds, and rollback behavior.

## 17. Versioned memory principles

Future memory uses append-only or versioned writes, structured delta proposals, conflict checking, and offline consolidation. Cognitive modules propose changes; trusted code validates them; trusted code writes accepted versions. Unrestricted in-place mutation is excluded from the architecture. Memory is historical evidence, not guaranteed current reality. No memory engine exists in v1.

## 18. Drift taxonomy

**Human Drift** is genuine change in a person's goals, knowledge, preferences, state, or behavior. **Model Drift** is degradation or staleness in the system's representation of that person. **Agent Drift** is change in the agent's own behavior caused by prompts, models, policies, tools, or implementation. Observed discrepancy may be consistent with more than one category. Classification must remain tentative until supported by discriminating evidence.

## 19. Human autonomy objective

Adaptation should increase useful support while preserving a person's ability to understand, correct, refuse, and change the system's assumptions. The architecture should favor inspectable representations, proportional clarification, reversible actions, user override, and bounded persistence. Autonomy cannot responsibly be reduced to a single universal score; its operational measurement is an open research problem.

## 20. Relationship to Javis OS

MindForge is the cognitive architecture. Javis OS may later serve as an operational substrate:

```text
MindForge
    ↓
Javis Adapter
    ↓
Javis OS
    ↓
Model / Tool Providers
```

MindForge remains model-provider agnostic and is not defined as a Javis plugin. The adapter is a future boundary. Javis OS is not modified or copied into this repository.

## 21. Relationship to Dante

Dante is the first planned domain application and testbed:

```text
MindForge
    ↓
Domain implementation
    ↓
Dante
    ↓
Fitness coaching
```

Dante is outside the MindForge cognitive core. Core contracts contain no fitness-specific fields or specialist names.

## 22. Current implementation status

**IMPLEMENTED**

- Standalone repository foundation.
- Canonical architecture and research documentation.
- Pydantic v2 contracts for the first cognitive artifacts, provenance, context, budget, and route decisions.
- Contract validation and deterministic tests.

**PLANNED**

- Bounded context construction, router execution, trust-boundary enforcement, workspace infrastructure, versioned memory, and evaluation harnesses.
- A separate Javis adapter, after the core boundary is stable.

**EXPERIMENTAL**

- Shared-workspace participation and arbitration.
- Epistemic-action policies.
- Structural-error attribution and change detection.
- Metrics for adaptation, calibration, and autonomy.

**OPEN RESEARCH QUESTION**

- Reliable separation of Human, Model, and Agent Drift.
- Person-specific predictive validity.
- Causal credit assignment across modules.
- The measurable value of a shared workspace.
- Valid, non-reductive measures of human autonomy and dependency.

## 23. Explicit research limitations

The v1 implementation cannot infer a human model, generate hypotheses, update beliefs, make or evaluate live predictions, route requests, execute tools, consolidate memory, or learn. Typed schemas improve representational discipline but cannot guarantee truthful inputs, sound inference, calibration, privacy, fairness, or safe behavior. Longitudinal adaptation may amplify error and sycophancy. Any future human study needs appropriate consent, privacy, security, withdrawal, and review practices.

## 24. Open research questions

1. How can we distinguish genuine human change from degradation of the system's model of that human?
2. How should structural prediction error be attributed across multiple cognitive modules?
3. Can an AI reliably simulate a specific person's future response rather than a generic response?
4. Does a shared workspace architecture measurably improve an LLM-based system, or merely make the architecture more theoretically elegant?
5. How should we measure human autonomy and dependency without reducing them to misleading single-number scores?
6. Which observations justify persistence, and how should consent and expiration interact?
7. When is clarification worth its interruption cost?
8. How should calibration be evaluated under non-stationary individual behavior?

