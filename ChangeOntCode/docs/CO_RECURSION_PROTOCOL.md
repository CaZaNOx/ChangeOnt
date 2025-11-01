# CO Recursion Protocol (how we evolve the spec safely)

When proposing a change or new mechanism:
1) **Map to the chain**: ID → eventlets → paths → δ → bends(τ) → equivalence → quotient Q → gauge → decision. Show the link.
2) **No oracles**: affirm none are introduced (list signals used).
3) **Equivalence & congruence**: prove merges respect τ-congruence; edges use infimum-lift.
4) **Two-time-scale**: show RM step size vs. mixing; add drift guard & sample floor.
5) **Anti-thrash**: hysteresis/cooldown bounds; a fallback that gives bounded regret if mis-specified.
6) **Falsifier shelf**: add at least one decisive pass/fail test with thresholds; preregister constants.
7) **Budget parity**: define fair matched baselines and account for quotient bookkeeping.
8) **Stress finitude knobs**: vary caps (0.5×, 2×) and show qualitative invariants persist.
