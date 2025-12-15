---
id: stmt.math-structures-closure
type: DR
aliases: ["FND_13.StructureClosure"]
title: Structure closure and extension under Tx
concepts: ["[[02_Concepts/C-math-structures]]", "[[02_Concepts/C-frame-operators]]"]
dependencies: ["[[01_Statements/Definition/S-DF-math-structures]]", "[[01_Statements/Definition/S-DF-tx-operator]]"]
parents: ["[[01_Statements/Definition/S-DF-math-structures]]"]
successors: ["[[01_Statements/Corollary/S-CR-nonclosure-under-tx]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_13_MathStructures.md:1
  - path: TheoryOfChange/02_Foundations/FND_6_TransformationOperator_Tx.md:1
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DR", "concept/math-structures", "concept/frame-operators"]
---
# Structure closure and extension under Tx
## Claim (formal)
When Tx induces nonclosure in the chosen structure, extend the structure or switch to one that represents Tx, logging GH if neither is feasible.

## Philosophical Translation (of formal claim)
We change our math to fit the change — and we say so when we can’t yet.

## Philosophical Justification
- From [[S-DF-math-structures]]: structures are chosen to respect reach, invariants, and Tx. If Tx breaks closure, the structure is inadequate for the phenomena.
- Recording Gödel-hole (GH) status keeps the ontology honest about current limits.

## Explanation (informal)
If your operators leave the space, either enlarge the space, pick a better one, or admit a hole. Don’t pretend closure you don’t have.

## Derivation (Philosophical)
- Detect nonclosure: ∃x, Tx(x) ∉ structure domain.
- Option A: extend structure minimally to include Tx(x) and retain required properties.
- Option B: switch to an alternate structure compatible with Tx and invariants.
- Option C: log GH if neither A nor B is available.

## Derivation (Formal/Logical/Mathematical)
```text
If T: S→S' with S' ≠ S, choose S'' ⊇ S ∪ S' s.t. properties(P) hold, or choose S_alt with closure(T).
Else mark GH(T,S).
```

## Proofs/Corollaries References
- corollary: [[S-CR-nonclosure-under-tx]].

## Clarifications / Further Context
- “Extension” must preserve declared invariants and validation semantics; arbitrary supersets not allowed.
- GH log ties to godel-hole tracking in derivation chains.

## Next Steps in Chain
- suggest: [[S-CR-nonclosure-under-tx]]

## Tags
#type/DR #layer/foundations #domain/formal #concept/math-structures #concept/frame-operators #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-math-structures]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]; [[02_Concepts/C-frame-operators]]
- Parents: [[01_Statements/Definition/S-DF-math-structures]]
- Dependencies: [[01_Statements/Definition/S-DF-math-structures]]; [[01_Statements/Definition/S-DF-tx-operator]]
- Successors: [[01_Statements/Corollary/S-CR-nonclosure-under-tx]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

