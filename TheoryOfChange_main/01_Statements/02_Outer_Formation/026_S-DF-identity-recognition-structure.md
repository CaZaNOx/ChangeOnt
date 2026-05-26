---
id: stmt.identity-recognition-structure
type: DF
aliases:
- COT_5.IdentityRecognitionStructure
- S-DF-identity-recognition-structure
title: Identity-recognition structure — similarity, admissibility, and threshold in one ordered structure
concepts:
- '[[02_Concepts/C-identity-change]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]'
- '[[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator]]'
- '[[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]'
- '[[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]'
parents:
- '[[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]'
successors:
- '[[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]'
- '[[01_Statements/Definition/S-DF-prm-reid-kernel]]'
symbols_used: []
sources:
- path: chat/2026-04-01 clarification that identity-recognition structure should be split from invariant-content.
flags: []
tags:
- layer/foundations
- domain/ontological
- type/DF
- status/stable
- concept/identity
chain_status_band: derived-but-weaker
chain_status_note: This node isolates the recognition side of identity from the later question of what preserved content actually survives through change.
---
# Identity-recognition structure — similarity, admissibility, and threshold in one ordered structure
## Claim (formal)
Identity-recognition structure is the ordered relation among graded similarity, identity-admissibility, and any sharpened thresholding that governs how a bounded continuing line can be recognized through transformation.

## Philosophical Translation (of formal claim)
Before asking what exactly remains the same, we must first specify how continuity is recognized as identity-bearing at all. That recognition side has its own structure and should not be conflated with the preserved content later called invariant.

## Philosophical Justification
[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile]] yields what later continuation must answer to, [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]] introduces same-line continuity through change, [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator]] supplies graded retained-versus-altered comparison, [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]] yields the tolerance field within which identity remains eligible, and [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]] sharpens that field when stronger cuts are needed. Together they form the recognition side of identity. The preserved content itself should therefore be isolated into a later node.

## Explanation (informal)
This node answers: how is continuity recognized as one line? It does not yet answer: what content is preserved in that line?

## Derivation (Philosophical)
- Identity-through-change requires recognition under transformation.
- Similarity makes graded comparison possible.
- Identity-admissibility gives the weaker tolerance field.
- Threshold may sharpen that field when contexts need stronger collapse.
- Therefore there is an ordered recognition structure prior to invariant-content.

## Derivation (Formal/Logical/Mathematical)
```text
RecognitionStructure_id(P) = <Sim, A_id, θ?>
where θ? indicates optional sharpened thresholding over an already-defined admissibility field.
```

## Clarifications / Further Context
- Recognition/admission structure is not identical with invariant content.
- Threshold remains derivative from admissibility.
- This node prepares later ReID machinery without collapsing recognition and preserved content into one file.

## Next Steps in Chain
- identify what content remains preserved inside recognized admissible continuity;
- only then connect that preserved content to ReID kernels and later stabilization operators.

## Tags
#type/DF #layer/foundations #domain/ontological #concept/identity #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]
- [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]
- [[01_Statements/Definition/S-DF-prm-reid-kernel]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-identity-change]]
- Parents: [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]
- Dependencies: [[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]; [[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator]]; [[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]; [[01_Statements/02_Outer_Formation/025_S-DF-self-similarity-threshold]]
- Successors: [[01_Statements/02_Outer_Formation/027_S-DF-identity-invariants]]; [[01_Statements/Definition/S-DF-prm-reid-kernel]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

