---
id: stmt.elm-ej-order-asymmetry
type: DF
aliases: ["ELM.EJ.OrderAsymmetry"]
title: Element — EJ — Order Asymmetry
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-prm-order-arisal]]", "[[01_Statements/Definition/S-DF-co-logic-graded-order]]"]
parents: ["[[01_Statements/Definition/S-DF-prm-order-arisal]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5628
flags: []
tags: [element, order, penalties, "type/DF"]
---
# Element — EJ — Order Asymmetry
## Claim (formal)
Emit per‑action order‑sensitive penalties and votes using graded co‑logic, along with loopiness/arisal indicators.

## Philosophical Translation (of formal claim)
Do the right things in the right order; doing them backward can undo what you gained.

## Philosophical Justification
Change is path‑dependent: AB may open opportunities that BA closes. Penalizing 2‑cycles/backtracks formalizes this intuition and reduces oscillations that waste effort or erase gains. Casting penalties as graded votes (co‑logic) integrates order awareness into decision aggregation.

## Derivation (Philosophical)
- Change is path-sensitive, not merely state-sensitive.
- Loopiness and graded order logic show that sequence can alter viability.
- EJ is the element that makes those order effects actionable.

## Derivation (Formal/Logical/Mathematical)
```text
penalty_map[a] := risk(returns_to_prev) + risk(undoes_gain)
vote_map := grade_to_votes(penalty_map)
```

## Explanation (informal)
EJ is where sequence really matters. It exposes that A then B may be harmless while B then A may be destructive, trapped, or wasteful.

## Clarifications / Further Context
- Calibrate penalties to avoid over‑discouraging necessary reversals (repair steps).

## Next Steps in Chain
- Evaluate arisal signals and loopiness trends under EJ to verify harm reduction.

## Tags
#type/DF #element #order #penalties #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-candidate-surface]]
- [[01_Statements/Definition/S-DF-prm-order-arisal]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-prm-order-arisal]]
- Dependencies: [[01_Statements/Definition/S-DF-prm-order-arisal]]; [[01_Statements/Definition/S-DF-co-logic-graded-order]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

