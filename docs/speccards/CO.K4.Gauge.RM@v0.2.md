# SpecCard — CO.K4.Gauge.RM @ v0.2.0

**Scope.** Robbins–Monro gauge with leak; no topology edits here.

## Update
g_{t+1}(x) = clip_{[0,1]}( g_t(x) + α_t( λ·PE_t(x) − β·EU_t(x) ) − ρ g_t(x) ),  
with α_t = (t + t0)^{−0.6}, t0=50; ρ=1e−3; λ,β ∈ [0,1].

## Tests required
- test_gauge: boundedness; convergence on stationary signals; no effect on topology.
