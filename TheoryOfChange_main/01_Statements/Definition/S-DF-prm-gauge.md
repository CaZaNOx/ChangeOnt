---
id: stmt.prm-gauge
type: DF
aliases: ["PRM_2.Gauge"]
title: Primitive — Gauge (history-adaptive alignment transport)
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-gauge-alignment-field]]", "[[01_Statements/Definition/S-DF-metric-space-emergent]]", "[[01_Statements/Definition/S-DF-prm-bend-metric]]"]
parents: ["[[01_Statements/Definition/S-DF-gauge-alignment-field]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-ed-gauge-warp]]", "[[01_Statements/Definition/S-DF-elm-ea-haq]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Gamma]]", "[[01_Statements/SYMBOLS/Curvature_K]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2498
  - path: TheoryOfChange/02_Foundations/DerChain.md:5442
flags: []
tags: [layer/formal, domain/operational, stable, primitive, alignment, field, "type/DF", "concept/math-structures", "symbol/Gamma", "symbol/Curvature_K"]
---
# Primitive — Gauge (history-adaptive alignment transport)
## Claim (formal)
Choose a connection Γ minimizing local tension mismatch Δτ across neighbors, yielding transport that preserves learned coherence and induces an emergent metric; track curvature K as coherence signal.

## Philosophical Translation (of formal claim)
Coherence comes from learning how to carry comparisons from place to place without tearing the pattern.

## Philosophical Justification
- [[S-DF-gauge-alignment-field]] defines alignment needs; [[S-DF-metric-space-emergent]] supplies distance; [[S-DF-prm-bend-metric]] gives cost of deviation.
- Selecting Γ to minimize bend mismatch aligns transports with lived coherence, reducing SE expenditure and stabilizing identity under change.
- Curvature K flags where transports disagree, guiding updates and HAQ warp.

## Explanation (informal)
Gauge is the rule for moving references around without them drifting apart. By adapting Γ from observed bends, we keep our comparisons meaningful even as frames shift.

## Derivation (Philosophical)
- Define Δτ across adjacent transports; choose Γ* = argmin Δτ subject to LocalReach constraints.
- Update Γ over breath windows using curvature feedback to avoid thrash.

## Derivation (Formal/Logical/Mathematical)
```text
Γ* := argmin_Γ ∑_{(i,j)∈LocalReach} ||τ_Γ(i→j) - τ_target||^2
K := dΓ + Γ∧Γ   // curvature as coherence diagnostic
```

## Proofs/Corollaries References
- corollary: supports [[S-DF-elm-ed-gauge-warp]], [[S-DF-elm-ea-haq]].

## Clarifications / Further Context
- History-adaptive: update Γ with EMA/leak to balance stability vs responsiveness.
- Gauge choice must remain compatible with declared invariants/Sim.

## Next Steps in Chain
- suggest: [[S-DF-elm-ed-gauge-warp]]
- suggest: [[S-DF-elm-ea-haq]]

## Tags
#type/DF #layer/formal #domain/operational #primitive #alignment #field #concept/math-structures #symbol/Gamma #symbol/Curvature_K #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-classical-limit-falsifier]]
- [[01_Statements/Clarification/S-CL-letter-regime-policy]]
- [[01_Statements/Definition/S-DF-elm-ea-haq]]
- [[01_Statements/Definition/S-DF-elm-ed-gauge-warp]]
- [[01_Statements/Derivation/S-DR-core-from-immediate-datum]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- Dependencies: [[01_Statements/Definition/S-DF-gauge-alignment-field]]; [[01_Statements/Definition/S-DF-metric-space-emergent]]; [[01_Statements/Definition/S-DF-prm-bend-metric]]
- Successors: [[01_Statements/Definition/S-DF-elm-ed-gauge-warp]]; [[01_Statements/Definition/S-DF-elm-ea-haq]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

