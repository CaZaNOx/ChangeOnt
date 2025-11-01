# SpecCard — CO.K2.Lift.Witness @ v0.2.0

**Scope.** Infimum-lift of edge costs to the quotient with **witness-consistent** paths/cycles.

## Definitions
- Perceived base cost: c(u→v) = max(0, δ(u→v) − ½(g_t(u)+g_t(v))).
- Lifted edge: c_Q([x]→[y]) := min_{u∈[x], v∈[y]} c(u→v), storing witnesses (u*,v*).
- Witness-consistent path: ([x_0]→…→[x_n]) with witnesses (u_i*, v_i*) such that v_i* = u_{i+1}* (or within ε_bend and congruence residual ≤ ε_cong). Cycle evaluation uses only witness-consistent chains.

## Properties (finite regime)
- Existence/attainment: minima attained over finite sets.
- Monotonicity: enlarging a class weakly decreases outgoing c_Q.
- Reach preservation: if a base path exists then a lifted witness-consistent path exists with Σ c_Q ≤ Σ c.

## Tests required
- test_lift: attainment & witness stored; monotonicity after merge; reach preservation; Frankenstein cycle rejected without consistency.

## Constants (prereg)
ε_bend = 0.05; ε_cong = 0.05; max_cycle_len = 32.
