---
id: stmt.df-godel-pressure-score
type: DF
title: Gödel pressure score — self-model discrepancy and complexity
concepts: ["[[02_Concepts/C-ontology-of-change]]", "[[02_Concepts/C-godel-holes]]"]
dependencies: ["[[01_Statements/Definition/S-DF-self-model-evolution]]", "[[01_Statements/Definition/S-DF-godel-hole-pointer]]"]
parents: ["[[01_Statements/Definition/S-DF-self-model-evolution]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:16487-16499
flags: []
tags: [layer/validation, domain/diagnostics, stable, metrics, definition, "type/DF", "concept/ontology-of-change", "concept/godel-holes"]
---
# Gödel pressure score — self-model discrepancy and complexity

## Claim (formal)
Define Gödel pressure as the normed difference between actual dynamics and the agent’s self-model, weighted by complexity:
```text
R_t^{(Gödel)} = H(x_t) - M_{θ_t}(x_t)
G_t = g(‖R_t^{(Gödel)}‖, Comp(R_t))
```
High G indicates structural contradictions or blind spots where the self-model cannot keep up, signaling candidate holes, urgency surges, and risks of collapse.

## Philosophical Translation (of formal claim)
When what happens and what you think will happen diverge in complex ways, pressure builds that points to holes in your model.

## Clarifications / Further Context
- Use this score to monitor emergent failures and to trigger meta-adaptation or GH logging.
- Complexity term prevents overreacting to small/simple residuals.
- Parents/Deps tie to self-model evolution and GH marking.

## Tags
#type/DF #layer/validation #domain/diagnostics #concept/ontology-of-change #concept/godel-holes #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-ineffable-pressure]]
- [[01_Statements/Clarification/S-CL-urgency-plasticity]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-godel-holes]]
- Parents: [[01_Statements/Definition/S-DF-self-model-evolution]]
- Dependencies: [[01_Statements/Definition/S-DF-self-model-evolution]]; [[01_Statements/Definition/S-DF-godel-hole-pointer]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

