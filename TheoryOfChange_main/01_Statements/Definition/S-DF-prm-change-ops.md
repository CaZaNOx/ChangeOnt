---
id: stmt.prm-change-ops
type: DF
aliases: ["PRM_6.ChangeOps"]
title: Primitive — Change ops (motif calculus)
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-eventlet]]", "[[01_Statements/Definition/S-DF-path-eventlet-chain]]", "[[01_Statements/Definition/S-DF-prm-closure-quotient]]"]
parents: ["[[01_Statements/Definition/S-DF-eventlet]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-ei-change-operators]]", "[[01_Statements/Definition/S-DF-prm-changeops-core]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:2572
  - path: TheoryOfChange/02_Foundations/DerChain.md:5516
flags: []
tags: [layer/operators, domain/operational, primitive, motifs, algebra, "type/DF", "concept/ontology-of-change"]
---
# Primitive — Change ops (motif calculus)
## Claim (formal)
Detect and compose k‑gram change atoms into higher motifs; enable split/compose/quotient operations consistent with similarity/closure.

## Philosophical Translation (of formal claim)
Small moves make bigger moves; we need the algebra that builds with them.

## Philosophical Justification
- [[S-DF-eventlet]] and [[S-DF-path-eventlet-chain]] provide the atomic steps and paths.
- [[S-DF-prm-closure-quotient]] ensures motifs respect identity tolerances (≈_ε).
- A calculus over these atoms allows systematic construction and manipulation of change structures instead of ad-hoc heuristics.

## Clarifications / Further Context
- Basis for EI (Change Operators) and OPS/J2 (quotients).
- k and closure tolerances must be declared per domain.

## Derivation (Formal/Operational)
```text
atoms := detect_eventlets(path)
motifs := kgram(atoms, k)
compose/quotient motifs under ≈_ε
```

## Next Steps in Chain
- suggest: [[S-DF-elm-ei-change-operators]]
- suggest: [[S-DF-prm-changeops-core]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #motifs #algebra #concept/ontology-of-change

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-hindsight-canonicalization]]
- [[01_Statements/Definition/S-DF-elm-ei-change-operators]]
- [[01_Statements/Definition/S-DF-prm-changeops-core]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-eventlet]]
- Dependencies: [[01_Statements/Definition/S-DF-eventlet]]; [[01_Statements/Definition/S-DF-path-eventlet-chain]]; [[01_Statements/Definition/S-DF-prm-closure-quotient]]
- Successors: [[01_Statements/Definition/S-DF-elm-ei-change-operators]]; [[01_Statements/Definition/S-DF-prm-changeops-core]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

