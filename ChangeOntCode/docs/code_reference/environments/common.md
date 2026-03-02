# docs/code_reference/environments/common.md

# Common Environment Contracts

## Purpose

This file documents the common expectations that all environment families must satisfy.

The project supports multiple task families, but the harness and runners still need a common baseline contract for:
- initialization,
- stepping,
- terminality,
- legality,
- and feedback.

---

## Why it exists

Without a common environment contract:
- runners drift,
- translators receive inconsistent assumptions,
- artifacts become hard to compare,
- and new environments become difficult to integrate honestly.

---

## Canonical common contract

**Binding**

Every environment family should define, clearly and consistently:

### 1. Reset behavior
- how an episode/run starts
- what reset returns
- what parts are stable across resets
- what is randomized across resets

### 2. Step behavior
- what an action means
- what the step call returns
- how legality is enforced
- how reward/feedback is represented
- how terminality is represented

### 3. Observation boundary
- what task-local information is available to the runner
- what can be translated into CO-facing structure
- what remains family-local and is not part of the kernel’s native representation

### 4. Constraint boundary
- what actions are legal
- which constraints are hard vs soft
- how illegal or masked actions are handled

---

## Relation to translators

**Binding**

Environments do not directly define the CO internal representation.

They define the task-local world.

Translators decide how task-local environment structure becomes CO-facing path-space updates.

---

## Relation to classical baselines

**Binding**

Environments must expose enough task-local information for honest STOA baseline execution.

A family should not be made artificially difficult for STOA by hiding information that the family’s classical baselines legitimately need.

---

## Relation to CO

**Binding**

Environments must also expose enough structure through runners/translators that the CO kernel is not starved.

A CO path is not honest if environment → translator → kernel flow erases most of the structure the kernel claims to reason about.

---

## Misalignment examples

The environment layer is misaligned if:
- reset/step semantics are undocumented,
- legality handling is unclear,
- observations are implicitly task-local but treated as if they were already CO-internal,
- or the environment exposes too little structure for an honest family comparison.