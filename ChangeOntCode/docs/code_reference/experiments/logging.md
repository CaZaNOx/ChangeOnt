# docs/code_reference/experiments/logging.md

# Logging

## Purpose

The logging layer writes run-level metrics and artifact-side metadata needed for later analysis.

---

## Why it exists

The project needs:
- inspectable runs,
- reproducible metrics,
- budget comparisons,
- and enough telemetry to understand what happened.

---

## Main responsibilities

The logging layer should support:
- writing metrics lines
- writing budget data
- writing manifests/status
- supporting plot generation from logged data

---

## Required run artifacts

**Binding**

Every successful run must produce:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

---

## Metric semantics

**Binding**

Metrics should be:
- family-relevant,
- honest,
- and sufficiently structured for mode/family/suite aggregation.

Examples:
- bandit regret or equivalent
- maze episode/return/path-like metrics
- renewal cumulative reward or equivalent
- CO diagnostic lines where appropriate

---

## Budget semantics

**Binding**

Budget files must be standardized enough for meaningful comparison.

A family-specific budget file that uses incompatible column naming without normalization is a misalignment.

---

## Plot contract

**Binding**

Plot generation is required, not best-effort.

Plots should be family-appropriate where possible, not only generic fallback plots.

---

## Misalignment examples

This area is misaligned if:
- required run artifacts are missing,
- budget schema drifts by runner,
- plots are absent or semantically meaningless,
- or logging flags/configs exist but are not actually honored by runtime.