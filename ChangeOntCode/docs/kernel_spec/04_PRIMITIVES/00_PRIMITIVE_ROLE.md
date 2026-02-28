# Primitive Role

## Purpose

This page defines what a primitive is in the ChangeOnt kernel.

It is binding for all primitive docs and implementations.

---

## Definition

A primitive is a **minimal reusable operational encoding of a structurally recurring demand** that arises when trying to think consistently from change.

Primitives are not claimed to be final or uniquely deduced formulas.

They are current candidate semantic ingredients.

---

## What primitives are for

Primitives exist to encode things like:
- bend / difference
- closure pressure
- gauge / modulation
- precision / scale
- recurrence / loopiness
- branching / convergence support
- topology / neighborhood support
- persistence / memory support

A primitive is introduced because it appears to be:
- semantically meaningful
- reusable across multiple elements
- not reducible to a purely task-specific trick

---

## What primitives are not

A primitive is not:
- a full mechanism hypothesis
- an element
- a task-specific heuristic
- a translator rule
- a final action policy

---

## Binding requirements

A primitive:
- exists only once in code
- may expose state and/or operations
- may be reused by many elements
- must not contain task-specific logic
- must not directly choose final actions
- must not silently depend on hidden runtime context

---

## Research status

Primitives are **derivationally motivated candidates**, not guaranteed final truths.

Derivation from change does not instantly produce a full final mechanics.

Instead, it constrains the plausible space of operations and behaviors.

Primitives are introduced as minimal reusable encodings of those constraints.

---

## Design consequence

If the same semantic quantity or operation is needed in multiple places:
- it should live in a primitive
- not be re-implemented inside multiple elements

If a proposed primitive is actually a full mechanism or event-pattern:
- it may belong at the element layer instead