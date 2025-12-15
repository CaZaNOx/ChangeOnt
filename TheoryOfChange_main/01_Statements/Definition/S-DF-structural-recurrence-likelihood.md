---
id: stmt.structural-recurrence-likelihood
type: DF
aliases: ["AI13.SRL"]
title: Structural Recurrence Likelihood (SRL)
concepts: ["[[02_Concepts/C-recursive-truth]]", "[[02_Concepts/C-markov-closure]]"]
dependencies: ["[[01_Statements/Definition/S-DF-rtv-operator]]", "[[01_Statements/Definition/S-DF-identity-through-change]]"]
parents: ["[[01_Statements/Definition/S-DF-rtv-operator]]"]
successors: ["[[01_Statements/Derivation/S-DR-srl-vs-se-theta]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Breath]]", "[[01_Statements/SYMBOLS/Approx]]"]
sources:
  - path: TheoryOfChange/00_Meta/AI_Summaries/AI_13_THEORY_ONLY.md:24
flags: []
tags: [layer/validation, domain/logical, stable, recursion, "type/DF", "concept/recursive-truth", "concept/markov-closure", "symbol/Breath", "symbol/Approx"]
---
# Structural Recurrence Likelihood (SRL)
## Claim (formal)
SRL(P) := normalized recurrence score of pattern P under breath validation across LocalReach, serving as a surrogate for classical probability when frames and identities shift.

## Philosophical Translation (of formal claim)
Instead of asking “how probable” in a fixed space, we ask “how reliably does this pattern recur” as the system breathes and adjusts.

## Philosophical Justification
- [[S-DF-rtv-operator]]: validation is iterative; SRL summarizes recurrence of acceptance events.
- [[S-DF-identity-through-change]]: recurrence must respect identity criteria (≈, invariants); otherwise counts are meaningless.
- Classical probability assumes fixed sample space; SRL adapts to shifting frames/local reach by using breath-indexed recurrence.

## Explanation (informal)
SRL is “how often this thing keeps showing up as itself” under ongoing checks. It replaces naive frequencies when the space itself morphs.

## Clarifications / Further Context
- SRL composes with identity criteria (≈, invariants) and depends on RTV stability.
- SRL is windowed: declare the breath window and frame; SRL can drift as frames shift.

## Derivation (Formal)
```text
Let K be a validation window. SRL(P) := (1/|K|) * |{ k∈K : RTV_k(P) accepts ∧ Sim(T_k(P),P)≥θ }|
```

## Proofs/Corollaries References
- derivation continues in [[S-DR-srl-vs-se-theta]] comparing SRL to SE thresholds.

## Next Steps in Chain
- suggest: [[S-DR-srl-vs-se-theta]]

## Tags
#type/DF #layer/validation #domain/logical #concept/recursive-truth #concept/markov-closure #symbol/Breath #symbol/Approx #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]; [[02_Concepts/C-markov-closure]]
- Parents: [[01_Statements/Definition/S-DF-rtv-operator]]
- Dependencies: [[01_Statements/Definition/S-DF-rtv-operator]]; [[01_Statements/Definition/S-DF-identity-through-change]]
- Successors: [[01_Statements/Derivation/S-DR-srl-vs-se-theta]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

