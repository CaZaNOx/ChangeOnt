# P7 Precision

## Purpose

P7 Precision encodes a reusable notion of **resolution / discrimination / coarse-graining level**.

Its role is to support:
- scale-sensitive behavior
- density-sensitive grouping
- stabilization by coarsening or tightening discrimination

---

## Primitive Role

P7 is a **scale/precision primitive**.

It exists because any local regime in change is plausibly dependent on:
- what differences are treated as relevant
- what differences are grouped together
- what resolution is currently operative

---

## Inputs

P7 may consume:
- visit density
- variance / dispersion proxies
- recent instability measures
- local recurrence indicators
- configured bounds for tightening/loosening

It remains task-agnostic.

---

## Outputs

P7 may return:
- precision level
- rounding level
- discrimination threshold
- tightened / loosened scalar

It does not itself define identity, but can affect the scale at which identity-like grouping is attempted.

---

## State Mutation

P7 may maintain bounded local state, for example:
- current precision level
- recent schedule value

But must not:
- become a hidden task-specific heuristic
- directly choose actions

---

## Why this primitive exists

If states/objects are local coarse-grainings of similar paths, then some notion of precision is unavoidable.

P7 is the reusable encoding of that pressure.

---

## Forbidden

P7 must not:
- silently re-implement closure/identity mechanisms
- contain task-specific translator logic
- directly emit final task action

---

## Telemetry

P7 need not emit direct primitive telemetry.

Signals derived from its use may appear through elements such as:
- density / precision mechanisms

---

## Current Status

P7 is retained as a justified primitive class even if exact scheduling laws remain provisional.