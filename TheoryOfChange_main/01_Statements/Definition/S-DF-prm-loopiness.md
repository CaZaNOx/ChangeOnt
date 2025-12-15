---
id: stmt.prm-loopiness
type: DF
aliases: ["PRM_8.Loopiness"]
title: Primitive — Loopiness (short-cycle propensity)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: []
parents: []
successors: ["[[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]", "[[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2598
  - path: TheoryOfChange/02_Foundations/DerChain.md:5542
flags: []
tags: [layer/operators, domain/operational, primitive, topology, recurrence, "type/DF", "concept/ontology-of-change"]
---
# Primitive — Loopiness (short-cycle propensity)
## Claim (formal)
Score short-cycle propensity (e.g., normalized count of short loops) as a control signal for exploration breadth and order penalties.

## Philosophical Translation (of formal claim)
When you keep circling, it’s time to widen the search.

## Philosophical Justification
- Loopiness captures local recurrence; high values indicate risk of stagnation.
- Using it as a control signal lets schedulers pivot to breadth, reducing trap risk without abandoning coherent regions.

## Clarifications / Further Context
- Feeds EH (Breadth/Depth) and EJ (Order Asymmetry).
- Define loop length thresholds relative to breath and task.

## Derivation (Formal/Operational)
```text
loopiness := norm(count_loops(length < L_thresh) / window_size)
```

## Next Steps in Chain
- suggest: [[S-DF-prm-depth-breadth-flip]]
- suggest: [[S-DF-elm-eh-breadth-depth]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #topology #recurrence #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
- [[01_Statements/Definition/S-DF-prm-order-arisal]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Successors: [[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]; [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

