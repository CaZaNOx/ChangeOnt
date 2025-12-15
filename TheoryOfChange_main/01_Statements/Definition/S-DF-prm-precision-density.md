---
id: stmt.prm-precision-density
type: DF
aliases: ["PRM_7.PrecisionDensity"]
title: Primitive — Precision/Density scheduling
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-attention-focus]]", "[[01_Statements/Definition/S-DF-breath-field-global-integrator]]"]
parents: ["[[01_Statements/Definition/S-DF-attention-focus]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-eg-density-precision]]", "[[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2584
  - path: TheoryOfChange/02_Foundations/DerChain.md:5528
flags: []
tags: [layer/operators, domain/operational, stable, primitive, control, scheduling, "type/DF", "concept/ontology-of-change"]
---
# Primitive — Precision/Density scheduling
## Claim (formal)
Schedule effective precision r′ from surprise/phase indicators to trade density vs. robustness; couple to breath phase for stability.

## Philosophical Translation (of formal claim)
Focus tightens or loosens with how surprising things are and where we are in the global rhythm.

## Philosophical Justification
- [[S-DF-attention-focus]] controls ε allocation; precision/density is its operational tuning knob.
- [[S-DF-breath-field-global-integrator]] provides phase and global context; aligning precision changes to breath avoids thrash.
- Adjusting precision based on surprise prevents overfitting noise (too tight) or missing signal (too loose).

## Explanation (informal)
When the system hits surprises, widen density (loosen precision) to gather more context; when things are stable, tighten to refine. Do this in sync with breath to keep SE balanced.

## Derivation (Formal/Logical/Mathematical)
```text
r' := f(surprise, phase)
if surprise high or phase=open: increase density (loosen precision)
else: increase precision (tighten density)
```

## Proofs/Corollaries References
- feeds [[S-DF-elm-eg-density-precision]] and curvature-aware schedulers ([[S-DR-bend-metric-lawvere-attractors]]).

## Next Steps in Chain
- suggest: [[S-DF-elm-eg-density-precision]]
- suggest: [[S-DR-bend-metric-lawvere-attractors]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #control #scheduling #concept/ontology-of-change #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
- [[01_Statements/Definition/S-DF-elm-eg-density-precision]]
- [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-attention-focus]]
- Dependencies: [[01_Statements/Definition/S-DF-attention-focus]]; [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
- Successors: [[01_Statements/Definition/S-DF-elm-eg-density-precision]]; [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

