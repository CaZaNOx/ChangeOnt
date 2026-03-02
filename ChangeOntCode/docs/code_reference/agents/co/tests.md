# docs/code_reference/agents/co/tests.md

# CO Tests

## Purpose

`tests/` contains smoke or validation tests for the CO runtime.

---

## Why it exists

The project needs quick ways to verify:
- kernel construction works,
- family adapters launch,
- basic selection/update loops work,
- and core artifacts are being produced.

---

## Main files

### `smoke_co_runner.py`
#### Role
Smoke-level runtime validation.

#### Why needed
A cheap test path to confirm the active runtime is not obviously broken.

---

## Target-state testing requirement

**Recommended starting point**

The CO test layer should eventually include at least:

- build smoke tests
- family adapter smoke tests
- select/update loop smoke tests
- artifact presence smoke tests
- representative `CO_full` smoke tests
- representative reduced variant smoke tests

---

## Misalignment examples

Testing is incomplete if:
- the repo claims runnable suites but has no honest smoke path,
- a “demo” suite hangs without a smaller canonical smoke suite,
- or test coverage does not reflect the active canonical runtime path.