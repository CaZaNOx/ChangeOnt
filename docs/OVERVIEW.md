# ChangeOnt — Overview

**ChangeOnt** is a prereg-style, auditable implementation of the **Change Ontology (CO)** core.
CO treats **change** (not objects, time, or states) as primitive. From the *Immediate Datum* (ID),
we derive a pipeline of structures:

Immediate Datum (ID)
→ eventlets (minimal contrasts)
→ paths (compositions of eventlets)
→ bends with tolerance τ (bounded re-identification)
→ equivalence closure (R,S,T) on paths
→ quotient Q (classes of paths; edges are observed transitions)
→ gauge G (Robbins–Monro attention/potential)
→ decision logic (loop/flip/hysteresis/MC-debt)
↘ headers (collapse-to-classical; density; meta-flip; complex turn)

Classical models appear as a **stabilized special case** (a *collapse header*), not as axioms.

## What’s here

- **docs/**: philosophy (FND0), math (CO_MATH), logic (CO_LOGIC), formal spec (SPEC_CORE_A_TO_I),
  headers, guardrails (CO_STRICT_RULES), prereg, baselines, benchmarks, evaluation, roadmap.
- **core/** (Batch 3+): reference Python for gauge/quotients/loops/headers and agents.
- **benchmarks/** (Batch 4+): renewal/codebook, drifting bandit, grid maze.
- **experiments/**: configs & runners to produce JSONL logs and plots.
- **evaluation/**: AUReg, Theil–Sen slope, FDR-windowed, volatility, LLN-stability.

## CO-Strict guardrails (must hold everywhere)

- **No oracles**: the agent cannot read plant step indices, renewal flags, or hidden “k” counters.
- **No topology edits**: only costs and quotienting vary; the plant’s latent topology is never edited.
- **Two-time-scale learning**: Robbins–Monro (RM) gauge update slower than mixing.
- **Drift & sampling guards**: LLN only logged when Jaccard drift ≤ 0.10 and sample floor ≥ 50.
- **Budget parity**: match precision, FLOPs/step, params, context window, and *count quotient bookkeeping*.
- **Collapse header**: if entropy H ≤ 0.10 bits and variance ≤ 5% (W=200), freeze to classical.

## Falsifiability (killer tests)

Each mechanism has a crisp pass/fail gate: flip sharpness, LLN convergence, AUReg deltas, density header safety, etc. See **EVALUATION.md** and **SPEC_CORE_A_TO_I.md** for exact conditions.

CO motto: “Stability through change.” The ‘classical’ is the limit case when novelty freezes.