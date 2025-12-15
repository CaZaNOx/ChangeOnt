---
id: stmt.prm-temporal-ops
type: DF
aliases: ["PRM_5.TemporalOps"]
title: Primitive — Temporal ops (EMA/lag; depth-aware)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-depth-reach]]"]
parents: ["[[01_Statements/Definition/S-DF-depth-reach]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-ee-compressibility]]", "[[01_Statements/Definition/S-DF-elm-ef-router]]", "[[01_Statements/Definition/S-DF-elm-eg-density-precision]]", "[[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]", "[[01_Statements/Definition/S-DF-ops-j3-attention-warp]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2558
  - path: TheoryOfChange/02_Foundations/DerChain.md:5502
flags: []
tags: [layer/operators, domain/operational, primitive, time, control, "type/DF", "concept/ontology-of-change"]
---
# Primitive — Temporal ops (EMA/lag; depth-aware)
## Claim (formal)
Use exponential moving averages and lag filters parameterized by depth/reach to maintain stable adaptation without erasing critical novelty.

## Philosophical Translation (of formal claim)
Memory should be soft, recent, and respectful of how far things are from now.

## Philosophical Justification
- Depth/reach ([[S-DF-depth-reach]]) tells how “far” an event is; weighting EMA by depth prevents distant events from overwhelming current adaptation.
- Without lag/EMA, signals thrash; too much smoothing erases novelty. Depth-aware smoothing balances stability with responsiveness.

## Clarifications / Further Context
- Feeds attention scheduling, gauge updates, and policy flips.
- Choose decay rates relative to breath cycle and depth; document these when reporting outcomes.

## Derivation (Formal/Operational)
```text
EMA_t(x) = α(depth)·x_t + (1-α(depth))·EMA_{t-1}(x)
Lag filters gate updates if depth exceeds threshold.
```

## Next Steps in Chain
- suggest: [[S-DF-elm-ee-compressibility]]
- suggest: [[S-DF-elm-ef-router]]
- suggest: [[S-DF-elm-eg-density-precision]]
- suggest: [[S-DF-elm-eh-breadth-depth]]
- suggest: [[S-DF-ops-j3-attention-warp]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #time #control #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ea-haq]]
- [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
- [[01_Statements/Definition/S-DF-elm-ef-router]]
- [[01_Statements/Definition/S-DF-elm-eg-density-precision]]
- [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
- [[01_Statements/Definition/S-DF-ops-j3-attention-warp]]
- [[01_Statements/Definition/S-DF-time-kernel]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-depth-reach]]
- Dependencies: [[01_Statements/Definition/S-DF-depth-reach]]
- Successors: [[01_Statements/Definition/S-DF-elm-ee-compressibility]]; [[01_Statements/Definition/S-DF-elm-ef-router]]; [[01_Statements/Definition/S-DF-elm-eg-density-precision]]; [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]; [[01_Statements/Definition/S-DF-ops-j3-attention-warp]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

