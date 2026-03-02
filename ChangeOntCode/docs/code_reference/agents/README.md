# docs/code_reference/agents/README.md

# Agents Folder

## Purpose

The `agents/` folder contains the executable decision logic used by the harness.

It has two major branches:

- `co/` — ChangeOnt kernel and integration
- `stoa/` — classical baseline/STOA algorithms

---

## Why it exists

The harness needs a common place for:
- problem-family classical baselines,
- CO kernel adapters and logic,
- and any shared agent-side interfaces.

---

## Runtime role

Runners select an agent family and instantiate:
- either a STOA agent path,
- or a CO adapter/kernel path.

`agents/` therefore sits directly on the runner side of execution.

---

## Subfolders

### `co/`
Contains:
- adapters
- headers
- integration/build logic
- kernel core
- registries
- combo/config-like kernel artifacts
- tests/utilities

### `stoa/`
Contains:
- bandit baselines
- maze baselines
- renewal baselines
- family-specific classical models

---

## Contracts

The `agents/` tree must satisfy:
- runner-facing agent instantiation contracts,
- family-local select/update logic,
- and faithful distinction between CO and STOA runtime paths.

---

## Status guidance

- `agents/co/` is the philosophically load-bearing side.
- `agents/stoa/` is the baseline comparison side.
- neither should silently impersonate the other or hide comparison semantics.