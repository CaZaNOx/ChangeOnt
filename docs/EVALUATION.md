# Evaluation: metrics & reporting

**Per-step JSONL**: time t, class, edges_out with perceived costs, loop score raw/EMA, mode, flip, gauge snapshot hash.

**Per-episode JSONL**: flips, FDR_windowed (Δ=6), AUReg_window vs baseline, Theil–Sen slope_window, LLN_stable flag, quot_vol_idx.

**Metrics**:
- AUReg_window: renewal-weighted area under cumulative regret improvement.
- Theil–Sen slope_window: robust slope of cumulative regret vs time.
- FDR_windowed (Δ): fraction of flips within ±Δ of event times.
- Volatility: 1 − Jaccard(Q_{t−W}, Q_t), W=200.
- LLN stability: volatility ≤ 0.10 for 3 windows and per-class visits ≥ 50.

**Budget parity**: report precision, FLOPs/step, params, memory bits (including quotient tables), context window.

**Plots**: (1) cumulative regret with flip markers, (2) volatility over time, (3) entropy/variance for collapse gate, (4) AUReg bar vs matched baselines.
