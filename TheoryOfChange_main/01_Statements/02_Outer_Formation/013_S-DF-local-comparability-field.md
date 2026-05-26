---
id: stmt.local-comparability-field
type: DF
aliases:
  - S-DF-local-comparability-field
  - COT_4.LocalComparabilityField
title: Local comparability field — graded preservation, loss, and strain after coarse admissibility but before metric packaging
concepts:
  - '[[02_Concepts/C-change-trace-invariants]]'
  - '[[02_Concepts/C-outer-formation-route]]'
dependencies:
  - '[[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]'
  - '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
parents:
  - '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
successors:
  - '[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]'
  - '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
  - '[[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator.md]]'
symbols_used:
  - '[[01_Statements/SYMBOLS/Distance]]'
  - '[[01_Statements/SYMBOLS/Theta]]'
sources:
  - path: chat/2026-03-31 strict traversal fix introducing a weaker comparability-field step before metric-like strengthening
flags: []
tags:
  - layer/foundations
  - domain/mathematical
  - type/DF
  - route/outer
  - concept/change-trace-invariants
  - status/stable
status: stable
---
# Local comparability field — graded preservation, loss, and strain after coarse admissibility but before metric packaging

## Claim (formal)
Once coarse continuation admissibility is available, transformations within a bounded unfolding can be compared more finely by how much they preserve, lose, or strain that unfolding. This yields a local comparability field prior to full metric geometry.

## Philosophical Translation (of formal claim)
Before the theory has earned distance in the stronger mathematical sense, it can already say something weaker but still meaningful: among supportable and near-supportable continuations, some preserve more than others, some distort less, and some impose more strain. That disciplined earlier comparison is a local comparability field.

## Why this claim is needed
Later files need a way to talk about:
- better and worse preservation,
- more and less strain,
- graded difference inside the supportability domain,
- and remaining burden.

Without this node, those later distinctions would either remain purely verbal or would smuggle in a metric too early.

## Philosophical Justification
The chain already has two ingredients.

1. **Invariant regime** gives a stable profile of what the unfolding preserves, tolerates, repairs, and loses.
2. **Continuation admissibility** gives the earlier coarse distinction between supportable and non-supportable continuation.

Once both are granted, the route can ask a finer question: not only whether a continuation remains supportable, but how it compares to other continuations in preservation, loss, and strain. That finer but still pre-metric ordering is a local comparability field.

## Explanation (informal)
This is the first genuinely mathematical-looking node in the outer route, but it is intentionally weak. It does not claim Euclidean distance, symmetric metric structure, or global geometry. It claims only that local continuations can be comparatively ordered by preservation and strain.

## Derivation (Philosophical)
- Invariant regime specifies what counts as preservation, tolerance, and failure for a bounded unfolding.
- Continuation admissibility already separates supportable from non-supportable continuation.
- Therefore different continuations can now be graded more finely with respect to preservation, loss, and strain.
- This yields a local comparability field.

## Derivation (Formal/Logical/Mathematical)
```text
Given bounded unfolding H, invariant regime R over H,
and coarse admissibility distinction A_cont,
one may define a local field C*(x,y)
that orders continuations by preservation / loss / strain
without yet requiring full metric axioms.
```

## Clarifications / Further Context
- The `Distance` symbol here should be read historically and cautiously.
- What is earned first is not full distance but weaker comparability.
- A stronger metric-like articulation is a later optional strengthening.
- Similarity in the identity branch is later and narrower than this general comparability field.

## Objection 1: “Why not introduce metric distance directly?”
Because the chain has not yet earned the stronger properties of metric space. It has earned only a weaker local ordering of preservation, loss, and strain.

## Objection 2: “Isn't similarity already doing this work later?”
Similarity is later and narrower. It specializes graded comparison to the identity branch and to retained-versus-altered comparison of bounded continuing lines. Comparability is earlier and more general.

## What this file establishes
This file establishes:
1. local continuations can be graded comparatively,
2. preservation/loss/strain can be ordered before metric geometry,
3. later burden and similarity talk has a justified comparison base.

## What this file does not yet establish
It does **not** yet establish:
- full distance,
- metric symmetry,
- triangle inequality,
- or global geometry.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]
- suggest: [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator.md]]
- suggest: [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]

## Active-chain status
**Status band:** derived-but-weaker  
**Reason:** the chain earns disciplined local comparison after coarse admissibility but before stronger distance geometry.

## Tags
#type/DF #layer/foundations #domain/mathematical #route/outer #concept/change-trace-invariants #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]
- [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]; [[02_Concepts/C-outer-formation-route]]
- Parents: [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]; [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]
- Successors: [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]; [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]; [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator.md]]
<!-- END:AUTOGEN:RELATIONSHIPS -->
