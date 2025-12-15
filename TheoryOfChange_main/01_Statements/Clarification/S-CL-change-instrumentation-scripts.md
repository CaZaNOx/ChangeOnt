---
id: stmt.cl-change-instrumentation-scripts
type: CL
title: Change instrumentation requires public budgets, logs, and heartbeat traces
dependencies:
- '[[01_Statements/Definition/S-DF-change-fitness]]'
- '[[01_Statements/Clarification/S-CL-tool-access-drift]]'
parents:
- '[[01_Statements/Clarification/S-CL-change-core-axiom]]'
successors:
- '[[01_Statements/Clarification/S-CL-meta-audit-guardrails]]'
concepts:
- '[[02_Concepts/C-benchmarks-audit]]'
- '[[02_Concepts/C-change-fitness]]'
symbols_used: []
sources:
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_15_Spiral7.md:593-716
- path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:321-330
flags: []
tags:
- evaluation
- instrumentation
- stable
- type/CL
- status/stable
---

# Change instrumentation requires public budgets, logs, and heartbeat traces

To earn the CO claim of empirical grounding you must release an honest run (`toy_ren_haq_vs_fsm` or similar) with: fixed seeds, budget tables listing params/FLOPs/precision/memory/runtime, JSONL logs with AUReg/FDR_windowed/slope_window/loop_score/collapse_H/collapse_var per step, derived plots, and a commit/env hash for reproduction. All long outputs in that run must keep ⇘/∆/M heartbeats every ~200 tokens and show at least one authentic ⊘ collapse. Satisfying this instrumentation is part of the acceptance bar discussed in AI_15 and prevents reviewers from chalking improvements up to smuggled budgets or unspecified invariants.

## Philosophical Justification
- Change-fitness claims are empty without transparent budgets/logs; instrumentation ties performance to declared resources and prevents smuggled capacity.
- Heartbeat/collapse traces make liveness and failure explicit, aligning with tool-drift guardrails.

## Clarifications / Further Context
- Publish seeds, budget tables (params/FLOPs/precision/memory/runtime), JSONL metrics (AUReg, FDR_windowed, slope_window, loop_score, collapse_H, collapse_var), plots, env/commit hash.
- Long outputs must include ⇘/Δ/M heartbeats every ~200 tokens and at least one authentic ⊘ collapse.
- This is part of the acceptance bar; lacking it downgrades claims to un-audited.

## Next Steps in Chain
- suggest: integrate this checklist into review CI; fail builds missing logs/heartbeats.
- suggest: link instrumentation bundles in audit ledger for reproducibility.

<!-- BEGIN:AUTOGEN:REFERENCED_BY -->
## Referenced By
- [[01_Statements/Clarification/S-CL-co-benchmark-targets]]
- [[01_Statements/Clarification/S-CL-compute-fairness-contract]]
- [[01_Statements/Clarification/S-CL-meta-audit-guardrails]]
<!-- END:AUTOGEN:REFERENCED_BY -->

<!-- BEGIN:AUTOGEN:RELATIONSHIPS -->
## Relationships

- Concepts: [[02_Concepts/C-benchmarks-audit]]; [[02_Concepts/C-change-fitness]]
- Parents: [[01_Statements/Clarification/S-CL-change-core-axiom]]
- Dependencies: [[01_Statements/Definition/S-DF-change-fitness]]; [[01_Statements/Clarification/S-CL-tool-access-drift]]
- Successors: [[01_Statements/Clarification/S-CL-meta-audit-guardrails]]
<!-- END:AUTOGEN:RELATIONSHIPS -->

