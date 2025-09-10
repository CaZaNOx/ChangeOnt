# FILE: evaluation/reports/report_md.md
# Experiment Report (Toy Renewal: HAQ vs FSM)

## Setup
- **Benchmark:** renewal_codebook
- **Episodes:** _(fill after run)_
- **Seed:** _(fill after run)_
- **Config:** see `experiments/configs/toy_ren_haq_vs_fsm.yaml`

## Summary
- **AUReg_window (HAQ vs FSM):** _(fill after run)_
- **Notes:** No oracles; float32; hysteresis+cooldown; collapse header (not enabled in toy).

## Per-episode
_(paste the Markdown table produced by `evaluation/reports/tables.py`)_ 

## Plots
- Rewards over time (HAQ) — `outputs/plot_rewards_haq.png`
- Rewards over time (FSM) — `outputs/plot_rewards_fsm.png`
- Flip–event alignment (HAQ) — `outputs/plot_align_haq.png`

## CO-Compliance Checklist (quick)
- No environment counters/renewals/leaks exposed ✅
- Budget parity (toy parity) ✅
- Two-time-scale RM gauge ✅
- Drift guard metrics available ✅

# Experiment Report (CO-core Renewal Toy)

This report is a simple placeholder. The Python helper renders the table and a small aggregate summary. Generated artifacts live under `outputs/...`.

**Sections**

- Setup: renewal fixture (see config)
    
- Agents: FSM baseline vs HAQ
    
- Metrics: flips, FDR_windowed(Δ), Theil–Sen slope, AUReg_window(W)
    
- Episodes table: inlined by the report builder
    
- Aggregates: mean ± IQR
    

_(Replace with a richer report later.)_

