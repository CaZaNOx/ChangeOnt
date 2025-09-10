# PREREG — Kernel v0.2.0 Constants

Purpose
Freeze operational constants for reproducibility and fair baselines.

Gauge (HAQ)
• alpha exponent (alpha0): 0.6
• t0 (burn-in offset): 50
• leak ρ: 1e−3
• clip range: [0, 1]
• lambda_pe: 1.0
• beta_eu: 1.0

Collapse Header
• window W: 200
• entropy_bits_thresh: 0.10
• var_rel_thresh: 0.05
• unfreeze_violations: 2

Flip (LoopEMA + Hysteresis)
• EMA beta: 0.9
• theta_on: 0.25
• theta_off: 0.15
• cooldown_steps: 10

Quotient Closure (example defaults)
• tau_merge (illustrative): 0.20
• padding weight w_pad: 0.25

Evaluation
• invariance epsilon: 1e−9 (deterministic fixtures)
• seeds: prefer fixed set {1729, 1737, 19937} for audits

Notes
Changing Kernel constants requires updating this file and the CHANGELOG.
Extensions must specify their own prereg blocks before promotion.
