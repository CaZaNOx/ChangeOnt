# SpecCard — CO.K3.Headers.Operational @ v0.2.0

**Scope.** Collapse-to-classical; loop_score + EMA; hysteresis + cooldown.

## Definitions
- loop_score s_t = (C_leave − C_stay) / (|C_leave| + |C_stay| + 1e−6).
- EMA: s̄ ← β s̄ + (1−β) s_t.
- Flip gate: on if s̄ ≥ θ_on; off if s̄ ≤ θ_off; enforce cooldown C steps between flips.
- Collapse: freeze merges/edits when (i) H(y|class) ≤ 0.10 bits AND (ii) Var(c)/(|E[c]|+1e−6) ≤ 0.05 over window W_c=200; unfreeze after two consecutive violations.

## Guarantees
- Anti-oscillation: flips ≤ ⌊T/C⌋ by construction.
- Collapse supremacy: when frozen, flip/merge requests ignored.

## Tests required
- test_headers: dead-band behavior, cooldown bound, collapse freeze/unfreeze.
