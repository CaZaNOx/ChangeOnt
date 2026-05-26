---
id: stmt.cl-intersubject-calibration-protocol
type: CL
title: Intersubjective calibration protocol (bend-budget quotient)
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-subject-awareness-experience]]'
dependencies:
- '[[01_Statements/Definition/S-DF-intersubject-gauge]]'
- '[[01_Statements/Definition/S-DF-gauge-alignment-field]]'
parents: []
successors: []
symbols_used: []
sources:
- path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:14
- path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:17
flags: []
tags:
- stability
- rigor
- type/CL
- concept/ontology-of-change
- concept/subject-awareness-experience
- status/stable
---

# Intersubjective calibration protocol (bend-budget quotient)

## Claim (formal)
To construct a shared identity space, subjects must run an explicit calibration protocol: (1) align on a fixed update rule and resource budget for their gauges; (2) compute pairwise bend budgets for candidate identities; (3) take the quotient that minimizes total bend cost across subjects; (4) declare convergence only when the bend budget and gauge updates stay within pre-declared Lipschitz and information-bottleneck bounds for the required window.

## Philosophical Translation (of formal claim)
We agree on “what counts as the same thing” by jointly minimizing effort to map our experiences onto each other, under rules that keep our personal salience tweaks from becoming unfalsifiable.

## Checks / protocol sketch
- Shared rule: gauge update must respect a declared Lipschitz constant and compression target; no ad hoc per-subject tweaks after the protocol starts.
- Pairwise cost matrix: compute bend budgets between each subject’s candidates; solve for the quotient that minimizes total budget (e.g., assignment or clustering under the declared tolerance).
- Convergence test: only accept the shared quotient if the total bend budget and per-subject gauge deltas stay below thresholds for K observations; otherwise keep collecting evidence.
- Falsifiability: if a subject can arbitrarily reshape its gauge to force agreement without paying budget, reject the run; calibration must be auditable under the shared rules.

## Tags
#type/CL #layer/stability #domain/formal #concept/ontology-of-change #concept/subject-awareness-experience

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-subject-awareness-experience]]
- Dependencies: [[01_Statements/Definition/S-DF-intersubject-gauge]]; [[01_Statements/Definition/S-DF-gauge-alignment-field]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

