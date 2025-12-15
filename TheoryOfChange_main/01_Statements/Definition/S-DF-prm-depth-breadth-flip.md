---
id: stmt.prm-depth-breadth-flip
type: DF
aliases: ["PRM_14.DepthBreadthFlip"]
title: Primitive — Depth/Breadth flip from loopiness and phase
concepts: ["[[02_Concepts/C-ontology-of-change]]", "[[02_Concepts/C-math-structures]]"]
dependencies: ["[[01_Statements/Definition/S-DF-breath-field-global-integrator]]", "[[01_Statements/Definition/S-DF-depth-reach]]"]
parents: ["[[01_Statements/Definition/S-DF-breath-field-global-integrator]]"]
successors: ["[[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/02_Foundations/DerChain.md:5710
flags: []
tags: [layer/operators, domain/operational, stable, primitive, search-policy, control, "type/DF", "concept/ontology-of-change", "concept/math-structures"]
---
# Primitive — Depth/Breadth flip from loopiness and phase
## Claim (formal)
Compute a policy p_breadth = f(loopiness, phase) that flips exploration/exploitation based on recurrence propensity and breath phase. High short‑cycle propensity and specific phases increase breadth; otherwise prioritize depth along stable trajectories.

## Philosophical Translation (of formal claim)
When the system is circling, widen the search; when it flows, go deeper.

## Philosophical Justification
- [[S-DF-breath-field-global-integrator]] coordinates validation rhythm; loopiness/phase signals come from it.
- [[S-DF-depth-reach]] provides the ordering to define “deeper” vs. “broader” moves.
- Adaptive flipping prevents stagnation in loops and prevents shallow dithering in tree-like areas.

## Clarifications / Further Context
- Couples to ELM‑EH (breadth/depth scheduling) and attention routing.
- Avoids lock‑in and collapse by syncing policy with global integrator dynamics (breath).

## Derivation (Formal/Logical/Mathematical)
```text
p_breadth := g(L, phase)
if p_breadth > θ: choose BFS-weighted expansion
else: choose DFS-weighted descent along minimal-depth paths
```

## Next Steps in Chain
- suggest: [[S-DF-elm-eh-breadth-depth]]

## Tags
#type/DF #layer/operators #domain/operational #primitive #search-policy #control #concept/ontology-of-change #concept/math-structures #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
- [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
- [[01_Statements/Definition/S-DF-loopiness]]
- [[01_Statements/Definition/S-DF-prm-loopiness]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-math-structures]]
- Parents: [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
- Dependencies: [[01_Statements/Definition/S-DF-breath-field-global-integrator]]; [[01_Statements/Definition/S-DF-depth-reach]]
- Successors: [[01_Statements/Definition/S-DF-elm-eh-breadth-depth]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

