# Outputs, Summaries, and Plots

This file documents the semantic meaning of outputs and the rules that make them trustworthy.

## 1. Principle

Outputs are part of the contract.

A file that exists but is semantically wrong does not count as a valid output.

## 2. Run outputs

Required run outputs:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

These are required artifacts.

## 3. Summary levels

### Mode
Aggregates all runs in one mode/environment.

### Family
Aggregates all completed modes in one family.

### Suite
Aggregates all completed families.

## 4. Plot requirement

Plots are required at:
- run level
- mode level
- family level
- suite level

Missing plots are a contract failure.

## 5. Semantic rules

### CO-only rule
CO-only summaries and plots must exclude STOA rows.

### STOA-vs-CO rule
STOA-vs-CO outputs must use compatible metric semantics across rows.

### Identity normalization rule
Agent identity normalization must be consistent across:
- run folders
- mode summaries
- family summaries
- suite summaries
- plot labels

### Label honesty rule
A plot or CSV label must correspond to what actually ran.

## 6. What must be documented for every summary output

Each summary output should make clear:
- what rows it uses
- what aggregation it performs
- what the resulting file means
- what would make it invalid

## 7. Failure/provenance outputs

**Recommended starting point**

Suites should also produce:
- failure summary outputs
- suite manifest/provenance
- config snapshots

These are strongly recommended and may become Binding if needed for diagnosis/reproducibility.

## 8. Current misalignment examples this file is meant to catch

This file should help detect:
- CO-only outputs that include STOA rows
- STOA-vs-CO files mixing incompatible metrics
- missing plots
- label drift across levels
- misleading suite outputs that appear valid but are not semantically correct