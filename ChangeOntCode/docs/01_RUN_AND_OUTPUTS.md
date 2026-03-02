# Run and Outputs

This file describes how the project is supposed to be run and what outputs a correct run must produce.

This is a target-state document. If code behavior differs from this file, that difference is a misalignment unless explicitly documented as experimental or legacy.

## 1. Main entrypoints

The main execution entrypoints are expected to be:

- suite execution through `experiments/suite_cli.py`
- family-local execution through the family runners in `experiments/runners/`

A valid execution path should always be understandable as:

1. suite or runner config is loaded
2. family/mode/run jobs are determined
3. environment is constructed
4. STOA or CO path is constructed
5. select → act → feedback → update loop runs
6. required artifacts are written
7. summaries and plots are generated at the correct barrier points

## 2. Working-directory and path rule

**Binding**

Path resolution must be explicit and robust.

In particular:
- config paths must resolve deterministically
- CO manifest paths must not silently fail
- output roots must be explicit
- a user must not accidentally run STOA-only when CO was intended because of brittle path handling

The implementation may resolve paths relative to:
- the suite config location,
- or a clearly documented canonical root,
but this behavior must be explicit and reliable.

## 3. Required run artifacts

Every successful run must produce:

- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

A run missing any required artifact is not fully successful.

## 4. Required higher-level artifacts

### Mode level
Every completed mode must produce:
- a mode summary CSV
- one or more mode plots

### Family level
Every completed family must produce:
- a combined family summary CSV
- one or more family plots

### Suite level
Every completed suite must produce:
- overall summary CSV
- STOA-vs-CO comparison CSV
- CO-only competition CSV(s)
- suite plots
- failure/provenance outputs

## 5. Plot requirement

**Binding**

Plots are required artifacts, not best-effort niceties.

Plots must exist:
- at run level
- at mode level
- at family level
- at suite level

## 6. Semantic validity of outputs

A run or suite is not trustworthy merely because files exist.

Outputs are only valid when:
- labels match actual agent identities
- CO-only summaries exclude STOA rows
- STOA-vs-CO summaries use compatible metrics
- required artifacts are present
- status/provenance matches what actually ran

## 7. Provenance

**Recommended starting point**

Every suite should also preserve:
- the suite config snapshot used
- the expanded suite job manifest
- failure summaries
- execution provenance

This may be promoted to Binding if absence of provenance blocks reproducibility or diagnosis.

## 8. What counts as failure

A run or suite should be considered failed or incomplete if:
- jobs remain indefinitely running
- required artifacts are missing
- plots are missing
- outputs are semantically wrong
- manifest/config resolution silently drops intended behavior
- summaries are mislabeled or structurally misleading