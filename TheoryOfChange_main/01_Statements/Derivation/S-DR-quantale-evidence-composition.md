---
id: stmt.quantale-evidence-composition
type: DR
aliases: ["LOG_2.0.QuantaleComp"]
title: Evidence composition under quantale logic (min-plus / inf-convolution)
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-quantale-logic]]", "[[01_Statements/Definition/S-DF-evaluation-surface]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]", "[[01_Statements/Corollary/S-CR-proof-as-reachability]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Join_min]]", "[[01_Statements/SYMBOLS/Compose_tensor]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2369
flags: []
tags: [layer/foundations, domain/formal, logic, composition, stable, "type/DR", "concept/math-structures"]
---
# Evidence composition under quantale logic (min-plus / inf-convolution)
## Claim (formal)
Let (L, ≤, ⊕, ⊗) be a quantale with ⊕ = pointwise min (weighted join) and ⊗ = inf‑convolution (path composition). For evidences e₁, e₂: X→ℝ₊ representing costs/negatives of support, the composed evidence satisfies:

(e₁ ⊗ e₂)(z) = inf_{x+y=z} (e₁(x) + e₂(y))

and aggregation across alternatives is e₁ ⊕ e₂ = min(e₁, e₂). Then ⊗ distributes over arbitrary joins (mins), ensuring associative, monotone composition of partial evidences consistent with CO’s path semantics.

## Philosophical Translation (of formal claim)
When multiple partial reasons support a change, we combine their best‑fitting paths (compose) and keep the least costly explanations among options (join). This respects how change accrues along trajectories and how alternatives compete.

## Philosophical Justification
Evidence that accrues along a path should not lose path information; hence composition is path‑wise (inf‑convolution) rather than a blunt sum. Competing explanations should not be averaged if the decision is “take the best available”; this is captured by min‑join. These choices preserve order‑enrichment and match the intuitive semantics of “cheapest sufficient support.”

## Worked micro‑example
- Suppose two independent cues contribute additive effort: e₁ for reaching A, e₂ for reaching B. The cost to reach A then B is the best split of effort along the way: e₁⊗e₂.
- If there are two distinct ways to reach A (e₁, e₁′), their joint support is the better one: e₁⊕e₁′.

## Derivation (Formal/Logical/Mathematical)
- ⊗ defined as inf‑convolution is associative and monotone; ⊕ defined as pointwise min is commutative, associative, and idempotent.
- Distributivity: e ⊗ (⊕ᵢ fᵢ) = ⊕ᵢ (e ⊗ fᵢ) by infimum/inf‑convolution structure.
- Unit: δ₀ (Dirac at zero path) is neutral for ⊗.

## Proofs/Corollaries References
- Corollary: [[S-CR-proof-as-reachability]] (view proofs as minimal‑cost paths).
- Boolean collapse: [[S-DR-quantale-boolean-flattening-proof]] (shows classical limit).

## Clarifications / Further Context
- Assumes evidences are costs/penalties; for supports flip order (use max‑plus).
- Relies on complete lattice structure for arbitrary joins; in finite cases, use finite minima.

## Next Steps in Chain
- suggest: [[S-CR-proof-as-reachability]]
- suggest: [[S-DR-quantale-boolean-flattening-proof]]

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Corollary/S-CR-proof-as-reachability]]
- [[01_Statements/Definition/S-DF-ops-j4b-counterfactual-bend]]
- [[01_Statements/Definition/S-DF-quantale-logic]]
- [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Definition/S-DF-quantale-logic]]; [[01_Statements/Definition/S-DF-evaluation-surface]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]; [[01_Statements/Corollary/S-CR-proof-as-reachability]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

