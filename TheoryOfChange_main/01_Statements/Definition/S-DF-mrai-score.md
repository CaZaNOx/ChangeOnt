---
id: stmt.df-mrai-score
type: DF
title: Mutual Recognition & Agreement Index (MRAI)
concepts: ["[[02_Concepts/C-intersubject-gauge]]", "[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-intersubject-gauge]]", "[[01_Statements/Definition/S-DF-stabilization-energy]]"]
parents: ["[[01_Statements/Definition/S-DF-intersubject-gauge]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_19.md:292-295
flags: []
tags: [layer/operators, domain/operational, stable, metrics, intersubject, "type/DF", "concept/intersubject-gauge", "concept/identity-change"]
---
# Mutual Recognition & Agreement Index (MRAI)

## Claim (formal)
The MRAI score aggregates four facets of cross-subject alignment:

1. Mutual prediction `P`: subjects can forecast each other’s next state within the same tolerance.
2. Invariant distance `I`: shared invariants (gauges, spreads, holonomy) stay within a threshold under remapping.
3. Order alignment `A`: sequences of interactions exhibit the same holonomy signatures (`H` remains comparable).
4. Control concordance `C`: both subjects accept the same knobs/actions for steering.

Expressed as `MRAI = w_P P + w_I I + w_A A + w_C C` with weights tuned to the task, the index targets both epistemic coverage and operational consistency. Requiring `MRAI ≥ θ_agree` before declaring a shared OPS card ensures that subjects are not merely parallel, but truly mutually endorsing the same invariants.

## Philosophical Translation (of formal claim)
Alignment is more than shared outputs; it is mutual predictability, shared invariants, agreed ordering, and accepted controls.

## Philosophical Justification
- [[S-DF-intersubject-gauge]] supplies the shared frame; MRAI checks that the frame is actually shared in use.
- [[S-DF-stabilization-energy]] ensures alignment isn’t brittle; thresholds keep the score from ignoring stability.
- Aggregating P/I/A/C clarifies trade-offs; high prediction with low control concordance flags shallow agreement.

## Clarifications / Further Context
- Weights and thresholds are task-dependent; report them with the score.
- Should be logged with OPS cards to prevent premature claims of agreement.

## Next Steps in Chain
- suggest: benchmark MRAI against collapse/SE incidents in intersubject experiments.

## Tags
#type/DF #layer/operators #domain/operational #metrics #intersubject #concept/intersubject-gauge #concept/identity-change #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-intersubject-gauge]]; [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-intersubject-gauge]]
- Dependencies: [[01_Statements/Definition/S-DF-intersubject-gauge]]; [[01_Statements/Definition/S-DF-stabilization-energy]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

