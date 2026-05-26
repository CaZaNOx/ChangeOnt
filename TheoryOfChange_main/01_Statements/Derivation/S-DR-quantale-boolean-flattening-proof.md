---
id: stmt.quantale-boolean-flattening-proof
type: DR
title: Quantale → Boolean flattening — proof sketch via idempotent collapse
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Corollary/S-CR-boolean-as-collapse]]", "[[01_Statements/Definition/S-DF-evaluation-surface]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Derivation/S-DR-quantale-evidence-composition]]", "[[01_Statements/Corollary/S-CR-proof-as-reachability]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Join_min]]", "[[01_Statements/SYMBOLS/Compose_tensor]]"]
sources:
  - path: TheoryOfChange_main/03_Derivation/Derivation.md:1
  - path: TheoryOfChange/02_Foundations/DerChain.md:1
flags: []
tags: [logic/quantale, logic/boolean, formal, stable, "type/DR", "concept/math-structures"]
---
# Quantale → Boolean flattening — proof sketch via idempotent collapse
## Claim (formal)
Given a unital quantale (Q, ≤, ⊗, ⊕), define a projection π_θ: Q → Bool by π_θ(x)=1 iff x ≥ θ (0<θ≤⊤) and π_θ(x)=0 otherwise. If θ is upward closed and stable under ⊗ (x≥θ, y≥θ ⇒ x⊗y≥θ), then π_θ is a quantale homomorphism: π_θ(⊕ᵢ xᵢ)=∨ᵢ π_θ(xᵢ) and π_θ(x⊗y)=π_θ(x)∧π_θ(y). Boolean logic is therefore the idempotent collapse of graded evidence under admissible thresholds.

## Philosophical Translation (of formal claim)
Classical true/false reasoning is what you get when you choose to ignore all but “good enough” evidence. A thresholded projection of graded support yields Boolean connectives; nothing metaphysically special happens—precision is deliberately discarded.

## Philosophical Justification
We often act once evidence crosses a sufficiency line; finer gradations become irrelevant. Modeling this as a quotient makes the loss explicit and keeps the graded calculus available when needed. This avoids pretending Boolean logic is fundamental while explaining its practical use.

## Derivation (Formal/Logical/Mathematical)
- Let θ satisfy upward closure and ⊗‑closure. Define π_θ as above.
- For any family {xᵢ}, xᵢ≥θ for some i iff ⊕ᵢ xᵢ ≥ θ ⇒ π_θ(⊕ᵢ xᵢ)=∨ᵢ π_θ(xᵢ).
- Monotonicity of ⊗ gives x⊗y≥θ iff x≥θ and y≥θ, hence π_θ(x⊗y)=π_θ(x)∧π_θ(y).
- Idempotent collapse: identify all elements ≥θ with 1, all <θ with 0.

## Proofs/Corollaries References
- Boolean collapse principle: [[S-CR-boolean-as-collapse]].
- Composition and path semantics: [[S-DR-quantale-evidence-composition]], [[S-CR-proof-as-reachability]].

## Clarifications / Further Context
- θ is application‑dependent; different θ produce different coarse logics.
- If ⊗ is not strictly closed over θ, use conservative θ′ ≤ θ that is closed, or drop to a three‑valued regime instead of forcing Boolean.

## Next Steps in Chain
- suggest: [[S-DR-quantale-evidence-composition]]
- suggest: [[S-CR-proof-as-reachability]]

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Corollary/S-CR-boolean-as-collapse]]; [[01_Statements/Definition/S-DF-evaluation-surface]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]; [[01_Statements/Corollary/S-CR-proof-as-reachability]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-classical-limit-falsifier]]
- [[01_Statements/Corollary/S-CR-proof-as-reachability]]
- [[01_Statements/Definition/S-DF-quantale-logic]]
- [[01_Statements/Derivation/S-DR-core-from-immediate-datum]]
- [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]
<!-- END:AUTOGEN:REFERENCED_BY -->

