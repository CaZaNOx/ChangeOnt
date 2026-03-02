# docs/code_reference/agents/co/core/contracts_and_context.md

# CO Contracts and Context

## Purpose

This area documents shared kernel-side contracts and context objects.

These are the pieces that make the kernel’s internal signals and packets understandable and stable.

---

## Why it exists

Without clear contracts/context:
- packets drift,
- signal semantics drift,
- different files silently assume incompatible structures.

This is exactly what a docs→code pipeline must prevent.

---

## Likely covered files

### `contracts/signals.py`
#### Role
Shared signal/packet definitions or helpers.

#### Why needed
The kernel uses structured contribution packets and bus-related updates rather than arbitrary ad hoc dicts.

#### Requirement
Signal and packet semantics must match the target-state docs.

---

### `context/math_context.py`
#### Role
Math/policy/context object for kernel-side interpretation or operator choice.

#### Why needed
A place to keep context-sensitive operator semantics explicit rather than silently global.

#### Requirement
If used in active runtime, its status and effect must be documented honestly.

---

## Target-state requirement

**Binding**

The contracts/context layer must support:
- structured element packets,
- clear signal semantics,
- stable internal representations,
- and explicit runtime context rather than hidden assumptions.

---

## Misalignment examples

This area is misaligned if:
- packet/signal contracts are underdefined,
- callers and callees assume different structures,
- or context objects exist but their runtime role is undocumented or effectively dead.