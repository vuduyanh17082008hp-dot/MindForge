# MindForge

> **A resource-rational, evidence-calibrated architecture for longitudinal human-AI collaboration.**

MindForge is a research project investigating whether an AI system can maintain **explicit, inspectable, and revisable beliefs about an individual**, make falsifiable predictions from those beliefs, compare them with real outcomes, and adapt assistance under bounded compute while preserving human autonomy.

### Core principles

- **State ≠ Trait** ? transient behavior must not silently become a persistent characteristic.
- **Model confidence ≠ metacognitive authority** ? routing, verification, and persistent writes are externally governed.
- **Memory is reconstructed and validated** ? historical context is not blindly replayed.
- **Prediction before correction** ? beliefs generate predictions that can later be tested against outcomes.
- **Decoupled execution** ? MindForge determines cognitive actions; execution layers such as Javis OS or a lightweight runner perform model/tool calls.

### Current status

**Research RFC + tested reference implementation.**

The repository currently contains the formal architecture, typed contracts, an External Metacognitive Governor, Prediction Ledger, Reconstructive Memory Gate, empirical competence contracts, and deterministic tests.

No large-scale human-subject effectiveness claim has been established yet.

### Start here

**[Read RFC-001: MindForge Architecture](docs/rfcs/RFC-001_MindForge_Architecture.md)**  
[Research Thesis](docs/RESEARCH-THESIS.md) ? [Data Contracts](docs/DATA-CONTRACTS.md) ? [Open Research Questions](docs/OPEN-RESEARCH-QUESTIONS.md)

---

## Problem

Personalized AI systems can preserve stale assumptions, confuse reports with facts, and spend the same computational effort on every interaction. They need explicit ways to represent uncertainty, notice prediction failures, and revise their understanding without weakening human control.

## Thesis

MindForge investigates whether structured, evidence-linked, revisable human modelling and selective cognition can improve adaptation over conversation-history-only personalization. This is a research thesis, not a demonstrated result.

## Core loop

`OBSERVE → MODEL → HYPOTHESIZE → PREDICT → ACT → EVALUATE → REVISE → repeat`

The defining goal is a system that can detect when its understanding of a person is wrong and revise that understanding.

## Current status

MindForge v1 is a foundation only. It contains the canonical architecture, initial typed cognitive contracts, and deterministic contract tests. It has no cognitive runtime.

See [MASTER-ARCHITECTURE-v1.md](docs/MASTER-ARCHITECTURE-v1.md) for the canonical design and [RESEARCH-THESIS.md](docs/RESEARCH-THESIS.md) for the research framing.

## Research status

The architecture contains implemented contracts, planned systems, experimental concepts, and open research questions. These maturity levels are explicitly distinguished in the architecture document. No effectiveness claims have yet been established.

## What is implemented

- A Python 3.11+ package using Pydantic v2.
- Typed contracts for observations, evidence, beliefs, hypotheses, predictions, outcomes, prediction errors, context capsules, cognitive budgets, and cognitive routes.
- Explicit provenance, epistemic status, evidence quality, calibration, uncertainty, scope, and route categories.
- Validation and serialization tests for the schema layer.

## What is not implemented

There is no inference engine, human-model inference, Bayesian updater, simulation, memory engine, learning engine, router execution, agent runtime, API, user interface, provider integration, database, RAG system, or Javis adapter.

## Repository structure

```text
apps/          Reserved application boundaries; currently empty
docs/          Canonical architecture and research documentation
evaluation/    Reserved benchmark, ablation, and dataset boundaries
experiments/   Reserved research experiments boundary
runtime/       Reserved operational adapters, including future Javis work
src/           MindForge Python package and contracts
tests/         Contract tests
```

## Research Architecture

MindForge is a research architecture for longitudinal human-AI collaboration. It studies whether an AI system can maintain explicit, inspectable, and revisable beliefs about an individual; make falsifiable predictions from those beliefs; resolve delayed outcomes; evaluate its own calibration; and adapt assistance under bounded compute while preserving human autonomy.

The current architecture separates cognitive control from model execution. Foundation models may generate or reason, but routing, evidence sufficiency, persistent-memory writes, and safety-critical escalation are governed externally by typed policies and empirical state.

Core invariants include:

- **State ≠ Trait**
- **Model self-confidence is not metacognitive authority**
- **Memory is reconstructed and validated, not blindly replayed**
- **MindForge determines cognitive actions; execution infrastructure handles API/tool calls**

The current work is a **Research RFC / Architectural Specification**, not a claim of general superiority or a completed large-scale human study.

?? Read the full specification in [RFC-001](docs/rfcs/RFC-001_MindForge_Architecture.md).

## Development setup

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

No global installation is required.

## Testing

```powershell
.venv\Scripts\python -m pytest
.venv\Scripts\python -m compileall -q src tests
```

## Disclaimer and limitations

MindForge does not claim AGI, consciousness, mind reading, psychological diagnosis, faithful simulation of an individual, solved human cognition, or solved theory of mind. Its human-model concepts are provisional research constructs and must remain inspectable, revisable, privacy-aware, and subordinate to human autonomy.

