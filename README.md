# MindForge
Road-to-UOW
# MindForge

### An Evidence-Calibrated Cognitive Architecture for Adaptive Human-AI Collaboration

> AI should not only remember a person.
> It should learn how to work with that person — while remaining uncertain, correctable and safe.

MindForge is an experimental cognitive architecture for building AI systems that adapt to humans over long-term interaction.

Rather than treating personalization as a larger prompt or a collection of stored memories, MindForge models adaptation as a continuous cycle:

**observe → hypothesize → predict → act → evaluate → correct**

The project investigates a central research question:

> How can an AI system continuously adapt to an individual while distinguishing evidence from inference, detecting when its model of that person is wrong, and preserving human autonomy?

---

## Why MindForge?

Most AI assistants currently rely on combinations of:

- conversation history
- retrieval
- user preferences
- persistent memory
- prompt-based personalization

These mechanisms are useful, but they create several unresolved problems.

### 1. Memory is not understanding

Knowing that a user previously preferred something does not tell us:

- whether that preference still holds
- why it existed
- whether it was context-dependent
- how confident the system should be
- what evidence would disprove it

MindForge therefore represents user understanding as **revisable hypotheses**, not permanent facts.

### 2. Personalization can become overconfidence

A system may repeatedly infer:

> "This user prefers concise explanations."

MindForge instead asks:

- What evidence supports this?
- In which contexts?
- How stable is the pattern?
- What contradicts it?
- Has the user changed?

### 3. More reasoning is not always better

Running every tool, model or agent for every request is expensive and can introduce unnecessary noise.

MindForge uses **selective cognitive routing** to activate only the processes required by the current problem.

### 4. Human-AI adaptation happens in both directions

An AI system changes the person using it.

Therefore a long-term assistant should not optimise only for engagement.

MindForge aims to track outcomes such as:

- user independence
- knowledge development
- reasoning quality
- confidence calibration
- reliance on AI
- transfer of learned skills

The objective is **productive co-adaptation**, not maximum dependency.

---

# Architecture

```text
Human
  │
  ▼
Perception / Context
  │
  ▼
Cognitive Context Compiler
  │
  ▼
Human Interaction Model
  │
  ▼
Latent Hypothesis Engine
  │
  ▼
Uncertainty / Evidence Evaluation
  │
  ▼
Meta-Controller
  │
  ├── FAST cognition
  │
  └── DEEP cognition
          │
          ▼
Selective Cognitive Modules
          │
          ▼
Internal Evaluation / Calibration
          │
          ▼
Action
          │
          ▼
Outcome
          │
          ▼
Prediction Error
     ┌────┴────┐
     ▼         ▼
Outcome     Structural
Error       Model Error
     └────┬────┘
          ▼
Model Revision
          │
          └──────────────↺
