---
id: stmt.reach-relation
type: DF
aliases: ["FND_2.Reach"]
title: Reach — transitive relation across change
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/Definition/S-DF-pointer-structural]]", "[[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]"]
parents: ["[[01_Statements/Definition/S-DF-pointer-structural]]"]
successors: []
symbols_used: ["[[01_Statements/SYMBOLS/Entailment]]"]
sources:
  - path: TheoryOfChange/02_Foundations/FND_2_PointerAndReach_FromSubjectiveChange.md:30
flags: []
tags: [foundations, logical, "type/DF", "concept/prior-pointer-reach"]
---
# Reach — transitive relation across change
## Claim (formal)
Reach(x,y) ∧ Reach(y,z) ⇒ Reach(x,z). The set {p | Reach(p, Now)} defines the local reach zone relative to Now.

## Philosophical Translation (of formal claim)
If the present can be reached from a prior, and that prior from another, then the present can be reached from that more distant point. This names the intuitive stitching of continuity as a structure, not a timeline.

## Philosophical Justification
“Reach” encodes the minimal shape of continuity that our pointer logic requires. Its transitivity is what turns isolated hints (pointers) into a navigable structure. We thus gain a way to talk about the neighborhood of the now without reifying time.

## Explanation (informal)
Think of reach as the compositional rule for change‑paths: stitching smaller steps yields a larger step in the same structure.

## Derivation (Philosophical)
- From [[S-DF-pointer-structural]] and non‑cessation: change supports path composition.

## Derivation (Formal/Logical/Mathematical)
```text
∀x,y,z [Reach(x,y) ∧ Reach(y,z) ⇒ Reach(x,z)]
LocalReach(Now) := { p | Reach(p, Now) }
```

## Clarifications / Further Context
- No linear time assumed; only composability of change‑paths.

## Next Steps in Chain
- Characterize LocalReach under ε, σ(ε) and pointer stability.

## Tags
#type/DF #layer/foundations #domain/logical #concept/prior-pointer-reach






























































































































<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-interaction-points-eventlets]]
- [[01_Statements/Corollary/S-CR-delta-now-implies-pointer]]
- [[01_Statements/Definition/S-DF-depth-reach]]
- [[01_Statements/Definition/S-DF-dimension-change]]
- [[01_Statements/Definition/S-DF-identity-through-change]]
- [[01_Statements/Definition/S-DF-locality-prior]]
- [[01_Statements/Definition/S-DF-localreach-topology]]
- [[01_Statements/Definition/S-DF-memory-trace-integration]]
- [[01_Statements/Definition/S-DF-path-eventlet-chain]]
- [[01_Statements/Definition/S-DF-pointer-structural]]
- [[01_Statements/Definition/S-DF-tx-operator]]
- [[01_Statements/Derivation/S-DR-pointer-behavior-under-tx]]
<!-- END:AUTOGEN:REFERENCED_BY -->











































































































































































































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/Definition/S-DF-pointer-structural]]
- Dependencies: [[01_Statements/Definition/S-DF-pointer-structural]]; [[01_Statements/FoundationalTruth/S-FT-continuity-noncessation]]
<!-- END:AUTOGEN:RELATIONSHIPS -->





































































































