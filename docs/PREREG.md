# PREREG — Pre-registration Contract

## Budgets & Seeds

- Precision: float32 everywhere.
- FLOPs/step and memory bits include quotient tables/gauges.
- Context window caps equalized across agents.
- Base seed 1729; per-episode seed = base + episode_index.

## Baselines

- FSMCounter (explicit counter up to k_cap=24).
- LSTM1/2 (hidden=64; eval-only, no training).
- TransformerLite (2× layers/heads; context cap 64; eval-only).

## Acceptance Bands (parity fixture)

Fixture: `A=6, L_win=8, p_ren=0.08, p_merge=0.25, p_split=0.15, p_noise=0.02, p_adv=0, T_max=600, k=12`.

- flips/episode: **2.0 ± 1.0**
- FDR_windowed (Δ=6): **≤ 0.25**
- slope_window (Theil–Sen): **≤ −0.010 ± 0.002**
- AUReg vs FSM: **≥ 0.06**

## Logging

- Per-step JSONL and per-episode JSONL with fixed schemas (see EVALUATION.md).
- Record class-cap hit-rates; cycle-search caps; header switches; collapse periods.

## Deviations

Any change to constants or guards requires prereg update and re-run of mis-spec stress tests.


# Preregistration: Renewal Codebook Toy (Rung-1)

## Hypotheses (mechanism-level)

- **(a) HAQ/gauge** yields sharper phase flips and lower regret than a matched FSM cadence on renewal/palimpsest streams without oracle signals.
    
- **(e) Attention-as-potential** (gauge warp) reduces time-to-stable loops vs. no-warp ablation.
    
- **(f) LLN-on-quotients** holds when drift guard + sample floor are satisfied (Jaccard ≤ 0.10 over W=200; visits ≥ 50).
    

## Environment (fixture)

- Alphabet `A=6`, window `L_win=8`, renewal `p_ren=0.08`, merge `p_merge=0.25`, split `p_split=0.15`, noise `p_noise=0.02`, adversary off, horizon `T_max=600`, `k=12`.
    
- Seeds: base `1729`, per-episode `base+ep`.
    

## Agents

- **FSMCounter**: cadence 12, cap 24 exits.
    
- **EnhancedHAQ**: θ_on=0.25, θ_off=0.15, cooldown=10, RM `(t+50)^(-0.6)`, leak 0.001, λ=1.0, β=0.8, EMA γ=0.90. Precision float32.
    

## Budgets

- Precision float32 everywhere.
    
- Count memory bits incl. quotient bookkeeping (for later rungs); FLOPs/step within ±10% when comparing like-for-like agents.
    

## Metrics

- **FDR_windowed(Δ=6)**: fraction of flips aligned with events within ±6 steps.
    
- **Theil–Sen slope_window(W=100)** on cumulative regret trace.
    
- **AUReg_window(W=100)** vs FSM baseline.
    

## Pass/Fail Gates

- HAQ: **flips/ep ≥ 1**, **FDR_windowed ≥ 0.5** on average, **AUReg_window ≥ 0.06** improvement vs FSM (same seeds).
    
- LLN: volatility (1−Jaccard) ≤ 0.10 for 3 consecutive windows with sample floor ≥ 50/class.
    
- Safety: collapse guard obeyed when `H≤0.10 bits & var≤5%` (if satisfied).
    

## Analysis Plan

1. Run 20 episodes per agent with fixed seeds.
    
2. Produce per-episode JSONL rows: `flips`, `FDR_windowed`, `slope_window`, `AUReg_window`.
    
3. Report **mean ± IQR** and the full table. No parameter tuning post-hoc.
    

## Deviations

- Any change to constants or windows must be preregistered (commit + reason). Post-hoc tuning invalidates parity claims for this rung.