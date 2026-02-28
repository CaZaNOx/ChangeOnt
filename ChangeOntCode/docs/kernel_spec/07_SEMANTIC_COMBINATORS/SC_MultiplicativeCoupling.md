# SC MultiplicativeCoupling

## Purpose

SC_MultiplicativeCoupling defines the semantic relation-form in which one primitive pressure **rescales** another.

This is used when a primitive does not merely add influence, but changes the effective strength of another quantity.

---

## Combinator Role

SC_MultiplicativeCoupling is a semantic combinator.

It is used when one primitive behaves like:
- amplifier
- attenuator
- modulator
- coupling factor

Generic form:
- `x * y`
- or weighted variants thereof

---

## Inputs

SC_MultiplicativeCoupling may combine:
- two or more primitive-derived scalars
- usually where at least one serves as modulator/coupler

---

## Outputs

It returns:
- one coupled scalar

This output may be used by an element.

---

## State Mutation

SC_MultiplicativeCoupling should be pure.

---

## Why this combinator exists

If change modulates change, then some quantities may not just accumulate; they may alter the force of other quantities.

Examples:
- precision modulating identity sensitivity
- gauge modulating novelty
- recurrence modulating exploration pressure

This is philosophically distinct from mere addition.

---

## When to use it

Use SC_MultiplicativeCoupling when:
- one quantity changes the effective strength of another
- a modulation story is intended
- additive accumulation would be too weak or semantically wrong

---

## When not to use it

Do not use SC_MultiplicativeCoupling when:
- contributions are just independent and accumulating
- the real mechanism is thresholding/gating
- selection/competition is the intended behavior

---

## Forbidden

SC_MultiplicativeCoupling must not:
- be treated as universal by default
- hide task-specific heuristics
- directly choose final actions

---

## Likely usage

Likely element consumers include:
- EA_HAQ
- EC_Identity
- EG_DensityPrecision

---

## Current Status

Binding reusable combinator class for v1.