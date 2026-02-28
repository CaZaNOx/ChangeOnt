# SC WeightedSelection

## Purpose

SC_WeightedSelection defines the semantic relation-form in which multiple candidate primitive-derived pressures or mechanism outputs compete under weighted comparison.

This is the law-form for:
- weighted dominance
- weighted preference
- competition among alternatives

---

## Combinator Role

SC_WeightedSelection is a semantic combinator.

It is used when the doctrine is:
- not simple addition
- not simple modulation
- not just thresholding

but instead:
- alternative pressures compete and one or some subset dominate

---

## Inputs

SC_WeightedSelection may consume:
- candidate scalars or scores
- explicit weights
- optional constraints or admissibility masks

---

## Outputs

It returns:
- selected dominant signal
- weighted preference ordering
- selected winner or weighted shortlist

---

## State Mutation

SC_WeightedSelection should generally be pure.

---

## Why this combinator exists

Not all change-derived pressures should necessarily co-exist symmetrically.

Sometimes:
- one mechanism should dominate in a regime
- one pressure should win against another
- local control should prefer one semantic line over another

This makes weighted competition a plausible relation-form.

---

## When to use it

Use SC_WeightedSelection when:
- multiple alternatives compete
- dominance/preference is intended
- ranking/selection matters

---

## When not to use it

Do not use SC_WeightedSelection when:
- the real story is additive accumulation
- the real story is threshold activation
- the real story is multiplicative modulation

---

## Forbidden

SC_WeightedSelection must not:
- become final task action selection by itself
- silently replace ActionHead
- hide task-specific policy choices

---

## Likely usage

Likely element or control consumers include:
- EH_BreadthDepth
- future routing/control mechanisms
- meta-control layers

---

## Current Status

Binding reusable combinator class for v1.