# docs/code_reference/agents/co/README.md

# Agents CO

## Purpose

`agents/co/` contains the ChangeOnt kernel and the code needed to integrate it into executable task-family runs.

This folder is the implementation-side home of:
- internal kernel mechanics,
- adapters,
- translator integration,
- headers,
- and kernel assembly logic.

---

## Why it exists

The project needs an executable kernel that can:
- receive translated task-local input,
- operate in a CO-native internal form,
- emit a continuation surface,
- and be compared honestly against STOA baselines.

---

## Runtime role

In the canonical runtime path:

1. a runner chooses a CO agent variant,
2. integration/build logic constructs the kernel,
3. a family adapter and translators bridge between environment and kernel,
4. the kernel processes path-space updates and emits continuation structure,
5. a translator maps that continuation structure into a concrete task action.

---

## Main subareas

### `adapters/`
Family-side CO interfaces.
Responsible for:
- shaping task-local observations into kernel entry calls,
- calling select/update style operations,
- and bridging runner execution with translators/kernel.

### `core/`
The kernel’s internal mechanics:
- primitives
- elements
- combinators
- contracts/context
- action/fusion logic

### `headers/`
Meta-header and header logic.
Responsible for:
- prior regime framing,
- live runtime regime modulation,
- classicality/cadence/sensitivity control.

### `integration/`
Build and assembly layer.
Responsible for:
- constructing kernel variants from config,
- connecting translators/adapters/headers/core.

### `registries/`
Registry and factory-like metadata/config support.
Should not drift from the active runtime path.

### `combos/`
Combo/kernel-configuration artifacts.
These must be clearly marked as:
- active canonical variant definitions,
- optional config artifacts,
- or legacy/experimental.

### `tests/`
Smoke and other CO tests.

### `utils/`
CO-side helper utilities.

---

## Key contracts

The `agents/co/` tree must respect:
- internal representation contract,
- header/meta-header contract,
- primitive→element composition contract,
- element contribution packet contract,
- fusion/classical collapse contract,
- translator boundary contract.

---

## Current documentation rule

If any file in `agents/co/` is:
- active runtime,
- optional runtime,
- experimental,
- or legacy/inactive,

that status should be documented explicitly.

No second hidden runtime architecture should remain ambiguous.