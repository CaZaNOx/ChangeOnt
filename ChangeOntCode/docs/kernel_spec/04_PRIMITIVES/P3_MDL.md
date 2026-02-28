# P3 MDL

## Purpose

P3 MDL encodes a reusable notion of **complexity/compressibility pressure**.

Its role is to support:
- birth pressure moderation
- simplicity/complexity tradeoffs
- compression-sensitive mechanism decisions

---

## Primitive Role

P3 is a **complexity-pressure primitive**.

It should not be interpreted as “MDL because machine learning likes MDL.”  
Its philosophical role is broader:

- if change forms local regimes and closures,
- then some notion of compression / parsimony / descriptive economy becomes highly plausible.

P3 is the current operational encoding of that pressure.

---

## Inputs

P3 may consume:
- residual/error proxy
- candidate new structure count
- compression proxy
- model-size proxy
- local descriptive cost proxy

The calling element supplies context.

---

## Outputs

P3 returns one or more quantities such as:
- complexity penalty
- mdl-like gain
- compression pressure scalar

It does not itself decide births or actions.

---

## State Mutation

P3 should ideally be pure or near-pure.

If it caches internal values, those must remain semantically auxiliary.

---

## Binding v1 Interpretation

In v1, P3 is allowed to be implemented using a simple penalty law such as:
- gain-like quantity minus weighted complexity cost

This is a minimal operationalization, not a claim that the final true law is classical MDL exactly.

---

## Why this primitive exists

If local regimes stabilize only under some economy of structure, then change is plausibly constrained by a pressure against arbitrary proliferations.

P3 encodes that pressure in reusable form.

---

## Forbidden

P3 must not:
- directly create prototypes
- directly emit births
- directly decide actions
- silently replace full closure logic

Those belong to elements/mechanisms using P3.

---

## Telemetry

P3 does not need direct primitive telemetry.

Downstream element telemetry may include:
- `EB_GHVC.mdl_gain`

---

## Current Status

P3 is kept, but should always be described as:
- a current complexity/compressibility primitive
- not a final proven law