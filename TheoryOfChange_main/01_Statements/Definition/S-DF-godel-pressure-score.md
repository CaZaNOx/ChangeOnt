---
id: stmt.df-godel-pressure-score
type: DF
title: Gödel pressure score measures self-model discrepancy and complexity
dependencies: []
parents: []
successors: []
concepts: ["[[02_Concepts/C-ontology-of-change]]", "[[02_Concepts/C-godel-holes]]"]
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:16487-16499
flags: []
tags: [metrics, definition, "type/DF"]
---
# Gödel pressure score measures self-model discrepancy and complexity

Define Gödel pressure as the normed difference between actual dynamics and the agent’s self-model, weighted by complexity:
```
R_t^{(Gödel)} = H(x_t) - M_θ_t(x_t)
G_t = g(‖R_t^{(Gödel)}‖, Comp(R_t))
```
High G indicates structural contradictions or blind spots where the self-model cannot keep up, signaling candidate holes, urgency surges, and risks of collapse. Use this score to monitor emergent failures and to trigger meta-adaptation.






<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-urgency-plasticity]]
<!-- END:AUTOGEN:REFERENCED_BY -->











<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-godel-holes]]
<!-- END:AUTOGEN:RELATIONSHIPS -->





