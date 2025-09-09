# ChangeOnt (CO): A Change-First Ontology for Learning & Control 

ChangeOnt is a research codebase and set of papers exploring **Change Ontology (CO)** — a first-principles framework that treats *change* (not static objects) as the primitive. From the **Immediate Datum** (what is minimally given to an observer), CO derives:

- **eventlets → paths → bends(τ) → equivalence closure → quotient graph Q → gauge-warped costs**
- Core mechanisms (a–i): HAQ, variable spawn (MDL), compressibility κ, edge-of-chaos control, attention-as-potential, LLN-on-quotients, density header, meta-flip, complex turn
- Headers that detect when the world is “effectively classical” and safely collapse to classical solvers

The repo aims to be **CO-strict** (no oracle signals; topology-invariance; matched budgets; falsifiable tests) and **reproducible** (frozen constants, seeds, and JSONL logs).

## Why CO?
Classical pipelines freeze “objects” then bolt on nonstationarity, probabilistic drift, or ad-hoc counters. CO inverts this: identity is **re-identification under bounded bends**; topology never changes, only **perceived costs** warp via a Robbins–Monro gauge. Classical behavior is a **stabilized limit case**.

## What’s here
- `docs/` — narrative (Immediate Datum), math/logic specs, CO-strict rules, headers, proofs, prereg & evaluation
- `core/` — CO math & logic primitives; quotient & gauge; loops/flip/debt; headers; compliance checks; agents
- `benchmarks/` — renewal/codebook, drifting bandit, grid-maze fixtures
- `experiments/` — configs, runners, logging, plots
- `evaluation/` — metrics & report templates
- `tests/` — unit & property tests for math and mechanisms

## Quick start (Python 3.10+)
1) Create and activate a venv:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1`
   - macOS/Linux: `python3 -m venv .venv; source .venv/bin/activate`

2) Install deps: `pip install -r requirements.txt`

3) Smoke test docs compile (math in GitHub renders with `$...$` and `$$...$$`).

4) First experiment (once code is populated):
python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml


## CO-strict guardrails (essentials)
- **No oracles**: agents never read plant step index, lap counters, or renewal flags.
- **Topology invariance**: gauge only warps costs; it never adds/removes edges.
- **Two-time-scale**: Robbins–Monro step sizes slower than mixing; drift-guard for LLN.
- **Budget parity**: compare against baselines with matched precision, FLOPs/step, params, memory, context.
- **Falsifiability**: each mechanism has pass/fail “killer tests” with thresholds.

## Status
We are finalizing theory docs (Immediate Datum → math → logic → proofs), then plugging in the experiment runners. See `docs/ROADMAP.md`.
