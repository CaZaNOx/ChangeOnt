---
id: stmt.pointer-structural
type: DF
aliases: ["FND_2.Pointer"]
title: Pointer — Structural implication from Δ(Now)
concepts: ["[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]
parents: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]
successors: ["[[01_Statements/Definition/S-DF-reach-relation]]", "[[01_Statements/Corollary/S-CR-delta-now-implies-pointer]]"]
symbols_used: ["[[01_Statements/SYMBOLS/Pointer_field]]", "[[01_Statements/SYMBOLS/Pointer_local]]"]
sources:
  - path: TheoryOfChange/02_Foundations/FND_2_PointerAndReach_FromSubjectiveChange.md:1
  - path: TheoryOfChange/02_Foundations/DerChain.md:1
flags: []
tags: [foundations, logical, "type/DF", "concept/prior-pointer-reach"]
---
# Pointer — Structural implication from Δ(Now)
## Claim (formal)
Pointer(Now) := ∃p [p ≠ Now ∧ Reach(p, Now)], inferred from Δ(Now) without presupposing memory or linear time.

## Philosophical Translation (of formal claim)
If change is happening in the now, then the now implicitly points beyond itself: there is an elsewhere, even if we cannot name it. The pointer is a structural tension in experience, not a recalled fact.

## Philosophical Justification
With only Δ at hand, the subject can still sense a difference that implies “not‑now.” This does not reintroduce time or memory; it records the minimal implication of difference: a beyond‑this. Calling that relation a pointer emphasizes that it is directional and structural — a way the present refers to what it is not.

## Explanation (informal)
Pointers (⇘/↶) are the bookkeeping of minimal reach. They enable reasoning about continuity without requiring a timeline or storage of prior states.

## Derivation (Philosophical)
- From [[S-FT-immediate-datum]]: Δ(Now) entails discriminability.
- Discriminability implies an “elsewhere” (not‑now) that the present points toward.

## Derivation (Formal/Logical/Mathematical)
```text
Δ(Now) ⇒ ∃p:\; p ≠ Now ∧ Reach(p, Now) \equiv Pointer(Now)
```

## Proofs/Corollaries References
- corollary: [[S-CR-delta-now-implies-pointer]]

## Clarifications / Further Context
- Pointers are structural traces, not memories.
- Both field (⇘) and local (↶) pointers may be used depending on scope.

## Next Steps in Chain
- Develop reach relation and local reach zone.

## Tags
#type/DF #layer/foundations #domain/logical #concept/prior-pointer-reach






























































































































<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-interaction-points-eventlets]]
- [[01_Statements/Clarification/S-CL-pointer-structural-not-causal]]
- [[01_Statements/Corollary/S-CR-delta-now-implies-pointer]]
- [[01_Statements/Corollary/S-CR-prior-with-change]]
- [[01_Statements/Counterfactual/S-CF-pointer-diff-equals]]
- [[01_Statements/Definition/S-DF-godel-hole-pointer]]
- [[01_Statements/Definition/S-DF-locality-prior]]
- [[01_Statements/Definition/S-DF-nonclassical-indicators]]
- [[01_Statements/Definition/S-DF-reach-relation]]
- [[01_Statements/Definition/S-DF-tx-operator]]
- [[01_Statements/Derivation/S-DR-pointer-behavior-under-tx]]
<!-- END:AUTOGEN:REFERENCED_BY -->











































































































































































































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
- Dependencies: [[01_Statements/FoundationalTruth/S-FT-immediate-datum]]
- Successors: [[01_Statements/Definition/S-DF-reach-relation]]; [[01_Statements/Corollary/S-CR-delta-now-implies-pointer]]
<!-- END:AUTOGEN:RELATIONSHIPS -->





































































































