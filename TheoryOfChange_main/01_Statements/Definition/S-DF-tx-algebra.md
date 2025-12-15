---
id: stmt.tx-algebra
type: DF
aliases: ["FND_6.TxAlg"]
title: Algebra of frame operators (Tx)
concepts: ["[[02_Concepts/C-frame-operators]]"]
dependencies: ["[[01_Statements/Definition/S-DF-tx-operator]]", "[[01_Statements/Definition/S-DF-localreach-topology]]"]
parents: ["[[01_Statements/Definition/S-DF-tx-operator]]"]
successors: ["[[01_Statements/Derivation/S-DR-dimension-variation]]", "[[01_Statements/Definition/S-DF-cross-audit-markov-gh-tx]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_6_TransformationOperator_Tx.md:1
flags: []
tags: [layer/operators, domain/logical, stable, "type/DF", "concept/frame-operators"]
---
# Algebra of frame operators (Tx)
## Claim (formal)
Tx operators compose and admit identity elements relative to frames: (Tx, ∘, I) with domain of definition restricted by LocalReach and frame-compatibility. Composition respects reach: if Tx₁: (S, F)→(S₁, F₁) and Tx₂: (S₁, F₁)→(S₂, F₂), then Tx₂∘Tx₁: (S, F)→(S₂, F₂).

## Philosophical Translation (of formal claim)
Frame changes can be chained consistently; some do nothing (identity). Not all chains are allowed — only those whose endpoints can be reached.

## Philosophical Justification
- Without an algebra, frame shifts would be ad hoc; we need closure/identity to reason about sequences of meta-changes.
- LocalReach constraints mean some frame jumps are undefined; the algebra encodes this via partial composition rather than pretending universality.
- Identity Tx exposes when “no change” is well-defined; failures here surface non-closure that GH/Audit must record.

## Clarifications / Further Context
- Closure here is about the algebra of Tx on admissible frames, not about fixed‑space Markov closure.
- Inverses may fail or be partial; record collapse ⊘ where composition breaks.
- Supports audits: explicit algebra reveals when Tx use breaks assumed closure.

## Derivation (Formal)
```text
Define Dom(Tx) ⊆ LocalReach×Frames. If (x,F)∈Dom(Tx₁) and Tx₁(x,F)=(x₁,F₁), and (x₁,F₁)∈Dom(Tx₂), define Tx₂∘Tx₁(x,F)=(x₂,F₂).
I(x,F)=(x,F).
```

## Next Steps in Chain
- suggest: [[S-DR-dimension-variation]]
- suggest: [[S-DF-cross-audit-markov-gh-tx]]
- suggest: audit cards for Tx classes listing domain guards, inverses, and collapse conditions.

## Next Steps in Chain
- suggest: [[S-DR-dimension-variation]]
- suggest: [[S-DF-cross-audit-markov-gh-tx]]

## Tags
#type/DF #layer/operators #domain/logical #concept/frame-operators #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-tx-operator]]
- [[01_Statements/Derivation/S-DR-dimension-variation]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-frame-operators]]
- Parents: [[01_Statements/Definition/S-DF-tx-operator]]
- Dependencies: [[01_Statements/Definition/S-DF-tx-operator]]; [[01_Statements/Definition/S-DF-localreach-topology]]
- Successors: [[01_Statements/Derivation/S-DR-dimension-variation]]; [[01_Statements/Definition/S-DF-cross-audit-markov-gh-tx]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

