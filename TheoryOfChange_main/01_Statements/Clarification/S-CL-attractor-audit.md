---
id: stmt.cl-attractor-audit
type: CL
title: Detecting attractor entry requires empirical state logging and recurrence checks
dependencies: ["[[01_Statements/Clarification/S-CL-meta-audit-guardrails]]", "[[01_Statements/Clarification/S-CL-meta-shape-prediction]]"]
parents: []
successors: []
concepts: ["[[02_Concepts/C-ontology-of-change]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:3571-3668
flags: []
tags: [detection, audit, "type/CL"]
---
# Detecting attractor entry requires empirical state logging and recurrence checks

Minimal-rule systems lack general invariants, so you must log every state (or hash) as the dynamics unfold, check for exact or approximate recurrence, and interpret bounded/patterned repetition as attractor entry. Diverging trajectories should keep producing novel states; reuse sliding windows, equivalence classes, or toleranced checks when exact comparisons are impossible. Only in rare systems can analytic invariants prove attraction; in general, only long-term empirical audit and sampling of many initial conditions reveal basins of attraction. This is the structured procedure AI_13 lays out in the later attractor discussion (lines 3571‑3668).

Record attractor hypotheses, divergence detections, and basins in the same ledger so future agents know which regions have been audited and which remain open.






























<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->



























































<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Dependencies: [[01_Statements/Clarification/S-CL-meta-audit-guardrails]]; [[01_Statements/Clarification/S-CL-meta-shape-prediction]]
<!-- END:AUTOGEN:RELATIONSHIPS -->





























