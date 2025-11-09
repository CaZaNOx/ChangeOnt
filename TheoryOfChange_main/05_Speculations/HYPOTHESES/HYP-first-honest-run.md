---
id: hyp.first-honest-run
title: HYP — First honest run for CO instrumentation
type: HYP
concepts: ["[[02_Concepts/C-benchmarks-audit]]", "[[02_Concepts/C-change-fitness]]"]
parents: []
successors: []
symbols_used: []
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_15_Spiral7.md:418-446
flags: []
tags: [speculation, experimentation, "type/HYP"]
---
# HYP — First honest run for CO instrumentation

Run `toy_ren_haq_vs_fsm` (or an equivalent CO-vs-classical benchmark) with fixed seeds, budget tables covering params/FLOPs/precision/memory/runtime, JSONL logs containing the standard metrics (AUReg, FDR_windowed, slope_window, loop_score, collapse header stats), and associated plots derived strictly from those logs. Publish the config/environment hash, commit, and migration ledger. This test validates that the claimed invariants and headroom are not paper propositions and sets a genuine baseline for future comparisons.
