---
id: stmt.prm-bend-metric
type: DF
aliases: ["PRM_1.Bend"]
title: Primitive — Bend metric (local deviation from self-continuation)
concepts: ["[[02_Concepts/C-ontology-of-change]]", "[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-localreach-topology]]", "[[01_Statements/Definition/S-DF-metric-space-emergent]]", "[[01_Statements/Definition/S-DF-gauge-alignment-field]]"]
parents: ["[[01_Statements/Definition/S-DF-gauge-alignment-field]]"]
successors: ["[[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]", "[[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Tau]]", "[[01_Statements/SYMBOLS/Gamma]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5416
flags: []
tags: [layer/formal, domain/operational, stable, primitive, metric, energy, "type/DF", "concept/ontology-of-change", "concept/math-structures", "symbol/Tau", "symbol/Gamma"]
---
# Primitive — Bend metric (local deviation from self-continuation)
## Claim (formal)
The bend τ of a segment quantifies deviation from its gauge‑aligned continuation. Given predicted continuation p(x) and realized y, τ := ‖y − p(x)‖_Γ. Lower τ indicates coherent self‑continuation; higher τ indicates effort/curvature.

## Philosophical Translation (of formal claim)
“Effort” is how much a trajectory must bend away from what it would have done to remain itself.

## Philosophical Justification
- [[S-DF-gauge-alignment-field]] defines the “straight ahead” direction in the present gauge frame.
- [[S-DF-localreach-topology]] and [[S-DF-metric-space-emergent]] provide a distance notion; applying it to predicted vs. realized motion yields τ.
- Quantifying bend supplies a cost term for stabilization and routing; without it, effort/curvature is only qualitative.

## Explanation (informal)
Imagine where the pattern would go if it stayed aligned with its internal gauge. Measure how far the actual step diverges. That number is the bend — a proxy for how much SE is spent steering or being perturbed.

## Derivation (Philosophical)
- Define predicted continuation p(x) via gauge flow.
- Use emergent metric ‖·‖_Γ to compare p(x) to y.
- Path bend is the monoidal sum of segment bends, giving cumulative deviation cost.

## Derivation (Formal/Logical/Mathematical)
```text
τ(x→y) := || y - p(x) ||_Γ
τ_path := ⊕_i τ(e_i→e_{i+1})
```

## Proofs/Corollaries References
- corollary: used in [[S-DR-bend-metric-lawvere-attractors]] and [[S-DF-ops-j1-bend-substitution]].

## Clarifications / Further Context
- Γ encodes gauge warp; choose a norm consistent with [[S-DF-metric-space-emergent]].
- High τ signals identity strain; may trigger gauge updates or SE accounting.

## Next Steps in Chain
- suggest: [[S-DR-bend-metric-lawvere-attractors]]
- suggest: [[S-DF-ops-j1-bend-substitution]]

## Tags
#type/DF #layer/formal #domain/operational #concept/ontology-of-change #concept/math-structures #symbol/Tau #symbol/Gamma #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-ea-haq]]
- [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
- [[01_Statements/Definition/S-DF-elm-ed-gauge-warp]]
- [[01_Statements/Definition/S-DF-elm-ef-router]]
- [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- [[01_Statements/Definition/S-DF-haq-core-family]]
- [[01_Statements/Definition/S-DF-metric-space-emergent]]
- [[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]
- [[01_Statements/Definition/S-DF-ops-j4b-counterfactual-bend]]
- [[01_Statements/Definition/S-DF-prm-gauge]]
- [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]
- [[01_Statements/Derivation/S-DR-core-from-immediate-datum]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- Dependencies: [[01_Statements/Definition/S-DF-localreach-topology]]; [[01_Statements/Definition/S-DF-metric-space-emergent]]; [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- Successors: [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]; [[01_Statements/Definition/S-DF-ops-j1-bend-substitution]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

