# docs/code_reference/experiments/README.md

# Experiments Folder

## Purpose

`experiments/` contains the harness and orchestration layer.

This folder is responsible for:
- suite execution,
- job expansion,
- config handling,
- family runners,
- logging,
- plotting,
- summaries.

---

## Why it exists

The project needs a single harness that can:
- run STOA and CO comparably,
- scale from small demos to larger suites,
- produce trustworthy artifacts,
- and support mechanism investigation across multiple task families.

---

## Runtime role

The canonical harness flow is:

1. load suite config
2. expand jobs
3. resolve CO injection if configured
4. schedule jobs according to the execution contract
5. launch family runners
6. collect artifacts
7. generate mode summaries
8. generate family summaries
9. generate suite summaries

---

## Main areas

### `suite_cli.py`
Primary suite entrypoint.

Responsible for:
- suite config loading,
- job expansion,
- scheduling/orchestration,
- temp per-run config generation,
- job state tracking.

### `configs/`
Suite configs, CO manifest configs, and related config assets.

### `runners/`
Family execution paths:
- bandit
- maze
- renewal

### `logging/`
Metric and artifact writing support.

### `plotting/`
Collection, summary aggregation, and plot generation.

---

## Contracts

The `experiments/` layer must satisfy:
- scheduler target state,
- run/mode/family/suite artifact contract,
- required plotting contract,
- semantic correctness of suite summaries,
- honest inclusion/exclusion of CO and STOA rows.

---

## Documentation requirement

Every major file or subsystem in `experiments/` should state:
- what it does,
- what files it reads/writes,
- what contracts it must satisfy,
- and whether current behavior matches target state.