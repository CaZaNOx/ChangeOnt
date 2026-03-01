# Architecture and Runtime (Canonical)

## Repo component map
- `environments/` — task worlds (maze/bandit/renewal)
- `agents/stoa/` — baseline agents (SOTA/standard algorithms)
- `agents/co/` — CO kernel (primitives, elements, headers, combinators, translators)
- `experiments/` — harness (suite, runners, logging, plotting)
- `outputs/` — run artifacts and summaries

## Canonical call flow (suite → runner → env → agent)
1) `experiments/suite_cli.py` loads `experiments/configs/suite_all.yaml` (or `--config`)
2) For each job (family × mode × agent × seed):
   - writes a per-run config under `outputs/suite/tmp/...`
   - calls a family runner as a subprocess
3) Each runner:
   - constructs the environment from `environments/<family>/...`
   - constructs the agent (STOA or CO)
   - runs the environment loop and logs metrics

Family runners:
- `experiments/runners/bandit_runner.py`
- `experiments/runners/maze_runner.py`
- `experiments/runners/renewal_runner.py`

## Canonical CO runtime path
Construction:
- `agents/co/integration/core_builder.py::build_co_core(params)`
  - loads `agents/co/registries/registry.yaml`
  - builds header, primitives, elements, combinators

Execution path (canonical surface):
- Adapter select: `agents/co/adapters/*_adapter.py::select(obs)`
  - calls `C_Pipeline.run(...)`
- Adapter update: `agents/co/adapters/*_adapter.py::update(feedback)`
  - calls `C_Pipeline.run_update(...)`
- Pipeline: `agents/co/core/combinators/C_pipeline.py::{run,run_update}`
- Action selection: `agents/co/core/elements/action_head.py::ActionHead.step(...)`
- Translation (family-specific scoring/masks): `agents/co/integration/translators/*_translator.py`

**Canonical surface:** adapters → `C_Pipeline.run/run_update`. Do not introduce alternate entrypoints (direct ActionHead calls, direct element calls, or custom loops). Those are non-canonical and must not diverge from the above path.

## Dataflow: votes, signals, masks
- **Votes:** Elements publish action votes into `co_bus` via `co_bus.push(family, action, weight, ...)`. ActionHead drains votes once per decision step with `co_bus.drain(family)`.
- **Scalar signals:** Elements publish scalar telemetry into `co_bus` via `co_bus.set(key, value)` (or `bus[key] = value`). ActionHead snapshots `co_bus.signals()` and attaches key signals into `co_debug` records.
- **Masks:** Translators return a `translator_mask` set (blocklist). ActionHead removes masked actions from **CO scores** before blending with classical scores (see `03_BINDING_SPEC.md`).
