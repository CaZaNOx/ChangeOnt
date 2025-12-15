---
id: stmt.rtv-fixedpoints
type: DF
aliases: ["FND_10.RTVFix"]
title: RTV fixed points and limit cycles
concepts: ["[[02_Concepts/C-recursive-truth]]"]
dependencies: ["[[01_Statements/Definition/S-DF-rtv-operator]]"]
parents: ["[[01_Statements/Definition/S-DF-rtv-operator]]"]
successors: ["[[01_Statements/Derivation/S-DR-rtv-collapse-threshold]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Breath]]"]
sources:
  - path: TheoryOfChange/02_Foundations/FND_10_RecursiveTruthValue.md:1
flags: []
tags: [layer/validation, domain/logical, stable, recursion, "type/DF", "concept/recursive-truth", "symbol/Breath"]
---
# RTV fixed points and limit cycles
## Claim (formal)
RTV yields acceptance when the validation mapping under breath F satisfies either a fixed point F(T)=T or an admissible limit cycle T_{k+m}=T_k within declared tolerances.

## Philosophical Translation (of formal claim)
Truth under change is what keeps returning to itself (or a small loop) under continued checking.

## Philosophical Justification
- [[S-DF-rtv-operator]] defines recursive validation; convergence behavior classifies robustness.
- Fixed points capture stable truths; short limit cycles capture tolerable oscillations (e.g., parity flips) within ε/σ(ε).
- Declaring admissible cycles prevents mislabeling noise-induced wandering as truth.

## Explanation (informal)
Run the check repeatedly; if the outcome stops moving or loops predictably inside tolerance, call it validated. Anything else signals instability or collapse.

## Clarifications / Further Context
- Admissibility depends on ε, σ(ε) and collapse criteria.
- Collapse thresholds and σ(ε) determine which cycles are allowed versus flagged.

## Derivation (Formal/Logical/Mathematical)
```text
Let F be validation update under breath.
Accept if ∃T: F(T)=T  (fixed point) or ∃m>0: T_{k+m}=T_k ∀k beyond burn-in, with |T_{k+1}-T_k|<ε.
```

## Proofs/Corollaries References
- corollary: informs [[S-DR-rtv-collapse-threshold]].

## Next Steps in Chain
- suggest: [[S-DR-rtv-collapse-threshold]]

## Tags
#type/DF #layer/validation #domain/logical #concept/recursive-truth #symbol/Breath #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-rtv-operator]]
- [[01_Statements/Derivation/S-DR-rtv-collapse-threshold]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]
- Parents: [[01_Statements/Definition/S-DF-rtv-operator]]
- Dependencies: [[01_Statements/Definition/S-DF-rtv-operator]]
- Successors: [[01_Statements/Derivation/S-DR-rtv-collapse-threshold]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

