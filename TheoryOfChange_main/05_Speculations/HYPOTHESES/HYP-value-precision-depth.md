---
id: hypothesis.value-precision-depth
title: Hypothesis — Values as (magnitude, precision, cost)
status: hypothesis
tags: [speculation, hypothesis, numbers, precision, cost]
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats/AI_21.md:189-205
links_core:
  - [[01_Statements/Definition/S-DF-spread-arithmetic]]
---
# Hypothesis — Values as (magnitude, precision, cost)

Claim (speculative)
- Numerical “values” should be modeled as tuples (mean, precision depth, compute/time cost). Precision is a resource choice; coarser depth can win when cost is penalized. Error budgets should be part of the value algebra, not tacked on.

Test sketch
- Compare computations under varying precision depths on tasks with finite budgets (e.g., iterative sums, change detection, forecasting). Score = accuracy + λ·cost. Expect non-trivial optima (not max precision) and different winners depending on drift/noise and time-to-value constraints.

Signals to watch
- Regimes where low precision plus correction beats high precision end-to-end (due to latency or cost).
- Sensitivity of downstream identities/decisions to precision depth; quantify stability bands.

Why it matters
- Grounds “value with error/compute attached” in CO spread arithmetic and makes precision a first-class control knob rather than an afterthought.
