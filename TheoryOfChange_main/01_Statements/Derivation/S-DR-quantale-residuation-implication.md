---
id: stmt.quantale-residuation-implication
type: DR
title: Residuation and implication in quantale-based evidence
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-evaluation-surface]]", "[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Corollary/S-CR-proof-as-reachability]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Join_min]]", "[[01_Statements/SYMBOLS/Compose_tensor]]", "[[01_Statements/SYMBOLS/Entailment]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:1
  - path: TheoryOfChange_main/03_Derivation/Derivation.md:1
flags: []
status: stable
tags: [logic/quantale, residuation, formal, "type/DR", "concept/math-structures", "#logic", "#math", "#type/DR", "#layer/foundations", "#domain/formal", "#concept/math-structures"]
---

# Residuation and implication in quantale-based evidence

Philosophical Derivation

Implication reflects how much additional evidence is needed so that composing it with a premise suffices for a conclusion. In graded settings, this is a residual (right adjoint) to composition. It expresses “what remains to be shown” with respect to the evaluation surface rather than binary truth.

Formal/Operational Derivation

Let (Q, ≤, ⊗, ⊕) be a unital quantale. Define A ⇒ B as the greatest R such that A ⊗ R ≤ B (residuation). Then for all X:

- A ⊗ X ≤ B  iff  X ≤ (A ⇒ B)  (adjunction)
- Monotone: if A₁ ≤ A₂ then (A₂ ⇒ B) ≤ (A₁ ⇒ B); if B₁ ≤ B₂ then (A ⇒ B₁) ≤ (A ⇒ B₂)
- Distributes over joins in the second argument: A ⇒ (⊕ᵢ Bᵢ) = ⊕ᵢ (A ⇒ Bᵢ)

In min-plus instantiations (cost domain), using additive composition and infimum as join, implication corresponds to a (truncated) difference: (A ⇒ B) ≈ max(0, B − A) in a simplified scalar regime. Operationally, “remaining cost” to meet B given A.

Clarifications

- The residual depends on the chosen algebra and order; it is not a unique numeric operator across domains.
- Under Boolean flattening (see [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]), ⇒ reduces to classical material implication.

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures

































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Definition/S-DF-evaluation-surface]]; [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]
- Successors: [[01_Statements/Corollary/S-CR-proof-as-reachability]]
<!-- END:AUTOGEN:RELATIONSHIPS -->
































































<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->






























