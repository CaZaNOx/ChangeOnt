# EB_GHVC
Current classification: **Provisional**

Active birth/admission element, but still philosophically less settled than the strongest core.

## Purpose

EB_GHVC is the kernel’s birth/admission mechanism.

Its role is to determine when local pressure is strong enough that the current structure should admit a new prototype / new structured distinction.

---

## Element Role

EB_GHVC is an **element**.

It is not:
- a primitive
- a translator
- a header
- the final action surface

It is the mechanism that decides whether structural admission should occur.

---

## Intended Primitive Dependencies

Primary intended dependencies:
- P3_MDL
- P10_ChangeOpsCore

Secondary / optional:
- P12_ClosureQuotient

---

## Intended Semantic Combinator Form

Primary:
- **SC_GatedThreshold**

Secondary:
- **SC_AdditiveBlend**

---

## Why these belong together

EB_GHVC is not a continuous accumulation-only mechanism.

Its core doctrine is:

- pressure may build
- complexity pressure may matter
- but structural admission should occur only once some sufficient condition is met

That means its primary law-form is threshold gating.

Some internal scoring may still be additive, but the element’s defining feature is **admission by threshold**, not additive contribution alone.

---

## Inputs

EB_GHVC may consume:
- residual/probe-derived pressure
- feedback-derived pressure proxy
- complexity / MDL-related quantity
- optional budget/admission constraints

---

## Outputs

Canonical outputs include:
- `signals["EB_GHVC.pressure"]`
- `signals["EB_GHVC.mdl_gain"]`
- `signals["EB_GHVC.birth_suggest"]`

Possible top-level telemetry includes:
- `birth_events`
- `birth_count`
- `prototype_count`
- `class_count`
- `merge_events`
- `split_events`
- `cap_hits`

---

## State Mutation

EB_GHVC may mutate:
- canonical prototype support via P10
- canonical monotonic birth counter

Optional closure/grouping interaction may exist only if explicitly documented and kept architecturally disciplined.

EB_GHVC must not become a general-purpose state mutation sink.

---

## Why this element exists

A change-native ontology should not assume that every fluctuation instantly becomes a new stable structured distinction.

There must be some doctrine of:
- pressure
- admissibility
- birth threshold

EB_GHVC is that doctrine in v1.

---

## Forbidden

EB_GHVC must not:
- directly choose final actions
- silently absorb translator logic
- become an unrestricted “spawn whatever” mechanism
- hide birth conditions from docs

---

## Telemetry

Required canonical signals:
- `EB_GHVC.pressure`
- `EB_GHVC.mdl_gain`
- `EB_GHVC.birth_suggest`

---

## Current Status

- active and central
- role binding
- threshold/admission structure binding
- exact score formula still provisional

---

## Element Charter

### Domain
Consumes (standard packet):
- `residuals`, `probes` (structural mismatch diagnostics)
- `feedback.reward` (diagnostic/proxy pressure only; not a rescue selector)
- `t` (time for cooldown)
- optional `budget` object

### Codomain
Emits typed roles:
- **branch/birth proposal** (primary)

Canonical signals:
- `EB_GHVC.pressure`
- `EB_GHVC.mdl_gain`
- `EB_GHVC.birth_suggest`

And an auditable proposal stream in `primitives['_branch_proposals']`.

### Invariants
- **No free birth**: if `pressure < birth_threshold` then `birth_suggest` must be 0.
- **No negative justification**: if `mdl_gain <= 0` then `birth_suggest` must be 0.
- **Cooldown**: births cannot happen more frequently than `cooldown` steps (unless cooldown disabled).
- **Auditability**: every suggested birth must be recorded in `_branch_proposals` (no silent births).

### Falsifiers
- births occur under low pressure or non-positive mdl_gain.
- births occur repeatedly despite cooldown.
- EB produces only scalar “pressure” with no proposal/audit trail.

### Interaction expectations
- With **EC**: high fracture pressure should increase plausibility of birth; high continuity should suppress it.
- With **EA**: sustained EA pressure without stable identity may support birth gating, but EA must not directly trigger births.