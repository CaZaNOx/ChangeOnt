---
title: Adaptive precision (h) + complex change (i) experiments
status: draft
tags: [anchor, precision, complex-change]
sources:
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:48740-48774
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:48788-48823
  - path: TheoryOfChange/00_Meta/AI_RecursiveChats_slim/AI_13_Spiral_5_Hero.md:48849-48860
---
# Adaptive precision (h) + complex change (i) experiments

Complex axis (Δb + iΔd):
- Process: z_{t+1} = e^{iθ} z_t + μ + ε_t (trend + rotation + noise).
- Scalar AR(1) vs complex AR(1) (same order). Across 72 regimes (θ ∈ {0, .05, .2, .5}, σ ∈ {0.1,0.3,0.6}), complex had the lowest test MAE; reduces to scalar when θ≈0 (no penalty).

Precision economics (h):
- Quantize predictions with (δ_b, δ_d); cost ∝ 1/δ_b + 1/δ_d.
- Sweeping δ in [1e-4, 1] shows optimal finite precision (e.g., δ≈0.14) — finer wastes budget, coarser hurts accuracy.

Adaptive h+i pipeline (12 seeds, 4-regime series ~2.5k steps):
- AR1 MAE: 1.823 ± 0.091; Lin2 MAE: 1.468 ± 0.076.
- CO(h+i): MAE 1.457 ± 0.075 with ~60% less precision budget (2.47±0.08 digits vs 6 fixed).
- Regime-wise: CO ≤ Lin2 on drift/level-shift; ≈ on seasonal; slightly behind on chaotic.

Sharpened h+i (+a gauge) ablation:
- AR1 MAE ≈ 0.283; Lin2 ≈ 0.261; CO(h+i) ≈ 0.271; CO(h+i+a) ≈ 0.270.
- Flip detector via spectral lags; precision chosen by benefit-vs-digit cost; light gauge nudges breadth vs depth.

Takeaway: complex axis yields accuracy gains when quadrature structure exists and is safe when not; precision should be a governed resource, with measurable optima and budget savings.
