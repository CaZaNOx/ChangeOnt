---
id: stmt.quantale-logic
type: DF
aliases: ["LOG_2.0.Quantale"]
title: Quantale logic — weighted joins & composition
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-co-logic-graded-order]]"]
parents: ["[[01_Statements/Definition/S-DF-co-logic-graded-order]]"]
successors: ["[[01_Statements/Derivation/S-DR-quantale-evidence-composition]]", "[[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]", "[[01_Statements/Derivation/S-DR-quantale-residuation-implication]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Join_min]]", "[[01_Statements/SYMBOLS/Compose_tensor]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2421
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DF", "concept/math-structures"]
---
# Quantale logic — weighted joins & composition
## Claim (formal)
Use quantales to capture weighted composition of evidence and validation strength; supports breath aggregation and non‑idempotent joins.

## Philosophical Translation (of formal claim)
We need math that can add up and compose "how true" in structured ways.

## Philosophical Justification
- [[S-DF-co-logic-graded-order]] introduces graded truth; quantales provide the algebra to compose and aggregate those grades.
- Joins/⊕ model competing evidences; tensor/⊗ models sequential composition; residuation captures “effort remaining.”
- Non‑idempotence suits change contexts where repeated evidence accumulates rather than flattens.

## Clarifications / Further Context
- Serves as the base for evidence composition, residuation, and Boolean flattening derivations.
- Choice of quantale (e.g., min-plus) should be declared per application.

## Next Steps in Chain
- suggest: [[S-DR-quantale-evidence-composition]]
- suggest: [[S-DR-quantale-residuation-implication]]
- suggest: [[S-DR-quantale-boolean-flattening-proof]]

## Tags
#type/DF #layer/foundations #domain/formal #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Assumption/S-AS-use-of-preexisting-concepts]]
- [[01_Statements/Corollary/S-CR-boolean-as-collapse]]
- [[01_Statements/Corollary/S-CR-proof-as-reachability]]
- [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- [[01_Statements/Definition/S-DF-elm-ef-router]]
- [[01_Statements/Definition/S-DF-prm-residuation]]
- [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]
- [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]
- [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- Dependencies: [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]; [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]; [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

