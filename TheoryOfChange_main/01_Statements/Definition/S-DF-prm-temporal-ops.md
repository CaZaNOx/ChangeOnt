---
id: stmt.prm-temporal-ops
type: DF
aliases: ["PRM_5.TemporalOps"]
title: Primitive — Temporal ops (EMA/lag; depth-aware)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]", "[[01_Statements/Definition/S-DF-depth-reach]]", "[[01_Statements/02_Outer_Formation/003_S-DF-trace-retention]]", "[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence]]"]
parents: ["[[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-ee-compressibility]]", "[[01_Statements/Definition/S-DF-elm-ef-router]]", "[[01_Statements/Definition/S-DF-elm-eg-density-precision]]", "[[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]", "[[01_Statements/Definition/S-DF-ops-j3-attention-warp]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2558
  - path: TheoryOfChange/02_Foundations/DerChain.md:5502
flags: []
tags: [layer/operators, domain/operational, primitive, time, control, "type/DF", "concept/ontology-of-change"]
status: stable
---
# Primitive — Temporal ops (EMA/lag; depth-aware)
## Claim (formal)
Use exponential moving averages and lag filters parameterized by depth/reach to maintain stable adaptation without erasing critical novelty.

## Philosophical Translation (of formal claim)
A change-first kernel needs memory that is neither frozen storage nor total forgetfulness. Temporal ops are the disciplined way to let recent structured change matter more than distant or noisy carry-over.

## Philosophical Justification
[[S-DR-kernel-primitives-from-invariant-regimes]] shows that selective recurrence forces a temporal summarization primitive. [[S-DF-trace-retention]] supplies carry-forward; [[S-DF-selective-recurrence]] supplies repeatability; [[S-DF-depth-reach]] supplies graded distance from now. Temporal ops are the compact operator family that turns those ideas into runtime weighting rather than all-or-nothing storage.

## Explanation (informal)
Temporal ops are the kernel’s soft memory discipline. They control how much of the recent past should still count, how quickly regimes can cool down, and how far-away evidence should fade.

## Derivation (Philosophical)
- Traces carry forward prior difference.
- Selective recurrence makes some of those traces more worth preserving than others.
- Depth/reach grades how far from the current locus a signal stands.
- Therefore a depth-aware smoothing and lag primitive becomes necessary.

## Derivation (Formal/Logical/Mathematical)
```text
EMA_t(x) = α(depth)·x_t + (1-α(depth))·EMA_{t-1}(x)
Lag filters gate updates if depth exceeds threshold.
```

## Clarifications / Further Context
- Feeds attention scheduling, gauge updates, and policy flips.
- Choose decay rates relative to breath cycle and depth; document these when reporting outcomes.
- This primitive summarizes time; it does not itself decide the regime.

## Next Steps in Chain
- suggest: [[S-DF-elm-ee-compressibility]]
- suggest: [[S-DF-elm-ef-router]]
- suggest: [[S-DF-elm-eg-density-precision]]
- suggest: [[S-DF-elm-eh-breadth-depth]]
- suggest: [[S-DF-ops-j3-attention-warp]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #time #control #concept/ontology-of-change #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ea-haq]]
- [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
- [[01_Statements/Definition/S-DF-elm-eg-density-precision]]
- [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
- [[01_Statements/Definition/S-DF-ops-j3-attention-warp]]
- [[01_Statements/Definition/S-DF-time-kernel]]
- [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]
- Dependencies: [[01_Statements/Derivation/S-DR-kernel-primitives-from-invariant-regimes]]; [[01_Statements/Definition/S-DF-depth-reach]]; [[01_Statements/02_Outer_Formation/003_S-DF-trace-retention]]; [[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence]]
- Successors: [[01_Statements/Definition/S-DF-elm-ee-compressibility]]; [[01_Statements/Definition/S-DF-elm-ef-router]]; [[01_Statements/Definition/S-DF-elm-eg-density-precision]]; [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]; [[01_Statements/Definition/S-DF-ops-j3-attention-warp]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

