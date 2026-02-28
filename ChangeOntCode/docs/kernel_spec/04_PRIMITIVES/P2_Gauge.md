# P2 Gauge

## Purpose

P2 Gauge encodes a reusable notion of **modulation of change by change**.

Its role is to support:
- adaptive weighting
- internal re-scaling
- control-sensitive semantic modulation
- regulation of how strongly other quantities matter

---

## Primitive Role

P2 is a **modulation primitive**.

It is not itself a full header, and it is not itself a full decision policy.

It exists because if change is primitive and self-involving, then some reusable notion of:
- amplification
- attenuation
- re-weighting
- regulation

is strongly motivated.

---

## Inputs

P2 may consume:
- scalar quantities from primitives/elements
- recent history summaries
- local stability indicators
- configurable gain parameters

The exact calling element defines the context.

P2 itself must remain task-agnostic.

---

## Outputs

P2 returns one or more gauge-modulated values, such as:
- adjusted scalar
- gain multiplier
- attenuation factor
- modulation weight

It does not emit final actions.

---

## State Mutation

P2 may maintain local primitive state if needed, for example:
- running average
- internal modulation baseline
- bounded gain state

But it must not:
- mutate environment-specific state
- become a hidden header
- silently store task-specific memory

---

## Binding Status

P2 is currently a **valid primitive role**, but its exact final law is not yet frozen.

This means:
- the architectural role is binding
- the exact formula is not yet fully binding

Current implementation may therefore remain minimal or partial.

---

## Why this primitive exists

From a change-first perspective, it is plausible that change does not merely propagate; it also modulates the significance of its own local expressions.

P2 is the reusable encoding of that pressure.

---

## Forbidden

P2 must not:
- become a task-specific heuristic
- directly choose actions
- silently duplicate header logic
- contain translator logic

---

## Telemetry

P2 does not require direct telemetry of its own.

If exposed, telemetry should appear through the element using it, not as standalone task-facing policy output.

---

## Current Status

P2 is retained as a justified primitive category, even if its exact formula remains under investigation.