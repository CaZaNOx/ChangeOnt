---
id: stmt.eventlet
type: DF
aliases: ["FND_7.Eventlet"]
title: Eventlet — minimal discernible modulation
concepts: ["[[02_Concepts/C-recursive-truth]]", "[[02_Concepts/C-prior-pointer-reach]]"]
dependencies: ["[[01_Statements/Definition/S-DF-localreach-topology]]"]
parents: ["[[01_Statements/Definition/S-DF-localreach-topology]]"]
successors: ["[[01_Statements/Definition/S-DF-path-eventlet-chain]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:610
flags: []
tags: [layer/foundations, domain/logical, stable, "type/DF", "concept/recursive-truth", "concept/prior-pointer-reach"]
---
# Eventlet — minimal discernible modulation
## Claim (formal)
An eventlet is the smallest discernible change unit under current ε; paths compose from eventlets.

## Philosophical Translation (of formal claim)
At the resolution you currently have, an eventlet is the tiniest “this happened” you can pick out. Stitching these together yields recognizable streams of change.

## Philosophical Justification
- [[S-DF-localreach-topology]] provides neighborhoods of reachable points; discrimination within a neighborhood bottoms out at ε, defining the smallest discernible step.
- Minimal granularity is needed to count and compose paths; otherwise continuity collapses into an undifferentiated blur.

## Explanation (informal)
Eventlets are pixels of change. They are not absolute atoms; if ε tightens, smaller eventlets can be recognized. Paths and metrics downstream depend on this granularity choice.

## Derivation (Philosophical)
- From LocalReach and discrimination threshold ε, define the equivalence that no finer subdivision is noticeable; the equivalence class is one eventlet.

## Derivation (Formal/Logical/Mathematical)
```text
Given ε, eventlet e satisfies:
  ∄ partition {e1,e2}: e = e1 ⊕ e2 with Dist(e1,e2) > ε recognizable in LocalReach.
```

## Proofs/Corollaries References
- corollary: forms the generators for [[S-DF-path-eventlet-chain]].

## Clarifications / Further Context
- Eventlets depend on observer/model resolution; they can refine as ε shrinks.
- Use consistent ε when composing paths; otherwise path depth comparisons drift.

## Next Steps in Chain
- suggest: [[S-DF-path-eventlet-chain]]

## Tags
#type/DF #layer/foundations #domain/logical #concept/recursive-truth #concept/prior-pointer-reach #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-interaction-points-eventlets]]
- [[01_Statements/Definition/S-DF-localreach-topology]]
- [[01_Statements/Definition/S-DF-path-eventlet-chain]]
- [[01_Statements/Definition/S-DF-point-occurrence]]
- [[01_Statements/Definition/S-DF-prm-change-ops]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-recursive-truth]]; [[02_Concepts/C-prior-pointer-reach]]
- Parents: [[01_Statements/Definition/S-DF-localreach-topology]]
- Dependencies: [[01_Statements/Definition/S-DF-localreach-topology]]
- Successors: [[01_Statements/Definition/S-DF-path-eventlet-chain]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

