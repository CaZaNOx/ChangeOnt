---
id: stmt.dimension-change
type: DF
aliases: ["FND_7.Dimension"]
title: Dimension — degrees of freedom under change
concepts: ["[[02_Concepts/C-dimension]]"]
dependencies: ["[[01_Statements/Definition/S-DF-reach-relation]]", "[[01_Statements/Definition/S-DF-localreach-topology]]"]
parents: ["[[01_Statements/Definition/S-DF-reach-relation]]"]
successors: ["[[01_Statements/Derivation/S-DR-dimension-variation]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/FND_7_Dimension.md:1
flags: []
tags: [layer/foundations, domain/formal, stable, "type/DF", "concept/dimension"]
---
# Dimension — degrees of freedom under change
## Claim (formal)
Dimension counts structurally independent directions in LocalReach; Tx may alter effective dimension by changing admissible transformations.

## Philosophical Translation (of formal claim)
“How many ways can it change” depends on the structure of reach and the frame; frames can change that number.

## Philosophical Justification
- [[S-DF-reach-relation]] and [[S-DF-localreach-topology]] define adjacency; independent directions correspond to independent generators of Reach within LocalReach.
- Transform operators (Tx) can constrain or expand admissible steps, changing the rank of the generator set; hence dimension is dynamic, not fixed a priori.
- Counting independent directions is necessary to reason about curvature, entropy, and SE allocation.

## Explanation (informal)
Dimension is not just “3D space” but “how many independent knobs can this system turn right now.” New knobs can appear when frames change; others can collapse under constraints.

## Derivation (Philosophical)
- Take LocalReach graph; compute minimal generator set of admissible moves under composition.
- Dimension := size of that set (or its span) relative to current frame.
- Tx that prune/introduce generators change dimension.

## Derivation (Formal/Logical/Mathematical)
```text
Let G be generators of Reach on LocalReach; dim := rank(span(G)).
Tx: G → G' ⇒ dim' = rank(span(G')).
```

## Proofs/Corollaries References
- corollary: informs [[S-DR-dimension-variation]] and curvature/entropy analyses.

## Clarifications / Further Context
- Dimension is local and frame-dependent; declare the frame and window when asserting dim values.
- Effective dimension can differ from ambient metric dimension if constraints reduce reachable directions.

## Next Steps in Chain
- suggest: [[S-DR-dimension-variation]]

## Tags
#type/DF #layer/foundations #domain/formal #concept/dimension #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-metric-space-emergent]]
- [[01_Statements/Derivation/S-DR-dimension-variation]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-dimension]]
- Parents: [[01_Statements/Definition/S-DF-reach-relation]]
- Dependencies: [[01_Statements/Definition/S-DF-reach-relation]]; [[01_Statements/Definition/S-DF-localreach-topology]]
- Successors: [[01_Statements/Derivation/S-DR-dimension-variation]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

