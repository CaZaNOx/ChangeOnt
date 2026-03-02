# docs/code_reference/agents/co/core/combinators.md

# CO Combinators

## Purpose

Combinators define how kernel parts are related and composed.

There are two broad kinds:
- semantic/local combinators
- runtime/orchestration combinators

---

## Why they exist

CO does not treat primitive presence alone as sufficient meaning.

Relation form matters.

Examples:
- additive
- subtractive
- multiplicative
- divisive
- gated
- thresholded
- order-sensitive
- staged/hierarchical

Combinators make these relation forms explicit.

---

## Semantic/local combinators

These are used inside elements or local fusion/grouping behavior.

### Expected examples
- additive blend
- multiplicative coupling
- gated threshold
- weighted selection

### Role
They implement local mechanism semantics.

### Status guidance
These are usually closer to **Binding runtime support** if actively used by the kernel.

---

## Runtime/orchestration combinators

These shape or support broader runtime behavior.

Examples may include:
- pipeline orchestration
- gate/routing structures
- transform chains
- math-policy-like controllers

### Role
They help determine how the overall runtime flow is organized.

### Status guidance
These must be clearly documented as:
- active canonical,
- optional canonical,
- experimental,
- or legacy/inactive.

---

## Target-state fusion rule

**Binding**

The canonical fusion architecture is hierarchical staged fusion.

Within that architecture, the allowed local fusion laws are:
- weighted additive
- gated selective
- order-sensitive sequential

If additional combinators exist, their status must be explicit.

---

## Misalignment examples

Combinator documentation is incomplete or code is misaligned if:
- relation forms are hidden inside element code with no explicit contract,
- runtime combinators exist but are bypassed by the active runtime path,
- or additive behavior is silently treated as the only allowed semantics.