# Combinator Role

## Purpose

This page defines what a **semantic combinator** is in the ChangeOnt kernel.

It is binding for future combinator design.

---

## Definition

A semantic combinator is a **reusable law-form for composing primitive outputs**.

A combinator does not introduce a new primitive.  
It specifies how primitives influence one another inside an element.

Examples:
- additive composition
- multiplicative composition
- gated composition
- weighted blending
- thresholded composition
- CO-native composition laws

---

## Why combinators matter

A primitive may be meaningful while its law of interaction remains unknown.

For example:
- a quantity may plausibly exist
- but whether it should act additively, multiplicatively, by division, gating, or another operator may still be under investigation

Combinators are the architectural place where those law-forms live.

---

## Binding requirements

A semantic combinator:
- exists only once in code
- is reusable across elements
- must be explicit
- must be loggable/configurable
- must not smuggle task-specific logic
- must not be hidden inside element-local ad hoc formulas

---

## Semantic combinators vs runtime combinators

This repo already contains runtime orchestration components such as `C_Pipeline`.

These are **runtime combinators**, not semantic combinators.

- **Semantic combinators** define law-forms of primitive interaction.
- **Runtime combinators** define execution order and runtime flow.

These categories must remain distinct.

---

## Design consequence

Elements should eventually declare:
- which primitives they use
- which semantic combinators they use
- which weights/roles they assign

This prevents element files from becoming opaque custom formula bags.