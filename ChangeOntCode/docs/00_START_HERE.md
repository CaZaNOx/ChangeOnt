# ChangeOnt (Code) — Start Here

ChangeOntCode is the runnable codebase for the ChangeOnt experiments (suite, runners, CO kernel, baselines, and outputs). These docs are strictly **code-only** and exist to tell you how to run the suite, understand the canonical runtime, follow binding contracts, pass QA, and extend safely without drifting semantics.

## Reading order (and purpose)
1) `01_RUN_AND_OUTPUTS.md` — exact commands, configs, and output layout
2) `02_ARCHITECTURE_RUNTIME.md` — canonical wiring and dataflow (what calls what)
3) `03_BINDING_SPEC.md` — binding contracts for adapters, masks, signals, and telemetry
4) `04_ACCEPTANCE_AND_QA.md` — QA gate and how to generate evidence
5) `05_DEV_GUIDE.md` — safe extension patterns and anti-drift rules

## Authority statement
These 6 pages are binding; `docs/annex/` is legacy/non-binding reference.

Canonical kernel spec: `docs/kernel_spec/00_INDEX.md`
