# P8 Loopiness

## Purpose

P8 Loopiness encodes a reusable notion of **recurrence / revisitation / local return pressure**.

Its role is to support:
- loop detection
- revisit-sensitive scheduling
- recurrence-aware control

---

## Primitive Role

P8 is a **recurrence primitive**.

It is not itself a full breadth-depth policy and not itself a complete closure mechanism.

It provides reusable recurrence-related quantities.

---

## Inputs

P8 may consume:
- local history
- revisit counts
- repeated transition patterns
- cyclicity indicators
- short trace windows

---

## Outputs

P8 may return:
- loopiness score
- revisit pressure
- recurrence scalar
- scheduler hints for consuming elements

It does not directly decide final actions.

---

## State Mutation

P8 may maintain local recurrence history, but must not:
- become task-specific
- hide policy decisions that belong to elements or headers

---

## Why this primitive exists

If change is self-involving and local regimes may stabilize or trap under recurrence, then some primitive notion of loopiness/return is strongly motivated.

P8 is the current reusable encoding of that pressure.

---

## Forbidden

P8 must not:
- directly define full breadth-depth scheduling
- become a task-specific loop detector
- choose final actions

---

## Telemetry

P8 may be surfaced through consuming elements if useful, but does not require direct primitive telemetry.

---

## Current Status

P8 is a justified primitive category and should remain separate from the element that consumes it.