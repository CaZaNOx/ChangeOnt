---
id: stmt.rtv-collapse-threshold
type: DR
aliases: ["FND_10.RTVCollapse"]
title: RTV collapse thresholds under ε, σ(ε)
concepts: ["[[02_Concepts/C-recursive-truth]]"]
dependencies: ["[[01_Statements/Definition/S-DF-rtv-fixedpoints]]", "[[01_Statements/Definition/S-DF-stabilization-energy]]"]
parents: ["[[01_Statements/Definition/S-DF-rtv-fixedpoints]]"]
successors: ["[[01_Statements/Clarification/S-CL-rtv-collapse-regimes]]", "[[01_Statements/Clarification/S-CL-truth-resilience-collapse]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Breath]]", "[[01_Statements/SYMBOLS/Epsilon]]", "[[01_Statements/SYMBOLS/Sigma_epsilon]]"]
sources:
  - path: TheoryOfChange/02_Foundations/FND_10_RecursiveTruthValue.md:1
flags: []
tags: [layer/validation, domain/logical, stable, recursion, "type/DR", "concept/recursive-truth", "symbol/Breath", "symbol/Epsilon", "symbol/Sigma_epsilon"]
---
# RTV collapse thresholds under ε, σ(ε)
## Claim (formal)
If the breath validation mapping F fails to reach a fixed point or admissible cycle within declared iteration and tolerance budgets (ε, σ(ε)), collapse ⊘ is triggered for the claim at the given resolution.

## Philosophical Translation (of formal claim)
If repeated checking cannot settle into stability (given our resolution), we declare the claim not validated here and now.

## Philosophical Justification
- [[S-DF-rtv-fixedpoints]] defines acceptable convergence modes; failure to reach them is non‑validation.
- [[S-DF-stabilization-energy]] bounds how long validation can be maintained; insufficient SE can force collapse before convergence.
- Declaring collapse is resolution-dependent (ε, σ(ε)); this prevents overclaiming robustness.

## Clarifications / Further Context
- Collapse is local to resolution; different ε, σ(ε) may yield different outcomes; SE informs robustness across settings.
- Collapse does not falsify the claim globally; it marks failure to validate under current resolution/energy.

## Derivation (Formal/Logical/Mathematical)
```text
Given F and tolerances (ε, σ):
If ∄ fixed point or admissible m-cycle within N iterations
   OR SE_budget exhausted before convergence
then mark ⊘(claim, ε, σ).
```

## Proofs/Corollaries References
- clarification: [[S-CL-rtv-collapse-regimes]]
- clarification: [[S-CL-truth-resilience-collapse]]

## Next Steps in Chain
- suggest: [[S-CL-rtv-collapse-regimes]]
- suggest: [[S-CL-truth-resilience-collapse]]

## Tags
#type/DR #layer/validation #domain/logical #concept/recursive-truth #symbol/Breath #symbol/Epsilon #symbol/Sigma_epsilon #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]
- Parents: [[01_Statements/Definition/S-DF-rtv-fixedpoints]]
- Dependencies: [[01_Statements/Definition/S-DF-rtv-fixedpoints]]; [[01_Statements/Definition/S-DF-stabilization-energy]]
- Successors: [[01_Statements/Clarification/S-CL-rtv-collapse-regimes]]; [[01_Statements/Clarification/S-CL-truth-resilience-collapse]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

