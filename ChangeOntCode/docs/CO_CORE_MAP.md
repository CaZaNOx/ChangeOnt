# CO Core Map (Elements ↔ Primitives ↔ Headers ↔ Combinators)

## Headers (fixed labels)
- CS (Classical Static): flat gauge, ε=0, math_policy=classical
- ID (Identity-First): fixed ε>0, stable gauge
- SSI (Self-Situated Inference): online gauge + ε via signals (loopiness/volatility)

## Elements (A–I)
A. HAQ (History-Adaptive Gauge)
  uses: P1 (bend metric), P2 (gauge), P3 (MDL), P7 (precision), P8 (loopiness)
  header inputs: ε, τ, gauge
  combinator: C_pipeline (first)
  outputs: {tau, eps, gauge_level}

B. GHVC (Gödel-hole & Variable Creation)
  uses: P3 (MDL), P9 (variable_birth legacy), P10 (change_ops_core), P13 (creative_option)
  header inputs: dyn_threshold (SSI)
  combinator: C_gate (opens when residual high)
  outputs: {births, splits}

C. Identity as Bend-Equivalence
  uses: P1, P12 (closure_quotient), P10 (⊕)
  header inputs: ε
  combinator: C_co_ops (closure)
  outputs: {eq_classes, id_hits}

D. Gauge-only Warp Stabilization
  uses: P2 (gauge), P11 (residuation) [for thresholds]
  header inputs: gauge α
  combinator: C_co_ops (warp)
  outputs: {stabilize_score}

E. Memory Compressibility → Robustness
  uses: P5 (temporal ops), P3 (MDL)
  header inputs: none required
  combinator: C_pipeline
  outputs: {lz, robustness_pred}

F. GIL Router (Header chooser)
  uses: P11 (residuation), P12 (quotient), P8 (loopiness)
  header inputs: CS/ID/SSI priors
  combinator: C_gate
  outputs: {route: classical|co}

G. Density / Precision Knob
  uses: P7 (precision), P6 (change-integral)
  header inputs: precision schedule
  combinator: C_math_policy
  outputs: {round_decimals}

H. Breadth–Depth Scheduler
  uses: P14 (depth↔breadth flip), P8 (loopiness)
  header inputs: loopiness threshold
  combinator: C_pipeline
  outputs: {flip_events, bd_ratio}

I. Change-Native Operators (⊕ merge, ⊗ compose)
  uses: P10 (change_ops_core), P1, P4 (re-ID), P12 (closure), P11 (residuation)
  header inputs: ε policy (fixed|mdl|ssi), k
  combinator: C_co_ops
  outputs: {motif_counts, comp_counts}

## Primitives (P1–P14)
- P1 bend metric 
- P2 gauge 
- P3 mdl 
- P4 reid_kernel 
- P5 temporal_ops 
- P6 change_ops 
- P7 precision 
- P8 loopiness 
- P9 variable_birth 
- P10 change_ops_core 
- P11 residuation 
- P12 closure_quotient 
- P13 creative_option_birth 
- P14 depth_breadth_flip 

## Combinators
- C_pipeline: linear order of elements (A→…→I)
- C_gate: route/mix classical↔CO based on header/router
- C_math_policy: pick classical vs CO algebra for a block
- C_co_ops: CO-specific algebra (min,+),(⊕,⊗)
- C_classic_ops: classical (+,×), standard logits/sigmoid

## Header influence summary
- CS: ε=0, math_policy=classical, router=classical
- ID: ε=const>0, math_policy=co, router=auto
- SSI: ε,τ,gauge from online signals (loopiness/volatility), router=adaptive

