# EA_HAQ

## Purpose

EA_HAQ is the kernel’s history-adaptive modulation mechanism.

Its role is to let recent change-history affect the current force of interpretation rather than treating every moment as equally context-free.

---

## Element Role

EA_HAQ is an **element**.

It is not:
- a primitive
- a translator
- a header
- the final action surface

It is a semantically meaningful mechanism built from lower-level ingredients.

---

## Intended Primitive Dependencies

Primary intended dependencies:
- P2_Gauge

Secondary / possible later dependencies:
- P7_Precision
- bounded history support

Current implementation may still operationalize parts of this minimally.

---

## Intended Semantic Combinator Form

Primary:
- **SC_MultiplicativeCoupling**

Secondary:
- **SC_AdditiveBlend**

---

## Why these belong together

EA_HAQ exists because history should not merely sit beside the present as another additive fact.

Rather, recent history should **modulate** the effective force of current interpretation.

That is why the primary intended law-form is multiplicative coupling:
- history-sensitive quantity changes the effective force of another quantity

Additive accumulation may still appear inside a local score, but modulation is the more important doctrine.

---

## Inputs

EA_HAQ may consume:
- recent history / trace information
- bounded local state
- primitive-derived modulation quantities

---

## Outputs

EA_HAQ may produce:
- `signals["EA_HAQ.novelty"]`
- other modulation-facing internal values if explicitly documented later

EA_HAQ should not directly choose final task actions.

---

## State Mutation

EA_HAQ may maintain:
- local bounded history state
- local EMA-like modulation state

It must not mutate:
- header ownership
- translator logic
- final action selection

---

## Why this element exists

A purely pointwise kernel would miss an important change-native fact:

what is happening now is not semantically independent of how change has recently been unfolding.

EA_HAQ is the current minimal mechanism for that idea.

---

## Forbidden

EA_HAQ must not:
- directly choose final actions
- silently absorb translator logic
- pretend to be just a primitive
- redefine header responsibilities

---

## Telemetry

Canonical telemetry may include:
- `signals["EA_HAQ.novelty"]`

This signal is useful, but the deeper role of EA_HAQ is modulation, not merely novelty logging.

---

## Current Status

- architecturally justified and active
- role binding
- exact formula still provisional