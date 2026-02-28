# EG_DensityPrecision

## Purpose

EG_DensityPrecision is the kernel’s local density / revisit / precision-sensitive hint mechanism.

Its role is to emit continuous information about local saturation, revisit density, or coarse-graining pressure.

---

## Element Role

EG_DensityPrecision is an **element**.

It is not:
- a primitive
- a header
- a translator
- the final action surface

It is a semantically meaningful continuous-hint mechanism.

---

## Intended Primitive Dependencies

Primary intended dependencies:
- P7_Precision

Secondary:
- local visit-density support
- possible later gauge modulation

---

## Intended Semantic Combinator Form

Primary:
- **SC_AdditiveBlend**

Secondary:
- **SC_MultiplicativeCoupling** later if modulation becomes explicit

---

## Why these belong together

Density/precision style information usually contributes as continuous pressure rather than hard admission.

That makes additive accumulation the right v1 law-form:
- revisit pressure
- local density
- local coarse-graining hints

can accumulate into one hint signal.

---

## Inputs

EG_DensityPrecision may consume:
- local visit information
- local recurrence counts
- precision/coarse-graining support
- bounded local state

---

## Outputs

Typical output:
- `signals["EG_DensityPrecision.visit_density"]`

Other density/precision-facing signals may be added only if documented.

---

## State Mutation

EG_DensityPrecision may maintain:
- local visit tracking state
- bounded density counters

It must not directly choose actions.

---

## Why this element exists

Some regions of unfolding become:
- dense
- repeatedly visited
- saturated
- locally over-familiar

That is semantically relevant, but not usually as a hard birth/identity event.
It is better treated as continuous hint pressure.

---

## Forbidden

EG_DensityPrecision must not:
- become a translator in disguise
- directly choose final actions
- pretend density itself is the whole ontology
- silently absorb unrelated primitive logic

---

## Telemetry

Typical canonical signal:
- `EG_DensityPrecision.visit_density`

---

## Current Status

- active and useful
- role binding
- exact formula still provisional