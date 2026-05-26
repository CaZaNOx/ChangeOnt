---
id: stmt.proof-as-reachability
type: CR
aliases: ["LOG2.C1.ProofReach"]
title: Proof as reachability; disjunction as min-join (⊕)
concepts: ["[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-quantale-logic]]", "[[01_Statements/Derivation/S-DR-quantale-evidence-composition]]"]
parents: ["[[01_Statements/Definition/S-DF-quantale-logic]]"]
successors: ["[[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]", "[[01_Statements/Derivation/S-DR-quantale-residuation-implication]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Compose_tensor]]", "[[01_Statements/SYMBOLS/Join_min]]"]
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5365
flags: []
tags: [corollary, logic, quantale, stable, "type/CR", "concept/math-structures"]
---
# Proof as reachability; disjunction as min-join (⊕)
## Statement (corollary)
In quantale logic, composition (⊗) encodes a proof path: A ⊗ B is “do A then B.” Disjunction/aggregation is min‑join (⊕), keeping the least‑cost route. Therefore proving is reachability with minimal effort, and “or” means “take the easiest path.”

## Philosophical Translation
To prove is to reach the target by chaining steps; “or” keeps the cheapest alternative.

## Philosophical Justification
Proof behaves like navigation: steps compose, order matters, and redundant longer routes are discarded. Modeling inference as path algebra preserves these intuitions and clarifies that classical proof search is a special case of path search in a graded space.

## Derivation (Formal/Logical/Mathematical)
- From [[S-DR-quantale-evidence-composition]], ⊗ composes evidential costs via inf‑convolution.
- Join ⊕ is pointwise min, so A⊕B chooses the cheaper of two proofs.
- Minimality: if A⊗B reaches the goal, any higher‑cost alternative is dominated by monotonicity.

## Proofs/Corollaries References
- Boolean limit: [[S-DR-quantale-boolean-flattening-proof]] collapses graded paths to classical trees.
- Residuation/implication: [[S-DR-quantale-residuation-implication]] captures “what remains to be shown.”

## Clarifications / Further Context
- Works for support‑style weights by order reversal (max‑plus variant).
- Reachability spans state graphs, program traces, and inference chains.

## Next Steps in Chain
- suggest: [[S-DR-quantale-boolean-flattening-proof]]
- suggest: [[S-DR-quantale-residuation-implication]]

## Tags
#type/CR #layer/foundations #domain/logic #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]
- [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]
- [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-quantale-logic]]
- Dependencies: [[01_Statements/Definition/S-DF-quantale-logic]]; [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]
- Successors: [[01_Statements/Derivation/S-DR-quantale-boolean-flattening-proof]]; [[01_Statements/Derivation/S-DR-quantale-residuation-implication]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

