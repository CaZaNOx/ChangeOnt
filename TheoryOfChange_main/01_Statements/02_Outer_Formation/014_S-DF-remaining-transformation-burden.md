---
id: stmt.remaining-transformation-burden
type: DF
aliases:
  - S-DF-remaining-transformation-burden
  - RemainingTransformationBurden
  - ReachabilityDeficit
  - AdmissibilityDeficit
title: Remaining transformation burden / reachability deficit
concepts:
  - '[[02_Concepts/C-change-trace-invariants]]'
  - '[[02_Concepts/C-outer-formation-route]]'
dependencies:
  - '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
  - '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
parents:
  - '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
  - '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
successors:
  - '[[01_Statements/Definition/S-DF-prm-residuation]]'
  - '[[01_Statements/Definition/S-DF-prm-reid-kernel]]'
  - '[[01_Statements/02_Outer_Formation/018_S-DF-operative-difference.md]]'
symbols_used: []
sources:
  - path: chat/2026-04-01 clarification that the deeper issue behind residuation is what remains for one local configuration to become another
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
# Remaining transformation burden / reachability deficit

## Claim (formal)
Once local continuations can be compared and supportable continuation is distinguished from non-supportable continuation, one can meaningfully speak of what still has to change for a present local unfolding to reach a target supportable state. This is remaining transformation burden.

## Philosophical Translation (of formal claim)
The theory now needs a way to say not only what has been transformed, but what transformation is still missing. Remaining transformation burden names the not-yet-accomplished side of becoming.

## Why this claim is needed
Without this node, the chain can say:
- some continuations are supportable,
- some preserve more than others,

but it still cannot say:
- how far a current unfolding remains from entering a target supportable region,
- or why some differences are more operative than others.

Later files on operative difference, operative invariants, and some kernel primitives depend on exactly this "still-to-be-done" notion.

## Philosophical Justification
Continuation admissibility supplies the target side: whether a continuation remains supportable. Local comparability field supplies the graded relation of preservation, loss, and strain. Once both are in place, it is legitimate to ask:
- given the current unfolding,
- and given some supportable target region,
- what burden remains for the present unfolding to reach it?

That question is not merely pragmatic. It is ontological for a change-first theory, because change is not exhausted by what has already occurred; it also includes the deficit between the present state of transformation and the target state required for supportable continuation.

## Explanation (informal)
This is the philosophical core behind later notions like cost-to-go, reachability deficit, or residuation. The present file does not yet privilege one formalism. It secures the underlying idea: an unfolding can still owe transformation relative to some target supportable configuration.

## Derivation (Philosophical)
- A supportable target region can be specified by continuation admissibility.
- A present unfolding can be compared to other transformations by local comparability.
- Therefore the present unfolding can stand at a greater or lesser remove from a target supportable region.
- The amount and kind of change still required is remaining transformation burden.

## Derivation (Formal/Logical/Mathematical)
```text
Let x be current unfolding.
Let A(y) be a target admissible region.
Let C*(x, A(y)) express the comparative transformation relation from x toward A(y).
Then remaining burden B_rem(x -> A(y))
tracks what still must change for x to enter A(y).
```

## Clarifications / Further Context
- This is earlier than any single numerical cost function.
- It is earlier than any specific algebra such as residuation.
- It is also earlier than identity-specific burden, though later identity-continuity claims may specialize it.

## Objection 1: “Isn’t this just future-oriented pragmatics?”
No. The concept is ontological before it is practical. A change-first ontology must be able to say that present becoming may still be incomplete relative to a target supportable regime. That incompleteness is real whether or not an agent computes it explicitly.

## Objection 2: “Why not define burden only after metric distance?”
Because the chain has already earned weaker comparability and supportability. Burden can therefore be earned before a stronger geometric packaging is available.

## What this file establishes
This file establishes:
1. the not-yet-accomplished side of transformation,
2. burden as a real feature of becoming, not just an engineering convenience,
3. the immediate precursor to operative relevance and later formal burden packages.

## What this file does not yet establish
It does **not** yet establish:
- one specific numerical burden law,
- one specific algebra,
- or a fully identity-specific continuity burden.

## Next Steps in Chain
- suggest: [[01_Statements/02_Outer_Formation/018_S-DF-operative-difference.md]]
- suggest: [[01_Statements/Definition/S-DF-prm-residuation]]

## Tags
#type/DF #layer/foundations #domain/ontological #route/outer #concept/change-trace-invariants #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility]]
- [[01_Statements/Definition/S-DF-prm-residuation]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]; [[02_Concepts/C-outer-formation-route]]
- Parents: [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]; [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]
- Dependencies: [[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]; [[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]
- Successors: [[01_Statements/Definition/S-DF-prm-residuation]]; [[01_Statements/Definition/S-DF-prm-reid-kernel]]; [[01_Statements/02_Outer_Formation/018_S-DF-operative-difference.md]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

