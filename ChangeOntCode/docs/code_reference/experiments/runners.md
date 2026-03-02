# docs/code_reference/experiments/runners.md

# Family Runners

## Purpose

`experiments/runners/` contains the family execution paths.

Each runner owns the family-specific execution loop and artifact writing for one task family.

---

## Why it exists

Different task families have different environment semantics, but the harness still needs:
- a unified job model,
- a unified artifact contract,
- and honest STOA/CO comparison.

Runners are the family-local realization of that unified contract.

---

## Canonical responsibilities

**Binding**

Every runner must:

1. load its per-run config
2. construct the environment
3. construct the correct agent path
4. execute the family loop honestly
5. write required run artifacts
6. emit the data needed for mode/family/suite summaries
7. satisfy the runner contract and artifact contract

---

## Main files

### `bandit_runner.py`
#### Role
Bandit-family execution path.

#### Expected behavior
- construct bandit environment
- instantiate STOA or CO bandit path
- execute horizon loop
- write metrics/budget/manifest/plot

#### Important target-state checks
- bandit CO should be more than decorative wrapping
- primitive/translator APIs must actually line up
- run should complete and produce required artifacts

---

### `maze_runner.py`
#### Role
Maze-family execution path.

#### Expected behavior
- construct maze environment
- instantiate STOA planners or CO path
- execute episode loop
- write required artifacts

#### Important target-state checks
- one coherent CO runtime lifecycle per run
- avoid pathological endless oscillation / non-termination
- maintain honest update semantics

Maze is currently especially important because it is the strongest live blocker.

---

### `renewal_runner.py`
#### Role
Renewal-family execution path.

#### Expected behavior
- construct renewal environment
- instantiate STOA or CO sequence path
- execute the family loop
- write required artifacts

#### Important target-state checks
- renewal translator/primitive semantics must be real, not fake sequence placeholders

---

## Artifact rule

**Binding**

A successful run must write:
- `metrics.jsonl`
- `budget.csv`
- `run_manifest.json`
- `job_state.json`
- `quick_plot.png`

---

## Misalignment examples

This area is misaligned if:
- a family runner violates the documented lifecycle,
- a runner can hang indefinitely without a documented reason,
- per-run artifact contract is incomplete,
- or CO and STOA paths are not compared honestly within the family.