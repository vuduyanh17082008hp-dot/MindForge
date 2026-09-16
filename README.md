# MindForge

> An evidence-calibrated cognitive architecture for adaptive human-AI collaboration.

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

