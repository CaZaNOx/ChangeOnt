# CO-Strict Rules (compliance invariants)

1) **No oracles.** Prohibit access to plant step index, lap counts, renewal flags, or “k-opportunity” signals. Any internal step in RM is observer time, not plant time.

2) **Topology invariance.** The agent never adds/removes nodes or edges in the plant. Gauge **warps costs only**. Quotient edges exist only if observed.

3) **Equivalence closure.** Identity decisions use τ-bend with reflexive/symmetric/transitive closure. Merges must pass τ-congruence and use **infimum-lift** edges.

4) **Two-time-scale + drift guard.** Robbins–Monro step sizes satisfy $\sum \alpha_t=\infty$, $\sum \alpha_t^2<\infty$; report Jaccard-volatility ≤0.10 and sample floor ≥50 before claiming LLN.

5) **Anti-thrash.** Hysteresis/cooldowns on flips; MC flip-debt with horizon H=40, n=8, ΔReg≥0.05.

6) **Spawn MDL.** Variable spawn only if ΔBIC≤−10 **and** AUReg gain ≥0.05; reap if posterior usage <0.05 over 3 renewals and t≥100 since spawn.

7) **Budget parity.** Match precision (float32), FLOPs/step, parameter count, memory bits (incl. quotient tables), and context window versus baselines.

8) **Logging.** Emit JSONL with per-step and per-episode schemas; include seeds, gates, and pass/fail per falsifier.

9) **Collapse guard.** Freeze to classical only if $H(y\mid [x])\le 0.10$ bits **and** var ratio ≤5% over W=200; auto un-freeze on breach.

10) **Capacity pressure.** If caps bind (class cap, cycle caps), log cap-hit rates; do not evict active attractors; raise “congruence-at-risk” flag and pause merges until pressure eases.
