# HEADERS — Kernel v0.2.0

Headers gate meta-change. Kernel includes:
• Collapse-to-Classical
• Loop Score with EMA
• Hysteresis with Cooldown

Extensions (harm/refuse/multi/memory/debt) are quarantined as HYP stubs until promoted.

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K3.Headers.Collapse@v0.2 — Collapse-to-Classical

Intent
Freeze topology edits when the current quotient is sufficiently stable; unfreeze on repeated violations.

Config (defaults)
• window W = 200 samples
• entropy threshold H(y | class) ≤ 0.10 bits
• relative variance threshold Var/Mean ≤ 0.05
• unfreeze after 2 consecutive threshold violations

Mechanics
Maintain a moving window of class assignments.
Compute: (a) entropy over the class histogram (bits);
(b) relative variance of counts.

Rule
If both thresholds hold ⇒ frozen (no merges/splits).
Else record a violation; when frozen, two consecutive violations unfreeze.

Code
core/headers/collapse.py.

Logging
At each update, record (frozen, entropy_bits, var_rel).

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K3.Headers.LoopEMA@v0.2 — Loop Score & EMA

Intent
Track loopiness or other exploration pressure via a normalized score s_t ∈ [0,1].

EMA
EMA_t = β * EMA_{t−1} + (1−β) * s_t, with β ∈ (0,1); default β = 0.9.
Effective memory ≈ 1 / (1−β).

Normalization
The producer of s_t must output in [0,1].
In the Kernel toy fixture we synthesize s_t; in real loops use a min-mean cycle score normalized to [0,1].

Code
Produced by experiment runner or loops module; consumed by HysteresisFlip.

––––––––––––––––––––––––––––––––––––––––

SpecCard CO.K3.Headers.Hysteresis@v0.2 — Flip Gate with Cooldown

Intent
Avoid flip-flop thrash between modes (e.g., explore/exploit).

Thresholds
θ_on = 0.25, θ_off = 0.15 (dead-band). Cooldown C = 10 steps.

Rule
Mode 0 → 1 if EMA ≥ θ_on.
Mode 1 → 0 if EMA ≤ θ_off.
After any flip, enforce cooldown for C steps (no further flips).

Anti-Oscillation Lemma
Over any horizon T, flips ≤ floor(T / C) (by cooldown).
Hysteresis dead-band prevents chattering near the boundary.

Code
core/headers/meta_flip.py.

Logging
Record ema, mode, cooldown, and cumulative flip_count.

––––––––––––––––––––––––––––––––––––––––

Optional: Density Header (Policy)
A simple dominance guard (e.g., majority ≥ 0.60) may delay widening/deepening.
This is policy, not contract, in Kernel v0.2.0.

––––––––––––––––––––––––––––––––––––––––

Extension Stubs (HYP — not Kernel)

Promotion criteria for each HYP: spec card, measurable proxies, unit tests, invariance pass, one fixture run with ledger.

HYP: CO.E.Headers.Harm@v0.1-HYP — Harm-Legitimated Edits
Idea
Allow spawn/merge/split/freeze iff expected harm reduction across channels
(epistemic, social, operational) minus option-loss exceeds θ_L.
Status
Draft only; estimators and thresholds pending.

HYP: CO.E.Headers.Refuse@v0.1-HYP — Refusal as Action
Idea
Refuse or downgrade when complying increases expected epistemic harm beyond θ_ref.
Status
Draft only; proxy choices (contradiction density, novelty) and tests pending.

HYP: CO.E.Headers.Multi@v0.1-HYP — Multi-Agent Consensus/Override
Idea
Reputational weighted consensus; veto on high harm; detect fluency-pressure
(style-similarity up, semantic gain down).
Status
Draft only; reputation metrics and tests pending.

HYP: CO.E.Memory.Strata+Debt@v0.1-HYP — Memory Strata and Instability Debt
Idea
Volatile → Motif → Invariant promotion/demotion with instability-debt when edits are deferred;
force Σ when debt high unless vetoed by harm.
Status
Draft only; promotion criteria and debt update require tests.

Provenance Guard: CO.K3.Headers.Sim@v0.1
Persona simulations are non-authoritative; any insight sourced from a sim must pass artifacts before promotion.

––––––––––––––––––––––––––––––––––––––––

Implementation Map (Traceability)
• Collapse: core/headers/collapse.py
• EMA/Hysteresis: core/headers/meta_flip.py
• Quotient closure: core/quotient/equivalence.py (witness logs)
• Lift with witness chaining: core/quotient/infimum_lift.py
• Invariance harness: evaluation/invariance_test.py
• Toy runner: experiments/runners/renewal_runner.py
