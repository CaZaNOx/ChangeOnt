---
id: stmt.dimension-variation
type: DR
aliases: ["FND_7.DimVar"]
title: Dimension variation under Tx
concepts: ["[[02_Concepts/C-dimension]]", "[[02_Concepts/C-frame-operators]]"]
dependencies: ["[[01_Statements/Definition/S-DF-dimension-change]]", "[[01_Statements/Definition/S-DF-tx-operator]]", "[[01_Statements/Definition/S-DF-tx-algebra]]"]
parents: ["[[01_Statements/Definition/S-DF-dimension-change]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_7_Dimension.md:1
  - path: TheoryOfChange/02_Foundations/FND_6_TransformationOperator_Tx.md:1
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DR", "concept/dimension", "concept/frame-operators"]
---
# Dimension variation under Tx
## Claim (formal)
For Tx: (S,F)→(S',F'), effective dimension dim(LocalReach') may differ from dim(LocalReach) due to admissible transformation changes.

## Philosophical Translation (of formal claim)
Changing the frame can change how many directions of change are even possible.

## Clarifications / Further Context
- Tx algebra determines which frame transitions are allowed; dimension is evaluated on the resulting LocalReach.
- Important for auditing when models assume fixed dimension but Tx alters reach.

## Tags
#type/DR #layer/foundations #domain/formal #concept/dimension #concept/frame-operators #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-dimension-change]]
- [[01_Statements/Definition/S-DF-tx-algebra]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-dimension]]; [[02_Concepts/C-frame-operators]]
- Parents: [[01_Statements/Definition/S-DF-dimension-change]]
- Dependencies: [[01_Statements/Definition/S-DF-dimension-change]]; [[01_Statements/Definition/S-DF-tx-operator]]; [[01_Statements/Definition/S-DF-tx-algebra]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

