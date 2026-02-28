# EC_Identity

## Purpose

EC_Identity is the kernel’s local continuity / identity mechanism.

Its role is to determine whether current unfolding remains within an admitted sameness class under bounded bend difference.

---

## Element Role

EC_Identity is an **element**.

It is not:
- a primitive
- a translator
- a header
- the action surface

It is the mechanism of local identity judgment.

---

## Intended Primitive Dependencies

Primary intended dependencies:
- P1_BendMetric

Secondary / optional:
- P12_ClosureQuotient
- later modulation influences from P2/P7 if identity strictness becomes dynamically coupled

---

## Intended Semantic Combinator Form

Primary:
- **SC_GatedThreshold**

Secondary:
- **SC_MultiplicativeCoupling** later if identity strictness is modulated

---

## Why these belong together

Identity here is not metaphysical absolute identity.

It is local admitted continuity under bounded difference.

That means the core law-form is threshold gating:

- if bend distance remains within threshold, continuity is admitted
- otherwise identity break pressure appears

This is the correct v1 form.

---

## Inputs

EC_Identity may consume:
- current short trace/history
- previous trace memory
- bend threshold / effective epsilon
- optional later modulation inputs

---

## Outputs

Canonical outputs:
- `signals["EC_Identity.same"]`
- `signals["EC_Identity.last_d"]`

Possible additional telemetry:
- `bend_triggers`

---

## State Mutation

EC_Identity may mutate:
- canonical bounded identity memory

It must not mutate:
- task translator state
- final action state
- header ownership

---

## Why this element exists

A change-native system still needs a doctrine of when something counts as “the same enough” to preserve local structure.

EC_Identity is that doctrine in minimal v1 form.

---

## Forbidden

EC_Identity must not:
- directly choose final actions
- pretend identity is primitive static sameness
- silently absorb closure/grouping doctrine unless documented
- become a translator-side heuristic

---

## Telemetry

Required canonical signals:
- `EC_Identity.same`
- `EC_Identity.last_d`

---

## Current Status

- active and central
- bend-threshold continuity structure binding
- richer identity doctrine still future/provisional