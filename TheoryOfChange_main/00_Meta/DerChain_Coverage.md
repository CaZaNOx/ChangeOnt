---
title: DerChain Coverage Crosswalk — FND/LOG/MTH/PRM → Statements/Concepts/Graph
tags: [meta, coverage]
status: evolving
---
# DerChain Coverage Crosswalk
Mapping of key DerChain sections to formal statements, concepts, and graph node ids. Mark “pending” where not yet added.

- FND 0.0 Immediate Datum → [[01_Statements/FoundationalTruth/S-FT-immediate-datum]] (if present), graph: stmt.immediate-datum
- FND 1.0 Change Cannot Begin → [[01_Statements/Derivation/S-DR-change-cannot-begin]], graph: stmt.change-cannot-begin
- FND 2.x Continuity → [[01_Statements/FoundationalTruth/...]]; graph: stmt.continuity-noncessation
- FND 7–15 Identity/Similarity/SE → [[01_Statements/Definition/S-DF-identity-through-change]], [[01_Statements/Definition/S-DF-similarity-operator]], [[01_Statements/Definition/S-DF-stabilization-energy]]; graph: stmt.identity-through-change, stmt.similarity-operator, stmt.stabilization-energy
- FND 16–23 Subject/Self‑model → [[01_Statements/Definition/S-DF-subject]], [[01_Statements/Definition/S-DF-self-model-evolution]]; concept: [[02_Concepts/C-subject-awareness-experience]]; graph: stmt.subject-definition, stmt.self-model-evolution
- FND 24 Consciousness Loop → [[01_Statements/Definition/S-DF-consciousness-loop]]; concept: [[02_Concepts/C-subject-awareness-experience]]; graph: stmt.consciousness-loop
- FND 25 Inter‑Subject Gauge → [[01_Statements/Definition/S-DF-intersubject-gauge]]; concept: [[02_Concepts/C-subject-awareness-experience]]; graph: stmt.intersubject-gauge (id within statement file)
- FND 26 Gödel Limits → [[01_Statements/Definition/S-DF-godel-limits-self-containment]], [[01_Statements/Definition/S-DF-godel-hole-pointer]]; concept: [[02_Concepts/C-godel-holes]]; graph: stmt.godel-limits-self-containment, stmt.godel-hole-pointer
- FND 27 Breath Field → [[01_Statements/Definition/S-DF-breath-field-global-integrator]]; concept: [[02_Concepts/C-ontology-of-change]]; graph: stmt.breath-field-global-integrator
- LOG 1–2 Co‑logic/Quantale → [[01_Statements/Definition/S-DF-quantale-logic]], [[01_Statements/Derivation/S-DR-quantale-evidence-composition]]; concept: [[02_Concepts/C-math-structures]]; graph: stmt.quantale-logic, stmt.quantale-evidence-composition
- PRM 1 Bend → [[01_Statements/Definition/S-DF-prm-bend-metric]]; graph: stmt.prm-bend-metric
- PRM 9 Variable Birth → [[01_Statements/Definition/S-DF-prm-variable-birth]]; graph: stmt.prm-variable-birth
- PRM 12 Closure/Quotient → [[01_Statements/Definition/S-DF-prm-closure-quotient]]; graph: stmt.prm-closure-quotient
- PRM 14 Depth/Breadth Flip → [[01_Statements/Definition/S-DF-prm-depth-breadth-flip]]; graph: stmt.prm-depth-breadth-flip

Pending (samples):
- Any remaining FND sections not referenced above (please flag via validator/report).
- Additional LOG/MTH examples and proofs (optional) beyond concise forms.

How to extend
- Add missing statement files under `01_Statements`.
- Append concept canonical lists with those statements.
- Insert nodes/edges into `03_Derivation/graph.yaml`.
- Run: `python3 tools/update_backlinks.py` then `python3 tools/validate_toc_main.py`.

