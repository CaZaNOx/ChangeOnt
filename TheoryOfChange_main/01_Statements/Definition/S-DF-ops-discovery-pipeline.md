---
id: stmt.df-ops-discovery-pipeline
type: DF
title: OPS discovery pipeline — invariant extraction + validation
concepts: ["[[02_Concepts/C-change-fitness]]", "[[02_Concepts/C-frame-operators]]"]
dependencies: ["[[01_Statements/Definition/S-DF-gauge-alignment-field]]", "[[01_Statements/Definition/S-DF-memory-trace-integration]]"]
parents: ["[[01_Statements/Definition/S-DF-gauge-alignment-field]]"]
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_19.md:329-382
flags: []
tags: [layer/operators, domain/operational, operations, invariants, stable, "type/DF", "concept/change-fitness", "concept/frame-operators"]
---
# OPS discovery pipeline — invariant extraction + validation
## Claim (formal)
Provide a repeatable pipeline to extract, test, and log invariants for a task by (1) normalizing gauge/breath, (2) fitting a task model, (3) stress‑testing invariants under ε/h sweeps and classical gate checks, and (4) auditing via ablations.

## Philosophical Translation (of formal claim)
To avoid smuggling classical assumptions, we explicitly discover and validate invariants, logging when they only hold in a classical slice versus in change‑native regimes.

## Philosophical Justification
- [[S-DF-gauge-alignment-field]]: invariants must respect gauge alignment; disabling/adapting gauge tests sensitivity.
- [[S-DF-memory-trace-integration]]: stable traces are needed to compare runs and detect spurious invariants.
- Declaring gates/ablations makes claims auditable and prevents hidden assumptions.

## Explanation (informal)
For each task we standardize, extract candidate invariants, stress‑test them, and record what holds where. The output is an OPS card with invariants, confidence, ablations, and a “classical slice” flag.

## Derivation (Operational Steps)
- Normalize logs (time, breath, gauge); temporarily freeze adaptive gauge to expose a classical candidate slice.
- Fit task model \(M_T\); extract invariants \(I_T\) (e.g., graph metrics, KL gaps, hazard tails).
- Sweep ε/h to ensure refinement and gauge invariance; reject brittle invariants.
- Classical gate: if holonomy ≈ 0 and performance ≈ classical baseline, mark invariants as objective; otherwise tag as change‑native.
- Ablate gauges/adaptive knobs; retain only invariants stable under ablation; log confidence bands.

## Clarifications / Further Context
- OPS cards must include slice flag, confidence intervals, ablation tables, and gauge settings.
- Designed to prevent unvetted classical assumptions entering CO derivations.

## Next Steps in Chain
- suggest: integrate OPS outputs into change-fitness scoring and router policies.

## Tags
#type/DF #layer/operators #domain/operational #operations #invariants #concept/change-fitness #concept/frame-operators #status/stable

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-symmetry-tie-breaking]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-change-fitness]]; [[02_Concepts/C-frame-operators]]
- Parents: [[01_Statements/Definition/S-DF-gauge-alignment-field]]
- Dependencies: [[01_Statements/Definition/S-DF-gauge-alignment-field]]; [[01_Statements/Definition/S-DF-memory-trace-integration]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

