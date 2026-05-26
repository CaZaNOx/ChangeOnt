---
id: stmt.fitness-vs-srl-se
type: DR
aliases: ["AI13.FitnessVsSRLSE"]
title: Fitness vs SRL/SE — thresholds and trade-offs
concepts: ["[[02_Concepts/C-recursive-truth]]", "[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-change-fitness]]"]
parents: ["[[01_Statements/Definition/S-DF-change-fitness]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md:17
flags: []
tags: [layer/validation, domain/operational, stable, "type/DR", "concept/recursive-truth", "concept/identity"]
---
# Fitness vs SRL/SE — thresholds and trade-offs
## Claim (formal)
Relate fitness CBF to its components by specifying threshold bands: e.g., CBF high requires SRL ≥ θ_srl, SE ≥ θ_se, GH_backlog ≤ τ_gh, and Tx_success flagged. Derive trade-offs where marginal SRL gains cannot compensate SE collapse or GH backlog growth.

## Philosophical Translation (of formal claim)
You can’t call something “fit” if it recurs a lot but falls apart or hides its gaps; thresholds make the trade-offs explicit.

## Derivation (Formal/Operational)
```text
CBF ≥ θ_fit only if
  SRL ≥ θ_srl
  SE ≥ θ_se
  GH_backlog ≤ τ_gh
  Tx_success documented
Otherwise CBF capped even if SRL is high.
```
Trade-off rule: if ΔSRL < k·ΔSE_loss or GH backlog grows beyond τ_gh, fitness score decreases.

## Clarifications / Further Context
- Thresholds are domain-specific; must be declared per benchmark.
- Prevents over-reliance on SRL when identity stability is weak or audits are failing.

## Next Steps in Chain
- integrate with benchmark scoring and evaluation rigor clarifications.

## Tags
#type/DR #layer/validation #domain/operational #concept/recursive-truth #concept/identity #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-change-fitness]]
- [[01_Statements/Definition/S-DF-stabilization-energy]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]; [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-change-fitness]]
- Dependencies: [[01_Statements/Definition/S-DF-change-fitness]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

