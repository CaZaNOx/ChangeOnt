---
id: stmt.dr-quotient-chain-lln
type: DR
title: Law of large numbers on quotient chains
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]", "[[01_Statements/Clarification/S-CL-drift-guarded-lln]]", "[[01_Statements/Definition/S-DF-prm-closure-quotient]]"]
parents: []
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:100
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:111
flags: []
tags: [statistics, formal, "type/DR", "concept/math-structures"]
status: draft
---

# Law of large numbers on quotient chains

## Claim (formal)
If the ε-quotient Markov chain induced by bend-based equivalence is ergodic and mixing, then for any bounded observable on equivalence classes, time averages converge almost surely to expectations under the unique stationary distribution of the quotient. Validity requires declared drift guards and sample floors.

## Philosophical Translation (of formal claim)
After we merge near-identical paths, repeated visits to each merged class stabilize their statistics—provided drift is bounded and we sample enough—so frequencies on the coarse classes become reliable.

## Derivation (sketch)
- Assume ergodicity/mixing on the quotient chain; then Birkhoff/LLN applies to bounded observables.
- The convergence is well-defined because the underlying topology is supplied by the bend metric (see [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]) and equivalence classes are measurable.
- Drift guards and minimum visit counts (see [[01_Statements/Clarification/S-CL-drift-guarded-lln]]) are required to keep the quotient stable during sampling.

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Dependencies: [[01_Statements/Derivation/S-DR-bend-metric-lawvere-attractors]]; [[01_Statements/Clarification/S-CL-drift-guarded-lln]]; [[01_Statements/Definition/S-DF-prm-closure-quotient]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

