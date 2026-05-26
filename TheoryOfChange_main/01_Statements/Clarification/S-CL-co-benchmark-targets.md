---
id: stmt.cl-co-benchmark-targets
type: CL
title: Benchmarks, target margins, and drop-in CO mechanisms
dependencies:
- '[[01_Statements/Definition/S-DF-change-fitness]]'
- '[[01_Statements/Clarification/S-CL-change-instrumentation-scripts]]'
concepts:
- '[[02_Concepts/C-ontology-of-change]]'
- '[[02_Concepts/C-change-fitness]]'
parents:
- '[[01_Statements/Clarification/S-CL-change-instrumentation-scripts]]'
successors: []
symbols_used: []
sources:
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:39403-41574
flags: []
tags:
- benchmarks
- methodology
- stable
- type/CL
- status/stable
---

# Benchmarks, target margins, and drop-in CO mechanisms

AI_13 names concrete win conditions for the applied program: HAR drift (A1) should add +2–5 macro-F1 under shifts while matching day-zero accuracy; navigation (A2) should cut replans 10–20% and tighten arrival variance; rehab tutors (A3) should reduce steps-to-criterion 15–25%; retail/ops/weather (B1–B3) should drop MAPE or MTTR 10–30%; genomics and ASR (C1–C2) should gain 3–6 AUPRC or 3–5% WER under novelty. The experiments must freeze the plant, compare classical + SOTA vs. a CO variant, stress the regime where CO matters (drift, flip, novelty), and ablate the CO knob to prove the gain. Three drop-in mechanisms translate CO talk into code: (i) Gauge/HAQ = maintain a per-path score \(g_t\), threshold bend cost to rewrite equivalence classes without re-training the plant; (ii) Gödel-gap latent = instantiate new head variables only when clustered residuals persist; (iii) Bend-equivalence identity = merge contexts only when their future distributions agree (bounded JS divergence). These sketches turn “CO will win on drift” into testable engineering claims.

## Philosophical Justification
- Change-fitness needs concrete margins and ablations to avoid hand-waving; benchmarks tether claims to measurable gains.
- Drop-in mechanisms operationalize CO: gauges, gap-triggered latents, and bend-based identity merges.

## Clarifications / Further Context
- Freeze the plant; compare classical+SOTA vs CO variant in drift/flip/novelty regimes; ablate CO knob to isolate effect.
- Report target margins per domain (A1–C2) and publish instrumentation per [[S-CL-change-instrumentation-scripts]].
- Mechanisms: gauge/HAQ, Gödel-gap latents, bend-equivalence merges with bounded JS divergence.

## Next Steps in Chain
- suggest: log benchmark configs and CO ablations in audit ledger.
- suggest: tie each margin to a falsifier threshold for acceptance.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By

<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-ontology-of-change]]; [[02_Concepts/C-change-fitness]]
- Parents: [[01_Statements/Clarification/S-CL-change-instrumentation-scripts]]
- Dependencies: [[01_Statements/Definition/S-DF-change-fitness]]; [[01_Statements/Clarification/S-CL-change-instrumentation-scripts]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

