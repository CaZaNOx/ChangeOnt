---
id: stmt.similarity-operator
type: DF
aliases: ["COT_5.Sim"]
title: Similarity operator (≈) and Sim
concepts: ["[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-identity-through-change]]", "[[01_Statements/Definition/S-DF-self-similarity-threshold]]"]
parents: ["[[01_Statements/Definition/S-DF-identity-through-change]]"]
successors: ["[[01_Statements/Definition/S-DF-identity-invariants]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Approx]]", "[[01_Statements/SYMBOLS/Epsilon]]", "[[01_Statements/SYMBOLS/Sigma_epsilon]]", "[[01_Statements/SYMBOLS/Theta]]"]
sources:
  - path: TheoryOfChange/01_CoreOntology/COT_5_Self_Similarity_and_the_Emergence_of_Identity.md:60
flags: []
tags: [layer/foundations, domain/ontological, foundations, "type/DF", "concept/identity", "symbol/Approx", "symbol/Epsilon", "symbol/Sigma_epsilon", "symbol/Theta", status/stable]
---
# Similarity operator (≈) and Sim
## Claim (formal)
Define a context-dependent similarity functional Sim(X,Y)∈[0,1] and write X≈Y iff Sim(X,Y)≥θ for declared threshold θ under tolerances (ε, σ(ε)).

## Philosophical Translation (of formal claim)
“Close enough to count as the same” is not vague handwaving: it is a declared criterion with thresholds and resolutions.

## Philosophical Justification
Identity in continuous change (see [[01_Statements/Definition/S-DF-identity-through-change]]) requires explicit criteria for “same enough.” Declaring Sim plus θ, ε, σ(ε) keeps ≈ auditable and prevents equivocation across contexts.

## Clarifications / Further Context
- Sim must be specified per domain (relational invariants, metric projections, feature correspondences, etc.).
- θ and (ε,σ(ε)) make ≈ auditable and comparable across settings.

## Derivation (Formal)
```text
X≈Y  ⇔  Sim(X,Y) ≥ θ;  Sim: D×D→[0,1],  with declared ε, σ(ε), θ.
```

## Tags
#type/DF #layer/foundations #domain/ontological #concept/identity #symbol/Approx #symbol/Epsilon

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-co-logic-graded-order]]
- [[01_Statements/Definition/S-DF-difference-operator]]
- [[01_Statements/Definition/S-DF-identity-invariants]]
- [[01_Statements/Definition/S-DF-locality-threshold]]
- [[01_Statements/Definition/S-DF-metric-space-emergent]]
- [[01_Statements/Definition/S-DF-prm-closure-quotient]]
- [[01_Statements/Definition/S-DF-prm-reid-kernel]]
- [[01_Statements/Definition/S-DF-self-similarity-threshold]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-identity-through-change]]
- Dependencies: [[01_Statements/Definition/S-DF-identity-through-change]]; [[01_Statements/Definition/S-DF-self-similarity-threshold]]
- Successors: [[01_Statements/Definition/S-DF-identity-invariants]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

