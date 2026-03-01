# Experiment Doctrine

## Purpose

This page defines how ChangeOnt kernel research should be conducted without creating code drift, semantic duplication, or uncontrolled variant explosion.

---

## Core Principle

Experiments must vary:
- assembly
- activation
- weights
- semantic combinator choice
- header/meta-header settings

They must **not** primarily vary by cloning files into many near-duplicate implementations.

The repo should preserve one implementation per semantic unit wherever possible.

---

## Allowed Experimental Axes

### 1. Element isolation
Examples:
- EA only
- EB only
- EC only

Purpose:
- test whether the mechanism has standalone value
- inspect its internal telemetry and semantic signature

### 2. Element combinations
Examples:
- EA + EB
- EA + EC
- EB + EC
- EA + EB + EC

Purpose:
- test whether mechanisms compose meaningfully
- inspect interaction effects

### 3. Weight variation
Examples:
- relative weighting between active elements
- relative weighting between CO and classical fallback
- internal declared weights where explicitly supported

Purpose:
- test whether a stable weighting pattern emerges across tasks

### 4. Semantic combinator variation
Examples:
- additive vs multiplicative
- gated vs ungated
- CO-native vs classical composition laws

Purpose:
- test candidate law-forms without changing the primitive set itself

Implementation hint (current):
- `semantic_overrides` can be set in CO agent params to remap semantic combinators.

### 5. Header / meta-header variation
Examples:
- detected stability only
- external prior only
- mixed control

Purpose:
- test deployment/control assumptions separately from semantic mechanism content

---

## Required Experimental Discipline

### Cross-task evaluation
Experiments should be tested across different task families where possible.

### Budget parity
Comparisons should preserve reasonable parity in budget and observability.

### Telemetry
Reward/performance alone is not enough.

Where relevant, experiments should also inspect:
- identity behavior
- birth behavior
- closure/class behavior
- mask behavior
- stability/control behavior

### Logging
Experimental conditions must be explicit and recoverable from configs/logs.

---

## What does not count as a clean experiment

The following are discouraged unless explicitly justified:
- cloning many slightly different EA/EB files
- silently changing formulas inside element files without contract updates
- sweeping many parameters without a clear semantic question
- introducing task-specific ontology logic into translators to make an experiment “work”

---

## Scientific posture

The goal is not to prove the final kernel by fiat.

The goal is to test whether:
- derivationally motivated primitives
- candidate semantic combinators
- semantically meaningful elements

produce transfer, explanatory value, and disciplined behavior across tasks.

This page is binding for future experiment design.
