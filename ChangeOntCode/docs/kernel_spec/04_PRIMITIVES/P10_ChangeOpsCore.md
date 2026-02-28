# P10 ChangeOpsCore

## Purpose

P10 ChangeOpsCore is the canonical reusable store for **prototype-like local structural units** produced by kernel mechanisms such as birth.

It supports:
- prototype storage
- prototype counting
- downstream closure/grouping
- minimal structural persistence across steps

---

## Primitive Role

P10 is a **state-support primitive**.

It is not itself the birth mechanism.  
It is the reusable place where newly admitted structural units are stored.

This is why P10 may look implementation-shaped: its role is to provide canonical persistence for mechanism outputs that must live somewhere shared and reusable.

---

## Inputs

P10 may consume:
- accepted birth payloads
- trace-derived prototype candidates
- merge/split commands from consuming mechanisms
- canonical prototype tokens/vectors

---

## Outputs

P10 provides:
- prototype store
- prototype count
- append/merge/split support
- stable shared location for downstream consumers

---

## State Mutation

P10 is stateful by design.

Canonical location:
- the kernel primitive registry entry for P10

Canonical internal concept:
- one shared prototype store
- not duplicated in multiple elements

---

## Binding Rule

All prototype-like persistent structural units must live in the canonical P10 store.

Elements must not maintain alternative hidden prototype stores.

---

## Why this primitive exists

If change can locally produce reusable structure-like units, those units need a canonical shared persistence surface.

P10 is that surface.

---

## Forbidden

P10 must not:
- directly decide births
- directly choose actions
- become a hidden element
- be duplicated under alternative semantic stores

---

## Telemetry

P10 itself does not need standalone primitive telemetry.

Derived telemetry may include:
- `prototype_count`
- related birth/merge/split counters from consuming elements

---

## Current Status

P10 is retained, though the name may later be refined.

Its architectural role is valid and should stay:
- canonical shared prototype/state-support primitive