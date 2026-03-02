# docs/code_reference/01_REPO_MAP.md

# Repository Map

This file maps the main code folders to their project role.

## Top-level code folders

### `agents/`
Contains agent implementations and agent-related runtime logic.

Subdivides into:
- `agents/co/` for ChangeOnt kernel and related integration
- `agents/stoa/` for classical / baseline / STOA agents

### `environments/`
Contains task-family environments.

These define the worlds that runners execute against.

### `experiments/`
Contains the harness:
- suite orchestration
- config loading
- runners
- logging
- plotting
- summaries

### `outputs/`
Generated artifacts from runs and suites.

### `tools/`
Auxiliary helper tools/scripts.

---

## Project runtime backbone

The canonical runtime backbone is:

1. suite config is expanded by `experiments/`
2. per-run jobs are launched via family runners
3. runners construct environments and agent paths
4. STOA jobs call classical baseline logic
5. CO jobs call translators/adapters/kernel logic
6. artifacts are written
7. summaries and plots are generated

---

## Current documentation intent

This code-reference layer is not the place for deep ontology.

It is the place to answer:

- what is this file/folder for?
- where does it sit in runtime?
- what contract does it satisfy?
- is it canonical, optional, experimental, or legacy?