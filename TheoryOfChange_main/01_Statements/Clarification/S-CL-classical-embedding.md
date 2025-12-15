---
id: stmt.cl-classical-embedding
type: CL
title: "Classical embedding lemma \u2014 CO config that replicates any classical baseline"
dependencies:
- '[[01_Statements/Definition/S-DF-identity-invariants]]'
- '[[01_Statements/Definition/S-DF-gauge-alignment-field]]'
parents:
- '[[01_Statements/Clarification/S-CL-change-core-axiom]]'
successors: []
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
symbols_used: []
sources:
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_15_Spiral7.md:2188-2218
flags: []
tags:
- logic
- collapse
- stable
- type/CL
- status/stable
---

# Classical embedding lemma — CO config that replicates any classical baseline

For any fixed classical baseline with budget B there exists a CO configuration (τ→0, A≡0, spread collapse, headers off, spawn/reap disabled, α=0, leak=0) that produces the same behavior within ε. This lets us treat classical methods as a subset of CO by proving the embedding lemma and ensures that separation claims must focus on CO’s extras (headers, gauges, loops). The embedding lemma is the first pillar of the separation narrative from AI_15.

## Philosophical Justification
- Embedding shows CO strictly generalizes classical models: set knobs to neutral values to recover classical behavior.
- Separation claims must then target CO features (gauges/Tx/spawn) rather than argue straw classical failures.

## Clarifications / Further Context
- Embedding requires explicit mapping of state/transition weights to CO fields (gauge alignment, identity invariants).
- Budget B and tolerance ε must be declared; otherwise “within ε” is vacuous.
- Use this lemma to set up A/B tests: classical vs CO with added features.

## Next Steps in Chain
- suggest: formal proof sketch referencing [[S-DF-gauge-alignment-field]].
- suggest: log benchmark cases where the embedding configuration is validated.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]
- Parents: [[01_Statements/Clarification/S-CL-change-core-axiom]]
- Dependencies: [[01_Statements/Definition/S-DF-identity-invariants]]; [[01_Statements/Definition/S-DF-gauge-alignment-field]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

