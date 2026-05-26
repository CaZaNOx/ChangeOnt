---
id: stmt.boundary-before-identity
type: DR
aliases:
- BoundaryBeforeIdentity
title: Boundary before identity — identity must be tested over a bounded hold
concepts:
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]'
- '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]'
successors:
- '[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md]]'
- '[[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]'
symbols_used: []
sources:
  - path: chat/2026-03-24 clarification on semiring continuity, border, and identity
flags: []
tags:
- layer/foundations
- domain/ontological
- derivation
- border
- identity
- type/DR
- concept/identity-change
- route/outer
status: stable
---
# Boundary before identity — identity must be tested over a bounded hold
## Claim (formal)
A change-first ontology must derive bounded local hold before token-like identity, because identity claims require a domain over which continuity can be tested.

## Philosophical Translation (of formal claim)
Before we can say “this is still the same,” we need a bounded locus over which “still” can even be evaluated. Identity cannot come first.

## Philosophical Justification
A major risk for the chain is smuggling in ready-made objecthood. [[009_S-DF-bounded-local-hold]] already shows that what is first available is a bounded live hold, not a finished thing. [[012_S-DF-continuation-admissibility]] then gives the language of supportable continuation over such a hold. Therefore identity must be later: it is a property tested over a bounded region, not the primitive generator of the region.

## Explanation (informal)
This is the anti-smuggling order. First there is a bounded local hold; only then can continuity or identity be assessed over it.

## Derivation (Philosophical)
- A local hold is bounded before it is object-like.
- Continuity/admissibility requires something bounded over which continuation can be assessed.
- Therefore identity comes later than bounded local hold.

## Derivation (Formal/Logical/Mathematical)
```text
BoundedLocalHold -> admissible continuity tests over that hold -> identity criteria
```

## Clarifications / Further Context
- This node no longer depends on identity-through-change itself; that circularity has been removed.
- The point is doctrinal order, not yet a full theory of identity recognition.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md]]

## Tags
#type/DR #layer/foundations #domain/ontological #route/outer #border #identity #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]; [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]
- Successors: [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md]]; [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

