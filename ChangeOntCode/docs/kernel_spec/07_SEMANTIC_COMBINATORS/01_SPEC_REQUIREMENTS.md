# Semantic Combinator Spec Requirements

## Purpose

This page defines what every semantic combinator spec file must contain.

It is binding for all files in `07_SEMANTIC_COMBINATORS/`.

---

## Definition Reminder

A semantic combinator defines a **relation-form** between primitive outputs.

It is not:
- a primitive
- an element
- a header
- a translator
- a runtime orchestration unit

---

## Every semantic combinator spec must contain

### 1. Purpose
State what kind of relation-form this combinator represents.

Examples:
- additive composition
- multiplicative modulation
- threshold gating
- weighted competition/selection

### 2. Combinator Role
State clearly why this is a semantic combinator rather than a primitive or element.

### 3. Inputs
State what kinds of primitive outputs it may combine.

### 4. Outputs
State what kind of result it returns.

Examples:
- scalar combination
- gated result
- selected dominant signal
- weighted composite

### 5. State Mutation
Most semantic combinators should be pure.
If not, the reason must be explicit.

### 6. Why this combinator exists
State the philosophical/mechanistic reason why this relation-form is plausible.

### 7. Forbidden
State what the combinator must not do.

Examples:
- choose final task actions
- become task-specific
- silently absorb translator logic
- claim to be a primitive

### 8. Usage Pattern
State which kinds of elements would plausibly use it.

### 9. Current Status
State whether the combinator is:
- binding and reusable now
- provisional but justified
- future/reserved

---

## Most Important Rule

A semantic combinator spec must answer:

**Why should these primitive quantities interact in this form rather than another form?**

If it does not answer that, it is incomplete.

---

## Anti-Patterns

A semantic combinator spec is wrong if it:

- is just a math operator with no architectural meaning
- is secretly an element formula
- is task-specific
- directly chooses actions
- pretends one relation-form is final truth without admitting alternatives where appropriate

---

## Reviewer Checklist

A semantic combinator spec is complete only if a reviewer can answer:

- What relation-form is this?
- Why is that relation-form plausible?
- What kinds of primitive outputs can it combine?
- What does it return?
- What must it not do?
- Which elements would use it?