# Developer Guide (Code)

## Lanes (avoid conflicts)
- Kernel: `agents/co/` (primitives, elements, headers, combinators, translators)
- Harness: `experiments/` (suite, runners, configs, logging, plotting)
- Envs: `environments/`
- Baselines: `agents/stoa/`
- Docs: `docs/` (these 6 pages are binding; annex is legacy)

## Add a new environment
1) Implement the environment under `environments/<family>/...`
2) Update the family runner in `experiments/runners/<family>_runner.py` to construct it
3) Ensure the runner emits a valid observation envelope (see `03_BINDING_SPEC.md`)
4) Add a suite entry in `experiments/configs/suite_all.yaml`
5) If CO needs a new translator, add one under `agents/co/integration/translators/`
6) Run the suite and QA

## Add a new baseline agent (STOA)
1) Implement under `agents/stoa/<family>/...`
2) Add it to the family runner switch
3) Ensure budget and metrics are comparable to existing agents
4) Add it to `experiments/configs/suite_all.yaml`
5) Run the suite and QA

## Add/modify a CO element or primitive
Rules that prevent drift:
- Do not create alternate runtime paths. The only canonical path is adapters → `C_Pipeline.run/run_update`.
- Elements must call primitives, not re-implement primitive logic inside elements.
- Publish votes via `co_bus.push(...)` and scalars via `co_bus.set(...)` with stable keys.
- Update this binding spec only when behavior truly changes.

## When to update the binding spec
- Update `03_BINDING_SPEC.md` when an implementation change affects adapter envelopes, mask semantics, vote/signal APIs, or telemetry keys.

