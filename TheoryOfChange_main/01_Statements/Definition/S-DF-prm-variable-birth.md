---
id: stmt.prm-variable-birth
type: DF
aliases: ["PRM_9.VariableBirth"]
title: Primitive — Variable birth (latent dimension addition under pressure + MDL gain)
concepts: ["[[02_Concepts/C-identity-change]]", "[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-stabilization-energy]]", "[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]", "[[01_Statements/Definition/S-DF-prm-mdl-compressibility]]"]
parents: ["[[01_Statements/Definition/S-DF-stabilization-energy]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-eb-ghvc]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Lambda]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5518
flags: []
tags: [layer/operators, domain/operational, stable, primitive, structure-growth, mdl, "type/DF", "concept/identity-change", "concept/math-structures", "symbol/Lambda"]
---
# Primitive — Variable birth (latent dimension addition under pressure + MDL gain)
## Claim (formal)
Introduce a new latent variable when structural pressure is high and the MDL (compression) gain is positive. Birth criteria jointly consider stabilization energy, recurrence structure, and description-length improvement.

## Philosophical Translation (of formal claim)
New degrees of freedom emerge when the system can explain more with less by adding them — growth when the pattern demands a larger room.

## Philosophical Justification
- [[S-DF-stabilization-energy]]: sustained pressure signals current representation is insufficient.
- [[S-DF-structural-recurrence-likelihood]]: recurrence structure shows whether pattern is coherent enough to justify extending it.
- [[S-DF-prm-mdl-compressibility]]: birth only when compression improves (error_drop − λ·params > 0) to avoid gratuitous complexity.

## Clarifications / Further Context
- Couples novelty pressure with conservative model selection (avoid overfitting; reward compressibility).
- Downstream: identity maintenance under new coordinates (quotients/closure).
- Use hysteresis on pressure/MDL thresholds to prevent birth thrash.

## Derivation (Formal/Operational)
```text
trigger = (pressure > τ_p) ∧ (MDL_gain = error_drop − λ·params > 0) ∧ SRL coherence
born_variable := trigger ? 1 : 0
```

## Proofs/Corollaries References
- element implementation: [[S-DF-elm-eb-ghvc]]

## Next Steps in Chain
- suggest: [[S-DF-elm-eb-ghvc]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #structure-growth #mdl #concept/identity-change #concept/math-structures #symbol/Lambda #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-feature-gating]]
- [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]; [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-stabilization-energy]]
- Dependencies: [[01_Statements/Definition/S-DF-stabilization-energy]]; [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]; [[01_Statements/Definition/S-DF-prm-mdl-compressibility]]
- Successors: [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

