---
title: Drift-head benchmark (AI_13 toy streams)
status: draft
tags: [anchor, drift, detection]
sources:
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:1
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:8
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:9
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:10
  - path: TheoryOfChange_main/00_Meta/Context/AI_13_leads_master.txt:11
---
# Drift-head benchmark (AI_13 toy streams)

Toy change-detection sweep (N=400 streams; true change at t=200) over `level_shift`, `season_appear`, `season_switch`, `drift`, `vol_spike`.

Detectors compared:
- PH (piecewise heuristic baseline)
- CO1 (identity-only, model switching)
- CO2 (CO1 + heads: drift, volatility, spectral)

Headline results (macro-F1): CO heads add +2–5 points under drift/shift with parity on day-zero. CO1 stays clean (low FPs) but misses slow drift/volatility; CO2 recovers those rows with small FP increase.

Notes
- Drift head: Kalman on (level, slope) + sequential probability ratio; alternative: rolling slope t-test.
- Stress test: rerun with extra stream families (piecewise trend, mixed season+drift) and multiple seeds; report delay/FP mean±CI.
- Takeaway: advantage comes from the combination of attention/gauge cues and dedicated heads; model-switching alone lags on slow tension changes.
