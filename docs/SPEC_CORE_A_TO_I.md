# SPEC — Core mechanisms (a–i)

This file freezes constants, formulas, and falsifiers. No oracle access; no topology edits.

## (a) HAQ / Gauge

- **Gauge update (RM):** `G_{t+1}(u) = clip(G_t(u) + α_t(λ·PE_t(u) − β·EU_t(u) − ρ·G_t(u)))`
- `α_t=(t+50)^−0.6`, `λ=1.0`, `β=0.8`, `ρ=0.001`.
- **Perceived edge cost:** `c_G(u→v)=max(0, δ(u→v) − ½(G(u)+G(v)))`.
- **Loop score:** `s = (C_leave − C_stay)/( |C_leave|+|C_stay|+1e−6 )`.
- **Flip hysteresis:** θ_on=0.25, θ_off=0.15, cooldown=10.
- **MC debt:** horizon H=40; paired n=8; require ΔReg ≥ 0.05.

**Falsifier:** On renewal/Counting-Gate family, phase-flip sharpness ≥ 0.85, FDR_windowed ≤ 0.20, AUReg ≥ 0.06 vs matched FSM.

## (b) Variable spawn (MDL/BIC)

- Every m=20 steps, compute surprisal z-score and ΔBIC on window W=200.
- **Spawn iff** `z ≥ 2.0` and `ΔBIC ≤ −10` and **post-spawn AUReg** improves ≥0.05.
- Spawn adds a **latent tag** in predictive head only (no topology edits).
- **Reap** if usage <0.05 across 3 renewals and age ≥100 steps.

## (c) Identity / Compressibility κ

- Build minimal deterministic automaton compatible with observed class-token traces under τ (PTA→empirical bisimulation).
- `κ = 1 − |A_min|/|A_raw|`. Success if Δκ ≥ 0.10 without AUReg loss.

## (d) Edge-of-chaos controller

- Diversity `D = 1 − max_class_freq` over last 200 steps; target band [0.25, 0.35].
- Control law: τ_merge ← τ_merge + k_p·(D* − D) + jitter σ=0.02 (k_p=0.5).

## (e) Attention as potential

- Already embedded via perceived cost `c_G`, symmetrically subtracting ½ gauge at endpoints.

## (f) LLN on quotients

- Declare LLN-stable when `Jaccard(Q_{t−W},Q_t) ≤ 0.10` for 3 consecutive windows and ≥50 visits/class.

## (g) Density header

- Breadth `b` = normalized out-degree; Depth `d` = 1 − revisitation ratio; both measured on Q only.
- **Agreement rule:** require a secondary depth proxy (mean return time) to agree within 10% before switching modes.
- Mode: breadth if `b≥0.60` and `b≥1.5×d`; depth if `d≥0.60` and `d≥1.5×b`; else mix.

## (h) Depth↔Breadth meta-flip

- Δ = EMA(b−d), β=0.9. Trigger if |Δ|≥0.20; min-hold 15; hysteresis 0.10; cooldown 20; ≤1 flip/50 steps.

## (i) Complex turn

- Maintain (z_re, z_im); update with η=0.25, momentum 0.80; clip |z|≤1.
- Choose φ ∈ {0, π/2, π, 3π/2} minimizing short-horizon regret (H=20).

**All constants frozen**; unlisted degrees of freedom are considered **forbidden** unless preregistered.

# CO Core (a–i) — Frozen Spec (v1)

Each mechanism is tied to the chain `ID → eventlets → paths → δ → bends(τ) → equivalence → quotient Q → gauge G → decision`. No oracles; topology invariant.

## (a) HAQ / gauge

- **Robbins–Monro**: `α_t=(t+50)^(-0.6)`, `λ=1.0`, `β=0.8`, leak `ρ=0.001`.
    
- **Perceived cost**: `c_G(u→v)=max(0, δ_Q(u→v) − ½(G(u)+G(v)))`.
    
- **Loop score**: `(C_leave − C_stay) / (|C_leave|+|C_stay|+ε)`, EMA γ=0.90.
    
- **Flip logic**: θ_on=0.25, θ_off=0.15, cooldown=10; MC-debt: horizon 40, `n=8`, paired RNG, require `ΔReg≥0.05`.
    

## (b) Variable spawning (MDL/BIC)

- **Spawn** if z-score surprisal ≥ 2.0 and `ΔBIC ≤ −10` on last `W=200` obs; every `m=20` steps.
    
- Spawn adds **latent tag** to the predictive head only (no topology edit).
    
- **Reap** if usage < 0.05 for 3 renewals and age ≥ 100 steps.
    

## (c) Identity / compressibility κ

- Build minimal DFA over class-token traces (empirical PTA → tolerant merges).
    
- Define `κ = 1 − |states_min| / |states_raw|`. Diagnostic-only. Flag success if `Δκ ≥ 0.10` without AUReg drop.
    

## (d) Edge-of-chaos control

- Diversity `D = 1 − max_class_freq` over W=200. Target band [0.25, 0.35].
    
- Control `τ_merge ← τ_merge + k_p(D* − D) + jitter`, `k_p=0.5`, jitter σ=0.02.
    

## (e) Attention as generalized potential

- Already captured via `c_G`; ablation sets `G≡0`.
    

## (f) LLN on quotients

- Drift guard: `1 − Jaccard(E_Q(t−W),E_Q(t)) ≤ 0.10` with W=200.
    
- Sample floor ≥ 50/class before declaring convergence.
    

## (g) Density-of-change header

- Breadth `b_t` = normalized out-degree; Depth `d_t` = 1 − revisitation rate. Both computed on `Q`.
    
- Activate breadth-biased schedule if `b ≥ 0.60` and `b ≥ 1.5× d`. Depth-biased if symmetric condition holds; else mix.
    
- **Safety**: require a second depth proxy (loop occupancy) to agree within 0.1 before switching.
    

## (h) Depth↔Breadth meta-flip

- EMA `Δ_t = EMA(b_t − d_t)` with β=0.9; trigger if `|Δ| ≥ 0.20`, min-hold 15, hysteresis 0.10, cooldown 20, max 1 flip per 50 steps.
    

## (i) Complex turn

- Maintain steering vector `z` with `z ← μ z + η \* dir`, `μ=0.80`, `η=0.25`; clip `|z| ≤ 1`.
    
- Discrete headings `φ ∈ {0, π/2, π, 3π/2}`, choose by short-horizon regret (H=20); ties → 0.
    

## Headers (collapse, game/instance/local)

- **Collapse**: H(y|class) ≤ 0.10 bits & var ≤ 5% over W=200 → freeze quotient & warp; auto un-freeze on breach (twice consecutive).
    
- **Game/instance/local**: if reward-rate CI width ≤ 10% over last 300 steps, reduce exploration by 0.1 absolute; else normal schedule.
    
