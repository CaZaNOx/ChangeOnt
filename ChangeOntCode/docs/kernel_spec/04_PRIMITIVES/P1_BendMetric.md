# P1 BendMetric
Current classification: **Canonical**

Core comparison primitive on the active default path.

## Purpose

P1 BendMetric encodes a minimal reusable notion of **directional deformation burden** between two traces.

Its role is to support:
- identity testing
- closure testing
- recurrence comparison
- path-family grouping

It is primitive because once change is treated as primary, some distinction between lesser and greater transformation burden is unavoidable.

---

## First-layer caution

The present philosophical source of truth is:
- `../../../../TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md`
- `../../../../TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md`

For P1 this means:
- root change is still read first as **happening / modulation / non-flat givenness**,
- carried-conditioning and proto-retention supports remain canonical but partly evolving,
- P1 must not be overread as if a full neutral metric background were already settled.

---

## Primitive Role

P1 is a **comparison primitive**, but not yet a full classical metric.

It does not presuppose a neutral geometric background.  
It provides a reusable distance-like quantity or burden measure that downstream identity and closure mechanisms may use.

---

## Inputs

P1 consumes:
- `trace_a`
- `trace_b`

A trace is a finite ordered sequence of tokens representing a local unfolding.

---

## Outputs

P1 returns a bend/deformation quantity, for example:
- `last_d: float`

Downstream logic may derive additional decisions from it, but the primitive itself is fundamentally the burden provider.

---

## Charter

### Domain / Codomain

- **Domain:** `(trace_a: Sequence[token], trace_b: Sequence[token])`
- **Codomain:** a normalized burden / distance-like value

### Invariants

Binding intent for v1:
1. zero self-burden on identical normalized traces
2. bounded output
3. monotone mismatch under stronger misalignment

### Notes

- Symmetry may hold in the current simplified implementation, but should not be treated as the deepest ontological commitment.
- Later stabilized regimes may approximate classical metric behavior; that is not the first meaning of bend.

## Current implementation status

Current code now implements a **bounded doctrinal realization** with:
- weighted directional alignment over bounded traces
- explicit insertion/deletion/substitution/transposition costs
- preserved-vs-altered decomposition recovered from the alignment
- backward-compatible symmetric distance for inactive callers

This remains a finite kernel implementation rather than a final metaphysical completion, but it is no longer merely a thin scalar proxy.