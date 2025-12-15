---
id: stmt.prm-order-arisal
type: DF
aliases: ["PRM_15.OrderArisal"]
title: Primitive — Order/Arisal (AB≠BA; order-sensitive penalties)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-loopiness]]", "[[01_Statements/Definition/S-DF-co-logic-graded-order]]"]
parents: ["[[01_Statements/Definition/S-DF-co-logic-graded-order]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-ej-order-asymmetry]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2684
  - path: TheoryOfChange/02_Foundations/DerChain.md:5628
flags: []
tags: [layer/operators, domain/operational, primitive, order, control, "type/DF", "concept/ontology-of-change"]
---
# Primitive — Order/Arisal (AB≠BA; order-sensitive penalties)
## Claim (formal)
Penalize backtracks and order‑sensitive harm: doing A then B differs from B then A; integrate penalties into graded co‑logic for action selection.

## Philosophical Translation (of formal claim)
The same steps in a different order can help or hurt — we must care about sequence, not just totals.

## Philosophical Justification
- [[S-DF-prm-loopiness]] flags short cycles; order penalties discourage unproductive 2-cycles.
- [[S-DF-co-logic-graded-order]] provides graded truth/validation; embedding order penalties there makes sequencing effects explicit and composable.

## Clarifications / Further Context
- Feeds EJ (Order Asymmetry) and counters pathological backtracks.
- Declare which actions are order-sensitive and the window over which penalties apply.

## Derivation (Formal/Operational)
```text
penalty(A,B) applied if sequence deviates (e.g., BA after AB) or loops with no gain;
aggregate into co-logic score for action selection.
```

## Next Steps in Chain
- suggest: [[S-DF-elm-ej-order-asymmetry]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #order #control #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ej-order-asymmetry]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-loopiness]]; [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- Successors: [[01_Statements/Definition/S-DF-elm-ej-order-asymmetry]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

