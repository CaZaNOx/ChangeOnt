---
id: stmt.identity-invariants
type: DF
aliases: ["COT_5.Invariants"]
title: Identity invariants — what remains through change
concepts: ["[[02_Concepts/C-identity-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-identity-through-change]]", "[[01_Statements/Definition/S-DF-similarity-operator]]"]
parents: ["[[01_Statements/Definition/S-DF-identity-through-change]]"]
successors: ["[[01_Statements/Definition/S-DF-self-similarity-threshold]]", "[[01_Statements/Definition/S-DF-stabilization-energy]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Identity]]", "[[01_Statements/SYMBOLS/Approx]]"]
sources:
  - path: TheoryOfChange/01_CoreOntology/COT_5_Self_Similarity_and_the_Emergence_of_Identity.md:80
flags: []
tags: [layer/foundations, domain/ontological, foundations, "type/DF", "concept/identity", "symbol/Identity", "symbol/Approx", status/stable]
---
# Identity invariants — what remains through change
## Claim (formal)
Let I be a declared set of invariants. Identity(P) holds across window K if for all k∈K, Inv(T_k(P))=Inv(P) for all Inv∈I and T_k(P)≈P under Sim.

## Philosophical Translation (of formal claim)
What makes a thing the same is not the absence of change, but the preservation of key relations/features while other aspects vary.

## Philosophical Justification
Identity in continuous change ([[01_Statements/Definition/S-DF-identity-through-change]]) requires explicit criteria for “same enough.” Declaring invariants plus ≈ (from [[01_Statements/Definition/S-DF-similarity-operator]]) prevents equivocation. The window K fixes the span (e.g., LocalReach steps, breath cycles) over which invariants are tested; without a declared window, claims of persistence are underspecified.

## Clarifications / Further Context
- Invariants can be structural (topology), relational (graphs), or conserved quantities; they must be declared to avoid equivocation.
- Coherence markers: track a small set of markers (e.g., invariant features, ≈ thresholds, SE trends) that signal identity persistence across cycles; these interface with attention thresholds to prioritize stabilization.
- K is the evaluation span (e.g., a path segment in LocalReach or a breath window) over which invariants are checked and similarity is aggregated.

## Derivation (Formal)
```text
I = {Inv_j};  ∀k,j: Inv_j(T_k(P)) = Inv_j(P)  ∧  Sim(T_k(P), P) ≥ θ.
```

## Tags
#type/DF #layer/foundations #domain/ontological #concept/identity #symbol/Identity #symbol/Approx

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-change-not-mere-flux]]
- [[01_Statements/Clarification/S-CL-classical-embedding]]
- [[01_Statements/Clarification/S-CL-invariance-as-derivative]]
- [[01_Statements/Corollary/S-CR-change-ontically-prior]]
- [[01_Statements/Corollary/S-CR-complexity-no-fundamental-simplicity]]
- [[01_Statements/Corollary/S-CR-identity-as-phase-resonance]]
- [[01_Statements/Corollary/S-CR-laws-as-robust-invariants]]
- [[01_Statements/Definition/S-DF-attention-focus]]
- [[01_Statements/Definition/S-DF-co-spread-number]]
- [[01_Statements/Definition/S-DF-evaluation-surface]]
- [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- [[01_Statements/Definition/S-DF-identity-through-change]]
- [[01_Statements/Definition/S-DF-intersubject-translation-resonance]]
- [[01_Statements/Definition/S-DF-math-structures]]
- [[01_Statements/Definition/S-DF-self-similarity-threshold]]
- [[01_Statements/Definition/S-DF-similarity-operator]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/Definition/S-DF-identity-through-change]]
- Dependencies: [[01_Statements/Definition/S-DF-identity-through-change]]; [[01_Statements/Definition/S-DF-similarity-operator]]
- Successors: [[01_Statements/Definition/S-DF-self-similarity-threshold]]; [[01_Statements/Definition/S-DF-stabilization-energy]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

