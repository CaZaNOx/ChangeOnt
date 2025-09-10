# KT Handbook — CO Kernel v0.2.0 (Quick Onboarding)

What You Need To Know
• Work on the quotient: detectability R_τ → closure ≈ → graph Q (name-free).
• Edits are gated: collapse and hysteresis; gauge adapts continuously.
• Invariance and witness logs are mandatory; accuracy-per-compute is the currency.

Install (example)
• Python 3.10+
• pip install -r requirements.txt
• pytest -q

Run the Toy Fixture
• python -m experiments.runners.renewal_runner
Outputs:
    metrics.jsonl
    budget.csv
    (merge_witness.jsonl appears when quotient closure is invoked)

Check Invariance
• python -m evaluation.invariance_test metrics.jsonl reports/invariance_summary.json
Verify:
    delta ≤ 1e−9 and pass = true (for deterministic toy)

Read Order (short)
1) docs/CO_MATH.md (R_τ, closure, lift with witness-consistency)
2) docs/HEADERS.md (collapse, EMA, hysteresis)
3) docs/CO_LOGIC.md (3-valued tables)
4) docs/EVALUATION.md (invariance, ledger)
5) docs/PREREG.md (constants)

Contribution Rules (Kernel Contract)
• No name-dependent metrics. Invariance must pass.
• All merges must emit witness logs.
• Kernel files K-1…K-5 require RFC for changes and two passing runs (ours + baseline).
• Extensions live under E-* until promoted (spec + tests + invariance + one run).

Contacts
• CHANGELOG.md for version history
• LABELS.md for legacy mapping
