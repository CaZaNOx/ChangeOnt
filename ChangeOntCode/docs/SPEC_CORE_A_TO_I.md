# Core mechanisms (a–i) — frozen constants (spec)

(a) **HAQ**: Gauge update (RM), warped perceived cost, τ-congruence, infimum-lift, loop score, hysteresis (0.25/0.15), cooldown 10, MC flip-debt H=40, n=8, ΔReg≥0.05.

(b) **Variable spawn**: Trigger if z-surprisal ≥ 2.0 over W=200 and ΔBIC ≤ −10; must yield AUReg gain ≥ 0.05; reap if usage <0.05 across 3 renewals and life ≥ 100.

(c) **Compressibility κ**: Build minimal deterministic automaton from class-token traces consistent with τ & congruence; κ = 1 − |states|_reduced / |states|_raw (diagnostic-only).

(d) **Edge-of-chaos**: Diversity band [0.25, 0.35]; proportional control $u_{t+1} = u_t + 0.5\,(D^* - D_t)$ with jitter σ=0.02.

(e) **Attention as potential**: $c_G = \max(0, \delta - \tfrac{1}{2}(G(u)+G(v)))$.

(f) **LLN on Q**: Drift guard V ≤ 0.10 with W=200; sample floor ≥ 50; call convergence only under guard.

(g) **Density header**: thresholds as in `HEADERS.md`, with dual depth proxy agreement (return time or loop occupancy must agree within ε=0.05).

(h) **Meta-flip**: EMA β=0.9, |Δ|≥0.20, min-hold 15, hysteresis 0.10, cooldown 20, ≤1/50 steps.

(i) **Complex turn**: η=0.25, momentum 0.80, φ∈{0,π/2,π,3π/2}, |z|≤1.
