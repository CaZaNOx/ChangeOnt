# C_Pipeline

## Purpose

`C_Pipeline` is the canonical **runtime combinator** for kernel execution flow.

It is not the full semantic combinator layer.

Its job is to orchestrate:
- update pass
- decision pass
- order of runtime calls

---

## Runtime Role

`C_Pipeline` defines the current canonical runtime flow:
- which components are called on update
- which components are called on decision
- when header update is allowed
- when ActionHead is called

This is runtime orchestration, not a semantic law-form between primitives.

---

## Binding Rules

### Update ownership
- header updates occur only in `run_update`
- decision pass must not call `header.update`

### Action ownership
- ActionHead is called only on decision path
- update path must not become a hidden action path

### Order
- non-ActionHead elements may update/emit before ActionHead
- votes/signals must be available before ActionHead finalization

---

## What C_Pipeline is not

`C_Pipeline` is not:
- a primitive
- a semantic combinator
- an element
- the place where ontology law-forms are defined

It is the runtime orchestration surface.

---

## Future relation to semantic combinators

Future semantic combinators may live in the same general code area, but must remain conceptually distinct from runtime orchestration components like `C_Pipeline`.

This distinction is binding.