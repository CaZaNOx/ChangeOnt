# Primitive and Element Composition

## Status
- **Binding**: primitives are reusable CO basis terms
- **Binding**: elements are doctrine-level compositions over those basis terms
- **Binding**: weights, transforms, and configure-time parameters are part of the mechanism, not decoration

## 1. Principle

Primitives are reusable structural lenses.
Elements combine them into doctrine-level behavior.

Not every execution-relevant philosophical principle becomes a primitive. Some principles belong to:
- runtime invariants / update discipline
- the kernel substrate / field state
- support surfaces
Only those that need reusable kernel-resolution handles should be packaged as primitives.

A meaningful element difference may come from:
- primitive choice
- primitive weighting
- transform law
- thresholding/gating
- memory/update law
- output publication strategy

This is why `ea1`, `ea2`, etc. must be able to differ honestly at runtime.

## 2. Runtime liveness rule

If docs claim a primitive weight, transform, or threshold is configurable, the runtime must honor it.

A config parameter that never reaches the live instance is a spec violation.

## 3. Contribution rule

In active v1, elements contribute through one or more of:
- returned metrics
- published bus signals
- optional direct votes

Not every element must do all three.
But the docs must state which channel is authoritative for that element.

## 4. Family-neutrality rule

Primitive/element meaning must be family-neutral.
Families differ only in:
- what they can honestly expose in the standard packet
- how a continuation surface is collapsed into native action space

If an element only works in one family because another family failed to expose the same visible structure in standard form, that is an integration bug, not an ontology truth.

## 5. Misalignment examples

Misalignment exists if:
- weights/combinators are documented but ignored at runtime
- element semantics are actually hidden in family translators
- one family receives richer standard packet structure only because the adapter was written more carefully
- variant configs differ in YAML but not in live behavior
