# HEADERS — Collapse, Density, Meta-Flip, Complex Turn

## Collapse-to-classical

- Compute class-conditional entropy `H(y|class)` and variance ratio of perceived costs over W=200.
- **Collapse** if `H ≤ 0.10 bits` and `var ≤ 5%` for the full window; **freeze** gauge warping and flips; **un-collapse** when either bound is violated twice consecutively.
- Purpose: recognize stabilized regimes; use cheap solver while continuing to monitor.

## Density header

- Schedules exploration mode using **breadth** vs **depth** measured on Q.
- **Safety clause**: require agreement between revisitation and mean-return-time depth proxies within 10%; otherwise, no switch.

## Meta-flip (depth↔breadth)

- See SPEC: EMA, hysteresis, cooldown, flip budget.

## Complex turn (smooth rotation)

- Smoothly rotate scheduling weights on the breadth–depth plane using bounded momentum to avoid thrash.

**Note:** Headers *schedule*; they never alter δ or topology.
