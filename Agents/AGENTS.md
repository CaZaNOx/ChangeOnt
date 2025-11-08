# Repository Guidelines

## Project Structure & Module Organization
Keep code changes inside `ChangeOntCode/`. `agents/co/` hosts the change-first (CO) implementations, while `agents/stoa/` keeps the classic baselines. Environment fixtures live under `environments/` (bandit, maze, renewal) and experiment orchestration is in `experiments/` with configs in `experiments/configs/` and logs written to `outputs/`. Theory artifacts stay in `TheoryOfChange/`; reference them but do not mix them with runnable code.

## Build, Test, and Development Commands
- `python -m venv .venv && source .venv/bin/activate` — create an isolated Python 3.10+ environment.
- `pip install -r requirements.txt` — install the shared scientific stack for both CO and STOA agents.
- `PYTHONPATH=ChangeOntCode python -m experiments.cli run all --config ChangeOntCode/experiments/configs/suite_all.yaml` — run the unified suite (bandit, maze, renewal) with outputs in `ChangeOntCode/outputs/suite/`.
- `PYTHONPATH=ChangeOntCode python -m agents.co.tests.smoke_co_runner` — quick wiring smoke test for the CO adapter registry.

## Coding Style & Naming Conventions
Use four-space indentation, type hints, and dataclasses where appropriate. Format Python files with `black --line-length 100 ChangeOntCode/…` and keep imports sorted via `isort`. Lint with `flake8` (E203 and W503 already ignored). Favor descriptive module names (`maze_runner.py`, `bandit_adapter.py`) and keep YAML configs snake_case.

## Testing Guidelines
Add unit or property tests beside the feature (`agents/co/tests/` or a new `ChangeOntCode/tests/` module) and target determinism. Run `PYTHONPATH=ChangeOntCode pytest -q` before opening a PR. For scenario smoke checks, rerun the suite command above and attach the updated metrics or plots in `outputs/` instead of embedding binaries in Git.

## Commit & Pull Request Guidelines
Commit messages should state intent in present-tense imperative (e.g., `bandit: add kl-ucb adapter`) and keep scope focused. For PRs, give a short problem/solution summary, list key configs touched, link related issues or theory notes, and include verification details (pytest output, suite run path, or relevant metrics).

## Agent-Specific Notes
When introducing a new CO combo, register it in `agents/co/registries/registry.yaml` and store the combo YAML under `agents/co/combos/`. Keep adapters pure (no file I/O) and route experiment artifacts to `ChangeOntCode/outputs/<family>/<run>/` so they stay gitignored and reproducible.
