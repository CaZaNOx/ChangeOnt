---
id: stmt.df-loopiness
type: DF
title: Loopiness L — cycle evidence for scheduler gating
concepts: ["[[02_Concepts/C-spiral-recursion]]", "[[02_Concepts/C-ontology-of-change]]"]
dependencies: ["[[01_Statements/Definition/S-DF-breath-field-global-integrator]]", "[[01_Statements/Definition/S-DF-memory-trace-integration]]"]
parents: ["[[01_Statements/Definition/S-DF-breath-field-global-integrator]]"]
successors: ["[[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_19.md:296-297
flags: []
tags: [layer/validation, domain/operational, stable, metrics, scheduling, "type/DF", "concept/spiral-recursion", "concept/ontology-of-change"]
---
# Loopiness L — cycle evidence for scheduler gating

`L` tracks the density of cycles (Betti‑1 counts, return probabilities) in the working graph over recent breath cycles. High `L` signals loop-rich domains where exploring breadth-first keeps new modalities in view, while low `L` invites depth-first, exploitative passes. `L` feeds the Breadth–Depth scheduler ([BDSCHED]) so that the policy toggles between BFS/DFS regimes in sync with the latent topology.

## Philosophical Justification
- [[S-DF-breath-field-global-integrator]] coordinates validation cycles; loopiness quantifies when to emphasize breadth vs. depth.
- [[S-DF-memory-trace-integration]] supplies the trace data to count returns and loops; without it, L is unobservable.
- Adaptive scheduling prevents premature collapse in loop-rich domains and avoids dithering in tree-like domains.

## Explanation (informal)
L is a knob telling the scheduler “stay wide, there are many cycles” or “go deep, it’s tree-like.” It keeps exploration aligned with the actual topology instead of a fixed policy.

## Derivation (Formal/Logical/Mathematical)
```text
L := f(Betti_1(LocalReach_window), return_probabilities over breath window)
Use L to weight BFS vs. DFS in BDSCHED:
  w_BFS = g(L); w_DFS = 1 - g(L)
```

## Next Steps in Chain
- suggest: [[S-DF-prm-depth-breadth-flip]]

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-spiral-recursion]]; [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Definition/S-DF-breath-field-global-integrator]]
- Dependencies: [[01_Statements/Definition/S-DF-breath-field-global-integrator]]; [[01_Statements/Definition/S-DF-memory-trace-integration]]
- Successors: [[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

