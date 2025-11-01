# EVALUATION — Kernel v0.2.0


- Regret is pseudo-regret computed from known arm means (not sample means). This isolates algorithmic behavior; it is standard for synthetic bandit fixtures.
- The “UCB growth test” asserts R(10k)/R(5k) ≈ log(10k)/log(5k) ±10%.


Purpose
Define name-free metrics, invariance checks, and compute ledger fields used to evaluate CO.

Core Metrics (name-free)
• AUReg (Area Under Regret): lower is better; computed over episodes/windows.
• FDR_windowed (False Discovery Rate within window): lower is better.
• Slope (trend) via robust Theil–Sen on per-window regret.

ID-Permutation Invariance Procedure
Goal: verify metrics do not depend on class IDs (names).
Procedure
1) Run an experiment and save metrics.jsonl.
2) Apply a random permutation π to class IDs in the saved records (do not rerun the model).
3) Recompute metrics on the permuted records.
4) Report absolute deltas; assert max delta ≤ ε (e.g., 1e−9 for deterministic fixtures).
Report Schema (JSON)
    {
      "metric": "AUReg",
      "delta": 2.1e-10,
      "threshold": 1e-9,
      "pass": true
    }
Tooling
evaluation/invariance_test.py provides a minimal harness (dummy AUReg for the toy);
replace with evaluation/metrics functions as they mature.

Compute Ledger (accuracy-per-compute discipline)
For each run log:
• flops_per_step (approximate),
• memory_bits,
• precision (e.g., 32),
• context (tokens or steps),
• edit_costs (if available),
• accuracy_per_compute summary (optional downstream aggregation).

Outputs
• metrics.jsonl — per-step or per-episode metrics.
• budget.csv — per-step compute ledger rows.
• merge_witness.jsonl — deterministic closure audit trail (from quotient merge pass).
