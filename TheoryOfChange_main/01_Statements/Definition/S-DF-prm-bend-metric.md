---
id: stmt.prm-bend-metric
type: DF
aliases:
- PRM_1
- BendMetric
- P1
title: Bend metric as directional deformation burden
concepts:
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]'
- '[[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold]]'
parents:
- '[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]'
successors:
- '[[01_Statements/Definition/S-DF-prm-reid-kernel]]'
- '[[01_Statements/Definition/S-DF-prm-gauge]]'
symbols_used:
- '[[01_Statements/SYMBOLS/Beta]]'
- '[[01_Statements/SYMBOLS/Distance]]'
sources:
- path: TheoryOfChange/02_Foundations/DerChain.md
flags: []
tags:
- layer/kernel
- domain/ontological
- type/DF
- status/stable
- strand/ontological
---
# Bend metric as directional deformation burden
## Claim (formal)
Bend is the primitive deformation burden between local continuations within a metric-like comparability field. It is not deviation inside a pre-given neutral geometry, but the directional cost or burden of transforming one continuation into another.

## Philosophical Translation (of formal claim)
If change is primary, then difference is first something like deformation burden, not neutral geometric spacing. Bend measures how much a continuation must be altered to become another, and this burden may be directional.

## Philosophical Justification
[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]] only earns a comparability/cost field, not a finished classical metric background. Therefore bend should not be defined as deviation inside pre-given geometry. Instead it is the primary deformation burden tracked within that comparison field: how much must be changed, redirected, or reconfigured for one local continuation to become another.

## Explanation (informal)
Bend is the first serious distance-like primitive for the kernel. But it is distance-like only because transformation costs can be compared; it remains grounded in deformation burden, not in a static point-space.

## Derivation (Philosophical)
- From local comparability/cost, some transformations are easier and others harder.
- This burden can be read as bend: the amount of reconfiguration needed to map one continuation into another.
- Because change is non-reversible in general, bend may be directional and need not inherit full metric symmetry.

## Derivation (Formal/Logical/Mathematical)
```text
bend(x→y) := directional deformation burden of transforming continuation x into continuation y within the local comparability field.
```

## Clarifications / Further Context
- This file should be read as a **kernel-resolution primitive handle**, not as one of the earliest ontological distinctions after change.
- Later stabilized regimes may approximate symmetric metric behavior.
- ReID and gauge may use bend, but bend is conceptually prior to those refinements.
- Bend is more primitive than exact identity because it already operates over tolerated deformation.

## Active-chain status
**Status band:** strongly-derived  
**Reason:** once local comparability is admitted, the primitive distinction between lesser and greater deformation burden is unavoidable for a change-first kernel.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ea-haq]]
- [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
- [[01_Statements/Definition/S-DF-elm-ed-gauge-warp]]
- [[01_Statements/Definition/S-DF-haq-core-family]]
- [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]
- [[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]
- [[01_Statements/Definition/S-DF-ops-j4b-counterfactual-bend]]
- [[01_Statements/Definition/S-DF-prm-gauge]]
- [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]
- [[01_Statements/Derivation/S-DR-core-from-immediate-datum]]
- [[01_Statements/Derivation/S-DR-kernel-geometric-primitives-from-localized-comparability]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-trace-invariants]]
- Parents: [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]
- Dependencies: [[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]; [[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold]]
- Successors: [[01_Statements/Definition/S-DF-prm-reid-kernel]]; [[01_Statements/Definition/S-DF-prm-gauge]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

