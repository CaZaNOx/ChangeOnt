# Kernel Runtime (Canonical)

## Canonical Flow (Files and Calls)
1. Suite entry: `experiments/suite_cli.py`
2. Runner: `experiments/runners/{bandit,maze,renewal}_runner.py`
3. CO adapter: `agents/co/adapters/*_adapter.py`
4. Core builder: `agents/co/integration/core_builder.py::build_co_core`
5. Pipeline: `agents/co/core/combinators/C_pipeline.py::{run,run_update}`
6. Elements: `agents/co/core/elements/*`
7. ActionHead: `agents/co/core/elements/action_head.py::ActionHead.step`
8. Translator: `agents/co/integration/translators/*_translator.py`
9. Logs: `experiments/logging/logging.py::write_metric_line`

## Header Update Ownership
- Header updates occur **only** in `C_Pipeline.run_update(...)`.
- The decision pass `C_Pipeline.run(...)` reads header state but must not call `header.update`.

## Votes and Signals
- Votes are stored in `co_bus` and drained once per decision step.
- Scalar signals are stored in `co_bus` and snapshotted by ActionHead into the `signals` dict.

