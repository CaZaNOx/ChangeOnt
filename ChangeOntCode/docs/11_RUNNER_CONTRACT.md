# Runner Contract

This file defines the target-state contract that all family runners must satisfy.

## 1. Core runner contract

Every runner must:

1. load family-local run config
2. construct the environment
3. construct the selected STOA or CO path
4. execute the family-local select → act → feedback → update loop honestly
5. write required run artifacts
6. expose enough information for summaries and plots

## 2. Artifact contract

A successful run must produce:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

A run missing required artifacts is incomplete.

## 3. Loop integrity contract

The runner must preserve:
- family-local semantics
- honest action execution
- honest feedback handling
- select/update integrity

For CO paths, this also means:
- translators/adapters are not bypassed in a way that destroys documented semantics
- update is not reduced to meaningless thin bookkeeping
- the kernel is not starved while still pretending to run full mechanisms

## 4. STOA integrity contract

For STOA runs:
- the baseline must be family-appropriate
- the runner must not hide its assumptions
- the STOA path must remain a real comparison stream

## 5. CO integrity contract

For CO runs:
- the runner must preserve the documented boundary contracts
- the run must be structurally faithful enough to support the phrase “CO-honest” once the rest of the stack aligns
- launchability alone is not sufficient

## 6. Termination/progress contract

A canonical runner path must not hang indefinitely in a nominal smoke/demo scenario without that behavior being treated as a real failure.

Pathological non-termination is a runner contract failure.

## 7. Status/provenance contract

The runner and suite together must ensure that:
- status files reflect actual run state
- manifests reflect what actually ran
- failures remain visible

## 8. Misalignment examples

A runner is misaligned if:
- it launches but does not produce required artifacts
- it writes semantically misleading metrics
- it lets CO paths hang indefinitely without detection
- it bypasses the documented CO boundary structure
- it makes honest comparison impossible