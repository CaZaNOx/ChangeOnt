---
id: stmt.prm-mdl-compressibility
type: DF
aliases: ["PRM_3.MDL"]
title: Primitive — MDL / compressibility prior
concepts: ["[[02_Concepts/C-math-structures]]", "[[02_Concepts/C-identity-change]]"]
dependencies: []
parents: []
symbols_used: ["[[01_Statements/SYMBOLS/Lambda]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2524
  - path: TheoryOfChange/02_Foundations/DerChain.md:5468
flags: []
tags: [layer/formal, domain/operational, stable, primitive, mdl, information, "type/DF", "concept/math-structures", "concept/identity-change", "symbol/Lambda"]
---
# Primitive — MDL / compressibility prior
## Claim (formal)
Prefer models that compress: MDL gain = error_drop − λ·parameters. Persistence correlates with compressibility under gauge‑consistent invariants.

## Philosophical Translation (of formal claim)
What lasts is what can be said simply, without losing what matters.

## Clarifications / Further Context
- Supports EB (birth), EE (robustness), and selection among motifs.
- λ must be declared; gauge consistency required when comparing across frames.

## Derivation (Formal/Logical/Mathematical)
```text
MDL_gain = error_drop − λ · params_added
Accept change if MDL_gain > 0 under declared gauge/invariants.
```

## Next Steps in Chain
- suggest: [[S-DF-prm-variable-birth]]
- suggest: [[S-DF-elm-ee-compressibility]]
- suggest: [[S-DF-elm-ef-router]]

## Tags
#type/DF #layer/formal #domain/operational #primitive #mdl #information #concept/math-structures #concept/identity-change #symbol/Lambda #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-elm-eb-ghvc]]
- [[01_Statements/Definition/S-DF-elm-ee-compressibility]]
- [[01_Statements/Definition/S-DF-elm-ef-router]]
- [[01_Statements/Definition/S-DF-prm-variable-birth]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]; [[02_Concepts/C-identity-change]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

