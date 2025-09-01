# EVALUATION — Metrics, Schemas, Falsifiers

## Core Metrics

- **AUReg_window**: per-window area-under-regret improvement vs baseline (higher is better).
- **Theil–Sen slope**: robust slope of cumulative regret vs time (more negative is better).
- **FDR_windowed (Δ)**: fraction of flips that align to an event within ±Δ steps.
- **Volatility**: `V = 1 − Jaccard(Q_{t−W}, Q_t)`.
- **LLN-stability**: stabilized when `V ≤ 0.10` for 3 windows and per-class visits ≥ 50.

## JSONL Schemas

**Per-step:**
{"ep":1,"t":123,"obs":3,"class":5,"G":0.41,"cost_stay":0.73,"cost_leave":1.12,
"loop_score":0.35,"flip":0,"spawn":0,"b":0.62,"d":0.28,"z_re":0.62,"z_im":0.28,
"header":"mixed","regret":0.004,"Q_hash":"f81d4fae"}


**Per-episode:**
{"ep":1,"flips":3,"FDR_windowed":0.17,"AUReg":0.083,"slope_window":-0.012,
"LLN_stable":true,"quot_vol_idx":0.08,"k":12,"adv":false,"seed":1730}

## Falsifiers (per mechanism)

- **(a)** Phase-flip sharpness ≥ 0.85; FDR ≤ 0.20; AUReg gain ≥ 0.06.
- **(b)** ΔBIC ≤ −10 **and** AUReg gain ≥ 0.05; else falsified.
- **(c)** Δκ ≥ 0.10 **without** AUReg loss.
- **(d)** Diversity within [0.25,0.35]; else falsified.
- **(e)** Warp reduces time-to-stable-loop ≥ 25% on CA/maze.
- **(f)** LLN must stabilize under guard; else falsified.
- **(g)** Header must not worsen AUReg by > 0.02 in classical regime.
- **(h)** Meta-flip reduces escape-time ≥ 30% w/ thrash ≤ 5%.
- **(i)** Complex turn beats flip-only by ≥ 0.03 AUReg on graded shifts.

# FILE: docs/EVALUATION.md
# Evaluation metrics (v1)

This repo uses small, CO-aligned metrics:

- **AUReg_window**: average per-window improvement of cumulative reward vs a baseline (non-negative).
- **Theil–Sen slope**: robust slope of (time, regret) pairs on a sliding window.
- **Flip–event alignment**: fraction of flips within ±Δ steps of event times logged by the *environment*, used purely for audit (no oracle used by the agent).
- **Volatility (Jaccard)**: 1 − Jaccard similarity between symbol sets in successive windows.
- **LLN stability**: volatility ≤ 0.10 for 3 consecutive windows and each symbol seen ≥ 50 times.

All metrics operate on **observed logs**; none feed into the agent during a run.


# Evaluation

We use the following **task-agnostic** metrics:

- **AUReg (renewal-weighted area under regret)** — compares agent vs baseline regret per window.
    
- **Theil–Sen slope** — robust trend of cumulative regret.
    
- **FDR-windowed (Δ=6)** — fraction of flips aligned to events within ±Δ steps.
    
- **Volatility index** — 1 − Jaccard on quotient snapshots across a window.
    
- **LLN stability** — declares stable when volatility ≤ 0.10 for 3 consecutive windows and per-class visits ≥ 50.
    

Each experiment run emits two JSONL logs:

- `*.steps.jsonl` — per-step records (time `t`, obs/action, reward, auxiliary metrics).
    
- `*.episodes.jsonl` — per-episode aggregates (return, flip counts, headline metrics).
    

See `experiments/run_experiment.py` for config fields and runner selection.
