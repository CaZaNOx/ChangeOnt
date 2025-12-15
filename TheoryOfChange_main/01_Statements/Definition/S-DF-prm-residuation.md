---
id: stmt.prm-residuation
type: DF
aliases: ["PRM_11.Residuation"]
title: Primitive — Residuation (implication-as-effort) in a residuated quantale
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Derivation/S-DR-quantale-residuation-implication]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5580
flags: []
tags: [layer/foundations, domain/formal, stable, primitive, logic, implication, "type/DF", "concept/math-structures"]
---
# Primitive — Residuation (implication-as-effort) in a residuated quantale
## Claim (formal)
In a (residuated) quantale (L, ≤, ⊕, ⊗) with min‑join ⊕ and composition ⊗, define residual a ⇒ b as the greatest x with a ⊗ x ≤ b. Equivalently: a ⊗ x ≤ b ⇔ x ≤ a ⇒ b. This interprets “how much more effort is needed” to reach b after a.

## Philosophical Translation (of formal claim)
Implication is “what remains to be done.” If a gets you partway, residuation measures the extra lift to achieve b.

## Clarifications / Further Context
- Supports policy heads (cost gaps), routing proofs, and J‑operators with guarantees.
- Links directly to [[S-DR-quantale-residuation-implication]] for formal properties.

## Tags
#type/DF #layer/foundations #domain/formal #primitive #logic #implication #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Definition/S-DF-quantale-logic]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

