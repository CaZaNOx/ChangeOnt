---
id: stmt.change-fitness
type: DF
aliases: ["AI13.Fitness"]
title: Change-based fitness (CBF)
concepts: ["[[02_Concepts/C-recursive-truth]]", "[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]", "[[01_Statements/Definition/S-DF-stabilization-energy]]", "[[01_Statements/Definition/S-DF-self-similarity-threshold]]"]
parents: ["[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]"]
successors: ["[[01_Statements/Derivation/S-DR-fitness-vs-srl-se]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Approx]]"]
sources:
  - path: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md:17
flags: []
tags: [layer/validation, domain/operational, stable, "type/DF", "concept/recursive-truth", "concept/identity", "symbol/Approx"]
---
# Change-based fitness (CBF)
## Claim (formal)
CBF(P) := weighted aggregation of SRL(P), identity persistence (SE, θ), and successful Tx usage with minimal GH backlog.

## Philosophical Translation (of formal claim)
Fitness measures how well a pattern keeps recurring and holding together while adapting frames honestly.

## Philosophical Justification
- [[S-DF-structural-recurrence-likelihood]]: recurrence under breath is a base fitness signal.
- [[S-DF-stabilization-energy]] and [[S-DF-self-similarity-threshold]]: identity persistence requires sufficient SE and similarity thresholds.
- Honest frame adaptation (Tx) without unresolved GH backlog reflects integrity in change.

## Clarifications / Further Context
- CBF is domain‑specific via weights; it is not a classical probability but a structural viability score.
- GH backlog is penalized to encourage explicit resolution of closure failures.

## Derivation (Formal)
```text
CBF(P) := w1*SRL(P) + w2*Stab(P; SE,θ) - w3*GH_backlog(P) + w4*Tx_success(P)
```

## Next Steps in Chain
- suggest: [[S-DR-fitness-vs-srl-se]]

## Tags
#type/DF #layer/validation #domain/operational #concept/recursive-truth #concept/identity #symbol/Approx #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-change-instrumentation-scripts]]
- [[01_Statements/Clarification/S-CL-co-benchmark-targets]]
- [[01_Statements/Derivation/S-DR-fitness-vs-srl-se]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]; [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]
- Dependencies: [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]; [[01_Statements/Definition/S-DF-stabilization-energy]]; [[01_Statements/Definition/S-DF-self-similarity-threshold]]
- Successors: [[01_Statements/Derivation/S-DR-fitness-vs-srl-se]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

