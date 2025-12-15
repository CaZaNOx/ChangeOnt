---
id: stmt.tx-operator
type: DF
aliases: ["FND_6.Tx"]
title: Transformation Operator (Tx) — frame-level change
concepts: ["[[02_Concepts/C-frame-operators]]"]
dependencies: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]", "[[01_Statements/Definition/S-DF-pointer-structural]]", "[[01_Statements/Definition/S-DF-reach-relation]]"]
parents: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]
successors: ["[[01_Statements/Definition/S-DF-tx-algebra]]", "[[01_Statements/Derivation/S-DR-pointer-behavior-under-tx]]", "[[01_Statements/Corollary/S-CR-nonclosure-under-tx]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_6_TransformationOperator_Tx.md:1
  - path: TheoryOfChange/02_Foundations/DerChain.md:1
flags: []
tags: [layer/operators, domain/logical, stable, "type/DF", "concept/frame-operators"]
---
# Transformation Operator (Tx) — frame-level change
## Claim (formal)
Tx acts on the configuration of the subject/space itself (frame), not merely on states within a fixed frame. Tx: (S, Frame) → (S', Frame').

## Philosophical Translation (of formal claim)
Some changes modify the rules under which change is described. Tx names those meta‑changes: they alter the background against which states make sense.

## Philosophical Justification
If pointers and reach track structure within a frame, we also need operators that account for frame shifts themselves. Otherwise, we misdescribe meta‑change as intraframe transitions and lose what is distinctive: variable identity conditions, novel invariants, or new observables.

## Explanation (informal)
Tx is a placeholder for a class of operators (to be formalized) that rotate, lift, or re‑parameterize the subject/space, making frame transitions explicit in the ontology.

## Derivation (Philosophical)
- From [[S-FT-immediate-datum]] we only know change/experience is given; tracking it requires Reach/Pointer. When change alters the very frame in which reach is defined, a separate operator is needed.
- Frame shifts alter what counts as identity, Sim, and admissible moves; without Tx, those shifts look like violations rather than structured transitions.

## Derivation (Formal/Logical/Mathematical)
```text
Tx: (S,F) ↦ (S',F')
Well-defined iff LocalReach_F → LocalReach_F' mapping preserves pointer coherence on overlap.
```
Define a domain guard: Tx is admissible only if reachability in F and F' overlaps on an interface where identities can be matched.

## Clarifications / Further Context
- Tx should integrate with pointer behavior (⇘² for meta‑monitoring), and with reach so that paths across frames compose properly.
- Frame shifts change identity criteria; Tx must carry updated invariants/similarity rules.
- Tx is not arbitrary: each Tx must declare (i) frame pre/post conditions, (ii) how identity/Sim lift across, (iii) how SE budgets are transformed.
- Use Tx to expose non-closure (see [[S-CR-nonclosure-under-tx]]) rather than to hide it.

## Next Steps in Chain
- Specify algebra (composition, identity) and interaction with collapse/repair.
- suggest: [[S-DF-tx-algebra]]
- suggest: [[S-DR-pointer-behavior-under-tx]]
- suggest: [[S-CR-nonclosure-under-tx]]

## Tags
#type/DF #layer/operators #domain/logical #concept/frame-operators #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Corollary/S-CR-external-asymmetry-prevents-closure]]
- [[01_Statements/Corollary/S-CR-nonclosure-under-tx]]
- [[01_Statements/Corollary/S-CR-qm-no-privileged-substrate]]
- [[01_Statements/Definition/S-DF-across-scales-godel-structure]]
- [[01_Statements/Definition/S-DF-cross-audit-markov-gh-tx]]
- [[01_Statements/Definition/S-DF-domain-generalization-principles]]
- [[01_Statements/Definition/S-DF-godel-hole-pointer]]
- [[01_Statements/Definition/S-DF-math-structures]]
- [[01_Statements/Definition/S-DF-nonclassical-indicators]]
- [[01_Statements/Definition/S-DF-tx-algebra]]
- [[01_Statements/Derivation/S-DR-dimension-variation]]
- [[01_Statements/Derivation/S-DR-gh-review-loop]]
- [[01_Statements/Derivation/S-DR-math-structures-closure]]
- [[01_Statements/Derivation/S-DR-pointer-behavior-under-tx]]
- [[01_Statements/Derivation/S-DR-predictive-statement-nonclassical]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-frame-operators]]
- Parents: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
- Dependencies: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]; [[01_Statements/Definition/S-DF-pointer-structural]]; [[01_Statements/Definition/S-DF-reach-relation]]
- Successors: [[01_Statements/Definition/S-DF-tx-algebra]]; [[01_Statements/Derivation/S-DR-pointer-behavior-under-tx]]; [[01_Statements/Corollary/S-CR-nonclosure-under-tx]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

