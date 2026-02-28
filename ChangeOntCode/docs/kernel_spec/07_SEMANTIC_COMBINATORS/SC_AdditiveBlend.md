# SC AdditiveBlend

## Purpose

SC_AdditiveBlend defines the semantic relation-form in which multiple primitive pressures contribute by **accumulation**.

This is the simplest combination law:
- one contribution plus another contribution

---

## Combinator Role

SC_AdditiveBlend is a semantic combinator.

It is used when multiple primitive outputs are treated as:
- co-contributing
- jointly accumulating
- independently relevant pressures

It is not a claim that the world is literally “plus”.
It is the current reusable law-form for accumulated influence.

---

## Inputs

SC_AdditiveBlend may combine:
- two or more primitive-derived scalars
- optionally with explicit weights

Generic form:
- `sum_i (w_i * x_i)`

---

## Outputs

It returns:
- one combined scalar or score

This output may then be used by an element.

---

## State Mutation

SC_AdditiveBlend should be pure.

---

## Why this combinator exists

Some primitive pressures are plausibly co-present without one needing to gate the other.

Examples:
- novelty pressure plus density penalty
- recurrence pressure plus complexity cost
- multiple weak pressures accumulating into one stronger one

In such cases, additive accumulation is a reasonable first law-form.

---

## When to use it

Use SC_AdditiveBlend when:
- primitive contributions are interpreted as jointly present
- no hard gating is intended
- one primitive does not annihilate the semantic relevance of another

---

## When not to use it

Do not use SC_AdditiveBlend when:
- one quantity should gate whether another matters at all
- one quantity should rescale another rather than merely add
- one primitive should dominate competitively

---

## Forbidden

SC_AdditiveBlend must not:
- be treated as the only valid relation-form
- directly choose final actions
- become task-specific

---

## Likely usage

Likely element consumers include:
- EA_HAQ
- EG_DensityPrecision
- EB_GHVC in some partial laws

---

## Current Status

Binding reusable combinator class for v1.