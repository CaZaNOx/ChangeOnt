---
id: stmt.metric-space-emergent
type: DF
aliases: ["FND_14.Metric"]
title: Metric space — emergent comparability
concepts: ["[[02_Concepts/C-dimension]]"]
dependencies: ["[[01_Statements/Definition/S-DF-localreach-topology]]", "[[01_Statements/Definition/S-DF-similarity-operator]]"]
parents: ["[[01_Statements/Definition/S-DF-localreach-topology]]"]
successors: ["[[01_Statements/Definition/S-DF-prm-bend-metric]]", "[[01_Statements/Definition/S-DF-dimension-change]]", "[[01_Statements/Definition/S-DF-evaluation-surface]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:1085
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DF", "concept/dimension"]
---
# Metric space — emergent comparability
## Claim (formal)
Metric comparability emerges when LocalReach and Sim provide consistent distance‑like assessments; not a primitive but derived.

## Philosophical Translation (of formal claim)
“Distance” is whatever consistently orders how far eventlets/paths are from each other using the available similarity judgments inside LocalReach.

## Philosophical Justification
- [[S-DF-localreach-topology]] provides neighborhoods; [[S-DF-similarity-operator]] gives graded comparison.
- If Sim satisfies triangle‑like and separation properties on LocalReach, we can induce a pseudometric; with symmetry/identity constraints, a metric.
- This keeps geometry grounded in Δ-structure instead of assuming Euclidean space a priori.

## Explanation (informal)
We treat “how far” as a score derived from how similar reachable points are. When these scores compose reliably, you get an emergent metric structure suitable for talking about curvature, bends, and evaluation surfaces.

## Derivation (Philosophical)
- Define d(x,y) := f(Sim(x,y)) where f is monotone.
- Require: d(x,x)=0; d(x,y)=d(y,x) if Sim symmetric; d(x,z) ≤ d(x,y)+d(y,z) if Sim respects composition along Reach.

## Derivation (Formal/Logical/Mathematical)
```text
Given Sim: LocalReach×LocalReach→[0,1],
let d(x,y) := g(1 - Sim(x,y)), with g monotone.
If ∀x,y,z: Sim(x,z) ≥ h(Sim(x,y), Sim(y,z)) then d satisfies triangle-like inequality.
```

## Proofs/Corollaries References
- corollary: enables [[S-DF-prm-bend-metric]] (curvature cost) and [[S-DF-evaluation-surface]] construction.

## Clarifications / Further Context
- Metric validity is local and resolution-dependent; tightening ε can refine d.
- Where Sim is asymmetric, treat d as quasi-metric until symmetry is earned.

## Next Steps in Chain
- suggest: [[S-DF-prm-bend-metric]]
- suggest: [[S-DF-dimension-change]]
- suggest: [[S-DF-evaluation-surface]]

## Tags
#type/DF #layer/foundations #domain/formal #concept/dimension #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-localreach-topology]]
- [[01_Statements/Definition/S-DF-math-structures]]
- [[01_Statements/Definition/S-DF-prm-bend-metric]]
- [[01_Statements/Definition/S-DF-prm-gauge]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-dimension]]
- Parents: [[01_Statements/Definition/S-DF-localreach-topology]]
- Dependencies: [[01_Statements/Definition/S-DF-localreach-topology]]; [[01_Statements/Definition/S-DF-similarity-operator]]
- Successors: [[01_Statements/Definition/S-DF-prm-bend-metric]]; [[01_Statements/Definition/S-DF-dimension-change]]; [[01_Statements/Definition/S-DF-evaluation-surface]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

