# CO_STRICT_RULES — Guardrails & Compliance

1. **No oracles.** Agents never read: step indices, renewal flags, hidden counters, lap counts, or “opportunity markers.”
2. **No topology edits.** The plant’s latent topology is fixed. Quotienting & gauges change perceived costs only.
3. **Two-time-scale RM.** Gauge step size satisfies SA conditions; empirical stats change slower than learning rate.
4. **Drift guard.** LLN logging only when Jaccard ≤ 0.10 over W=200 and sample floor ≥ 50 per class.
5. **Budget parity.** Match precision, FLOPs/step, params, context window, *and* include quotient bookkeeping in memory/FLOPs.
6. **Collapse header.** Use entropy/variance guard; auto un-collapse on breach.
7. **Falsifiers.** Each mechanism has a pass/fail criterion; predefine acceptance bands; no retro-tuning.
8. **Report finitude knobs.** Caps (class cap 64, cycle caps, windows) must be logged with hit-rates and stress-tested (0.5×, 2×).
9. **Traceability.** Every spec item maps to code path → tests → metrics via `docs/EVALUATION.md` and `evaluation/reports/`.

# CO-Strict Rules (Guardrails)

These are the non-negotiables we enforce across code, analyses, and writeups.

1. **No oracles.** Agents never read plant internals (step index, renewal flags, lap counts, “k-opportunity” markers). All signals derive from the observation stream and learned structures only.
    
2. **Topology invariance.** The plant’s node/edge set is fixed. CO adapts by **quotienting** and **gauge-warping costs**, not by adding/removing plant edges.
    
3. **Equivalence & congruence.**
    
    - Identity arises via **bend-tolerance** `τ` and **equivalence closure** (reflexive, symmetric, transitive).
        
    - After merges, quotient edges use **infimum-lift** of perceived costs; **τ-congruence** must hold (class actions ≈ representative actions within τ).
        
4. **Two-time-scale learning.** Gauge updates follow Robbins–Monro with step sizes `α_t = (t+c)^{-p}` (`p∈(0.5,1)`), strictly **slower** than mixing. Include a **drift guard** (e.g., Jaccard ≤ 0.10 over a window) and a **sample floor** (≥ 50) before declaring LLN stability.
    
5. **Anti-thrash flips.** Mode switches (EXPLORE/EXPLOIT) use **hysteresis** (θ_on/θ_off) and **cooldowns**; MC-debt checks are bounded (horizon H, paired rollouts).
    
6. **MDL-grounded spawn.** Variable spawning allowed only under **ΔBIC ≤ −10** and observed performance gain (e.g., AUReg ≥ 0.05). Reap unused spawns (usage < 0.05 over 3 renewals, min life 100).
    
7. **Collapse-to-classical.** When **H(y|class) ≤ 0.10 bits** and **var ≤ 5%** (window W=200), freeze quotient and gauge warp; auto **un-collapse** when bounds break. “Classical” is a stabilized special case.
    
8. **Budget parity & audits.** Match precision, FLOPs/step, memory bits (incl. quotient tables), params, context window across baselines. Log seeds and counters; publish configs.
    
9. **Falsifiers first.** Each mechanism lists a decisive failure mode with a pre-specified pass/fail test (e.g., phase-flip sharpness, LLN convergence, bounded regret under mis-spec).
    
10. **Recursion protocol.** Every new definition cites its predecessors in the chain: Immediate Datum → eventlets → paths → bends/τ → equivalence → quotient → gauge-warped costs → decision. No “floating” primitives.
