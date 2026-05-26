---
title: Gap-spawn variable vs. simple and always-on baselines
status: draft
tags: [anchor, novelty, variable-spawn]
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:39511-39533
---
# Gap-spawn variable vs. simple and always-on baselines

Synthetic AR regime shift (shock at t=1500, T=3000; 200 trials):
- simple: always 1-lag linear (no new variable).
- always_on: always 2-lag (extra variable always active).
- co_gapspawn: 1-lag until dual-EMA change detector fires; then add 2nd lag.

MSE (pre | post | overall):
- simple: 0.652 | 0.957 | 0.807 (features=1.00; false spawn=0).
- always_on: 0.663 | 0.671 | 0.667 (features=2.00; false spawn=0).
- co_gapspawn: 0.652 | 0.697 | 0.675 (features=1.47; false spawn≈0.13).

Read: CO matches simple before the shock, nearly matches always_on after, and uses ~26–27% fewer active features on average. Trade-off between adaptation speed and false spawns is explicit via the detector thresholds.
