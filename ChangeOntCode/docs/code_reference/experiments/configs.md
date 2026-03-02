# docs/code_reference/experiments/configs.md

# Experiments Configs

## Purpose

`experiments/configs/` contains the harness configuration surfaces:
- suite definitions
- family/mode settings
- CO variant manifests
- and other config assets

---

## Why it exists

The harness needs an explicit config layer so that:
- runs are reproducible,
- variants are inspectable,
- and implementation choices are not hidden in code.

---

## Main config areas

### Suite configs
Examples:
- `suite_demo.yaml`
- `suite_all.yaml`

#### Role
Define:
- families
- modes
- seeds
- STOA agents
- CO injection behavior
- scheduler controls
- output roots

---

### CO agent manifests
Examples:
- `configs/co_agents/...`

#### Role
Define runnable CO variant configurations.

#### Requirement
This is the canonical place to express active CO variant selection unless another place is explicitly documented as canonical.

---

## Target-state config grammar

**Binding at the structural level**
The final config system must be able to express:

- `meta_header`
- `header`
- `primitives`
- `elements`
- `groups`
- `final_fusion`
- `translator`
- `logging`
- `run`

### Important note
The exact YAML syntax is still a **Recommended starting point / open implementation design** unless separately frozen, but the structure above must be representable.

---

## Config truthfulness rule

**Binding**

A parameter should not appear in config as if it matters if the runtime ignores it.

Decorative parameters are a real docs→code misalignment.

---

## Manifest path rule

**Binding**

Manifest resolution must be explicit and robust.

If a suite config points to a CO manifest, the system must not silently run STOA-only due to brittle path resolution.

---

## Misalignment examples

This area is misaligned if:
- configs expose parameters that runtime ignores,
- multiple variant definition paths silently compete,
- manifest paths are ambiguous,
- or current config structure cannot express the documented kernel layers.