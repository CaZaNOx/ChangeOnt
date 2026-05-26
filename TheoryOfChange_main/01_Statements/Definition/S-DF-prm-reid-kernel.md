---
id: stmt.prm-reid-kernel
type: DF
aliases:
- PRM_4
- ReIDKernel
- P4
title: Re-identification kernel from admissible continuity
concepts:
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/026_S-DF-identity-recognition-structure]]'
- '[[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]'
parents:
- '[[01_Statements/02_Outer_Formation/026_S-DF-identity-recognition-structure]]'
successors:
- '[[01_Statements/Definition/S-DF-elm-ec-identity]]'
symbols_used: []
sources:
- path: TheoryOfChange/02_Foundations/DerChain.md
flags: []
tags:
- layer/kernel
- domain/ontological
- type/DF
- status/stable
- strand/ontological
---
# Re-identification kernel from admissible continuity
## Claim (formal)
Re-identification is the primitive kernel that decides or tracks sameness-through-change from the identity-recognition structure together with preserved invariant-content. Gauge may refine cross-context transport later but is not a precondition of re-identification itself.

## Philosophical Translation (of formal claim)
To re-identify something is not to find an unchanged point. It is to judge that continuity under transformation remains admissible enough to count as the same ongoing identity-process.

## Philosophical Justification
[[01_Statements/02_Outer_Formation/026_S-DF-identity-recognition-structure]] establishes the recognition side of identity: graded comparison, admissibility, and any later thresholded sharpening. [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]] then states what content is actually preserved within that recognized continuity. Re-identification therefore comes from recognized admissible continuity together with preserved invariant-content; it should not depend on gauge as if transport/alignment were ontologically prior to identity-recognition itself.

## Explanation (informal)
ReID is the kernel primitive that turns continuity-through-change into an operationally usable sameness judgment. It works over admissible persistence rather than exact point equality.

## Derivation (Philosophical)
- Identity-through-change requires recognition structure.
- Recognition structure yields admissible and sharpened continuity judgments.
- Identity invariants specify what preserved content survives within that recognized continuity.
- Re-identification is the primitive handle that uses these ingredients to track sameness-through-change.

## Derivation (Formal/Logical/Mathematical)
```text
ReID(P_t, P_{t+k}) is grounded in identity-recognition structure over recognized admissible continuity together with preserved invariant-content.
```

## Clarifications / Further Context
- This file should be read as a **kernel-resolution primitive handle**, not as one of the earliest ontological distinctions after change.
- Gauge may later improve cross-frame transport of ReID judgments.
- ReID is not exact point equality.
- ReID is the primitive precursor used by richer identity elements such as EC.

## Active-chain status
**Status band:** derived-but-weaker  
**Reason:** the move from admissible continuity to re-identification is clearly motivated, but the exact final formal law remains implementation-sensitive.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]
- [[01_Statements/Definition/S-DF-elm-ec-identity]]
- [[01_Statements/Definition/S-DF-ops-j4a-reid-closure]]
- [[01_Statements/Definition/S-DF-prm-bend-metric]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/02_Outer_Formation/026_S-DF-identity-recognition-structure]]
- Dependencies: [[01_Statements/02_Outer_Formation/026_S-DF-identity-recognition-structure]]; [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]
- Successors: [[01_Statements/Definition/S-DF-elm-ec-identity]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

