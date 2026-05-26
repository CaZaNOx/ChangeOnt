---
id: stmt.continuation-admissibility
type: DF
aliases:
  - S-DF-continuation-admissibility
  - ContinuationAdmissibility
title: Continuation admissibility — coarse supportable continuation before graded comparison and before identity-specific preservation
concepts:
  - '[[02_Concepts/C-change-trace-invariants]]'
  - '[[02_Concepts/C-outer-formation-route]]'
dependencies:
  - '[[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]'
  - '[[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]'
parents:
  - '[[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]'
successors:
  - '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
  - '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
  - '[[01_Statements/02_Outer_Formation/018_S-DF-operative-difference.md]]'
  - '[[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]'
symbols_used: []
sources:
  - path: chat/2026-04-04 carried-constraint and admissibility clarification
flags: []
tags:
  - layer/foundations
  - domain/ontological
  - type/DF
  - route/outer
  - concept/change-trace-invariants
  - status/stable
status: stable
---
# Continuation admissibility — coarse supportable continuation before graded comparison and before identity-specific preservation

## Claim (formal)
Given a bounded local hold and an invariant regime, one can already distinguish continuations that remain supportable for the unfolding from continuations that exceed what the unfolding can absorb. This coarse distinction is continuation admissibility.

## Philosophical Translation (of formal claim)
Before asking whether a process remains the same identity, and even before finely grading preservation or burden, one can ask a weaker question: can this unfolding continue at all in a supportable way under the change being imposed on it? Continuation admissibility is that earlier distinction.

## Why this claim is needed
The chain needs a notion weaker than identity preservation but stronger than mere recurrence. Without it, later files cannot sharply discuss:
- burden,
- operative difference,
- or identity-admissibility.

If the route jumps directly to identity, it makes every meaningful threshold a sameness-threshold. But many continuations fail earlier, at the level of supportability itself.

## Philosophical Justification
Invariant regime already gives a stable profile of what a recurrent unfolding preserves, tolerates, repairs, and loses. Bounded local hold says that this supportability question concerns a locally stabilized unit of unfolding rather than an arbitrary global totality. Together they support a first coarse distinction:
- some transformations stay within what the unfolding can still support,
- others push it beyond that supportability.

That is exactly what continuation admissibility names.

## Explanation (informal)
A flame can continue under some changes and fail under others; a path can remain traversable under some deformations and collapse under others. Those are not yet identity questions in the strong sense. They are earlier questions of whether supportable continuation remains available at all.

## Derivation (Philosophical)
- Invariant regime provides the stable profile of preservation, tolerance, and failure.
- Bounded local hold specifies the local unfolding for which that profile is being tracked.
- Therefore one can distinguish transformations that remain supportable for that unfolding from those that exceed its supportability.
- This distinction is continuation admissibility.

## Derivation (Formal/Logical/Mathematical)
```text
Let H be a bounded local hold and R an invariant regime over H.
A continuation T(H) is continuation-admissible iff T(H)
remains within the supportable preservation/tolerance profile specified by R.
```

## Clarifications / Further Context
- This is earlier than identity-admissibility.
- It is earlier than graded burden comparison.
- It is not yet saying "the same thing remains the same."
- It says only that continuation remains supportable for this unfolding.

## Objection 1: “Why not just use identity-preservation directly?”
Because identity is stronger and later. The present file secures the more primitive question of supportable continuation. Identity-specific continuity can then be defined as a narrower special case.

## Objection 2: “Is admissibility just a threshold?”
No. Thresholds may later formalize admissibility, but the concept itself is earlier. It names the ontological distinction between supportable and non-supportable continuation. Finer graded comparison comes next, not first.

## What this file establishes
This file establishes:
1. a pre-identity notion of supportable continuation,
2. admissibility as a real ontological distinction,
3. a coarse supportability cut that later graded comparison may refine.

## What this file does not yet establish
It does **not** yet establish:
- identity-preservation,
- a graded comparison field,
- a fixed numeric threshold,
- or any one formal implementation.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]
- suggest: [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]
- suggest: [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]

## Tags
#type/DF #layer/foundations #domain/ontological #route/outer #concept/change-trace-invariants #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field]]
- [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]
- [[01_Statements/02_Outer_Formation/018_S-DF-operative-difference]]
- [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]; [[02_Concepts/C-outer-formation-route]]
- Parents: [[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold.md]]; [[01_Statements/02_Outer_Formation/011_S-DF-invariant-regime.md]]
- Successors: [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]; [[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]; [[01_Statements/02_Outer_Formation/018_S-DF-operative-difference.md]]; [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]
<!-- END:AUTOGEN:RELATIONSHIPS -->
