# Semantic Combinators Overview

## Purpose

This folder defines the missing middle layer between:
- primitives
- elements

A semantic combinator specifies **how primitive outputs are related, composed, gated, or weighted** inside an element.

Without this layer, the architecture collapses into:
- primitives as loose variables
- elements as hidden ad hoc formulas

That is exactly what this folder is meant to prevent.

---

## Why this layer exists

The project does not claim that primitives alone are enough.

A primitive like:
- bend
- gauge
- precision
- loopiness
- complexity pressure

does not yet tell us how these should interact.

The missing question is:

- additive?
- multiplicative?
- thresholded?
- gated?
- weighted?
- dominance-switched?
- stabilizing vs destabilizing?

Semantic combinators are the layer where those relations are specified.

---

## Layer Role

A semantic combinator is:

- not a primitive
- not an element
- not a header
- not a translator
- not a runtime combinator

It is a **law-form** for primitive interaction.

In rough analogy:

- primitives are the reusable variables/ingredients
- semantic combinators are the forms of relation between them
- elements are meaningful grouped mechanisms built from primitives through those combinators

---

## Why this matters philosophically

The ontology does not just need named ingredients.
It needs a plausible story for how change-related ingredients interact.

If change gives us:
- bend
- recurrence
- grouping
- branching
- convergence
- precision

then we still need to know:

- when does one modulate another?
- when does one gate another?
- when does one dominate another?
- when are two pressures added vs multiplied?

This is not implementation detail.
It is part of the mechanistic doctrine.

---

## Current v1 Position

In v1, semantic combinators are being introduced at the doc/spec level first.

That means:

- the architecture now recognizes them explicitly
- current code may still implement some of them only implicitly
- future code should move toward explicit primitive -> combinator -> element structure

---

## Minimal v1 combinator set

The minimal reusable combinator families are:

1. Additive blend
2. Multiplicative coupling
3. Gated threshold
4. Weighted selection

This is not necessarily the final set, but it is enough to stop uncontrolled drift.

---

## Binding Rule

Every element spec should eventually say not only:
- which primitives it uses

but also:
- which semantic combinator forms it uses

If that is absent, the element spec is incomplete.

---

## Relation to runtime combinators

Do not confuse semantic combinators with runtime combinators.

### Runtime combinators
Examples:
- pipeline orchestration
- update-vs-decision separation
- bus routing

### Semantic combinators
Examples:
- additive interaction of novelty and density
- thresholded birth rule
- multiplicative modulation of identity by precision

The former controls execution.
The latter controls meaning/mechanism.

---

## Current architectural conclusion

The semantic combinator layer is now a required part of the intended architecture.

Even if implementation is still partial, future work should follow:

primitive -> semantic combinator -> element -> bus/header/action