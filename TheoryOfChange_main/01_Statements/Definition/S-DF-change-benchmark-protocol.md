---
id: stmt.change-benchmark-protocol
type: DF
aliases: ["AI13.Benchmark"]
title: Change-based benchmark protocol
concepts: ["[[02_Concepts/C-markov-closure]]", "[[02_Concepts/C-recursive-truth]]"]
dependencies: ["[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]", "[[01_Statements/Definition/S-DF-nonclassical-indicators]]", "[[01_Statements/Definition/S-DF-stabilization-energy]]"]
parents: ["[[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]"]
successors: ["[[01_Statements/Derivation/S-DR-benchmark-scores]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md:27
flags: []
tags: [layer/validation, domain/logical, stable, "type/DF", "concept/markov-closure", "concept/recursive-truth"]
---
# Change-based benchmark protocol
## Claim (formal)
Benchmarks must report: SRL, identity persistence (SE, θ), indicator incidence (non‑classical triggers), and collapse rates (⊘) under breath, alongside classical baselines.

## Philosophical Translation (of formal claim)
Test what matters in change: recurrence, robustness, and where fixed‑space models silently fail.

## Philosophical Justification
- [[S-DF-structural-recurrence-likelihood]] captures recurrence; [[S-DF-stabilization-energy]] captures identity robustness.
- [[S-DF-nonclassical-indicators]] detect structural shifts requiring Tx/GH handling; benchmarks must surface them.
- Comparing against classical baselines reveals where closure assumptions break and change-aware models add value.

## Clarifications / Further Context
- Report not just accuracy but structure: GH incidence, Tx needs, collapse rates, and SE/SRL summaries.
- Use breath-aware protocols; declare ε/σ settings and gates.

## Next Steps in Chain
- suggest: [[S-DR-benchmark-scores]]
- suggest: [[S-DR-predictive-statement-nonclassical]]

## Tags
#type/DF #layer/validation #domain/logical #concept/markov-closure #concept/recursive-truth #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-driff-guarded-lln]]
- [[01_Statements/Clarification/S-CL-drift-guarded-lln]]
- [[01_Statements/Clarification/S-CL-evaluation-rigor]]
- [[01_Statements/Derivation/S-DR-benchmark-scores]]
- [[01_Statements/Derivation/S-DR-predictive-statement-nonclassical]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-markov-closure]]; [[02_Concepts/C-recursive-truth]]
- Parents: [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]
- Dependencies: [[01_Statements/Definition/S-DF-structural-recurrence-likelihood]]; [[01_Statements/Definition/S-DF-nonclassical-indicators]]; [[01_Statements/Definition/S-DF-stabilization-energy]]
- Successors: [[01_Statements/Derivation/S-DR-benchmark-scores]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

