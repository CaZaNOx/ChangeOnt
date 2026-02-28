# EH_BreadthDepth

## Purpose

EH_BreadthDepth is the kernel’s exploration-style preference mechanism.

Its role is to bias or select between broader vs deeper local exploration posture.

---

## Element Role

EH_BreadthDepth is an **element**.

It is not:
- a primitive
- a header
- a translator
- the final action chooser

It is a mechanism of weighted preference among exploration styles.

---

## Intended Primitive Dependencies

Primary intended dependencies:
- P8_Loopiness

Possible future additions:
- explicit depth/breadth support primitives

---

## Intended Semantic Combinator Form

Primary:
- **SC_WeightedSelection**

Secondary:
- **SC_GatedThreshold**

---

## Why these belong together

Breadth vs depth is not primarily an accumulation problem.

It is more naturally a competition/preference problem:
- should broader exploration dominate?
- should deeper continuation dominate?

That makes weighted selection the right primary law-form.

---

## Inputs

EH_BreadthDepth may consume:
- loopiness/recurrence information
- bounded exploration-state hints
- local traversal tendencies

---

## Outputs

It may produce:
- preference-weight signals
- exploration-bias outputs
- optional votes if explicitly documented in implementation

---

## State Mutation

EH_BreadthDepth may maintain:
- local exploration counters
- local recurrence-sensitive state

---

## Why this element exists

Different local regimes plausibly favor different exploration modes.

EH_BreadthDepth is the current architectural place for that preference logic.

---

## Forbidden

EH_BreadthDepth must not:
- become final action selection itself
- silently absorb translator logic
- pretend breadth/depth preference is a primitive rather than a mechanism

---

## Telemetry

No strict canonical telemetry is required yet, but explicit outputs should be documented if added.

---

## Current Status

- non-central but valid
- role binding
- exact formula provisional