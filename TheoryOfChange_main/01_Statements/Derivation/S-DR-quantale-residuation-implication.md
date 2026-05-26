---
id: stmt.quantale-residuation-implication
type: DR
aliases: []
title: Residuation and implication in quantale-based evidence
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-evaluation-surface]]", "[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]", "[[01_Statements/Definition/S-DF-prm-residuation]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Corollary/S-CR-proof-as-reachability]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Join_min]]", "[[01_Statements/SYMBOLS/Compose_tensor]]", "[[01_Statements/SYMBOLS/Entailment]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:1
  - path: TheoryOfChange_main/03_Derivation/Derivation.md:1
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DR", "concept/math-structures"]
---
# Residuation and implication in quantale-based evidence

## Claim (formal)
In a unital quantale (Q, ≤, ⊗, ⊕), define residual A ⇒ B as the greatest R such that A ⊗ R ≤ B; equivalently A ⊗ X ≤ B ⇔ X ≤ (A ⇒ B). ⇒ distributes over joins in the second argument and is monotone contravariant in A, covariant in B. In min-plus instantiations, ⇒ corresponds to “remaining cost.”

## Philosophical Derivation
Implication reflects how much additional evidence is needed so that composing it with a premise suffices for a conclusion. In graded settings, this is a residual (right adjoint) to composition. It expresses “what remains to be shown” with respect to the evaluation surface rather than binary truth.

## Formal/Operational Derivation
```text
Adjunction: A ⊗ X ≤ B  iff  X ≤ (A ⇒ B)
Monotone: A₁ ≤ A₂ ⇒ (A₂ ⇒ B) ≤ (A₁ ⇒ B); B₁ ≤ B₂ ⇒ (A ⇒ B₁) ≤ (A ⇒ B₂)
Join-distribution: A ⇒ (⊕ᵢ Bᵢ) = ⊕ᵢ (A ⇒ Bᵢ)
Min-plus intuition: (A ⇒ B) ≈ max(0, B − A) when ⊗=+, ⊕=min
```

## Clarifications / Further Context
- Depends on chosen quantale/order; not a single numeric operator.
- Under Boolean flattening (see [[S-DR-quantale-boolean-flattening-proof]]), ⇒ reduces to classical implication.

## Next Steps in Chain
- suggest: [[S-CR-proof-as-reachability]]

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Definition/S-DF-evaluation-surface]]; [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]; [[01_Statements/Definition/S-DF-prm-residuation]]
- Successors: [[01_Statements/Corollary/S-CR-proof-as-reachability]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Corollary/S-CR-proof-as-reachability]]
- [[01_Statements/Definition/S-DF-evaluation-surface]]
- [[01_Statements/Definition/S-DF-prm-residuation]]
- [[01_Statements/Definition/S-DF-quantale-logic]]
<!-- END:AUTOGEN:REFERENCED_BY -->

