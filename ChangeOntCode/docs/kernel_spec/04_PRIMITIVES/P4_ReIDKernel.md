# P4 ReIDKernel
Current classification: **Canonical**

Core continuity/re-identification primitive on the active default path.

## Purpose

P4 is the **re-identification kernel**: a minimal operator for *sameness-through-change* grounded in admissible continuity.

Unlike P1 (bend burden), which is a generic comparison, P4 is identity-oriented:
- it aggregates continuity evidence over a trace
- it yields continuity and fracture-style signals

---

## First-layer caution

P4 is better grounded than the weakest locality bridge, but it still inherits some evolving first-layer supports around admissibility and continuity.

So read P4 as:
- a bounded identity-evidence primitive,
- not a proof that the full philosophical identity doctrine is already maximally closed.

Use alongside:
- `../../../../TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md`
- `../../../../TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md`

---

## Charter

### Domain / Codomain

- **Domain:** `(trace, reference_trace | memory, comparison/admissibility evidence)`
- **Codomain:** a small identity summary, at minimum:
  - `continuity_conf ∈ [0,1]`
  - `fracture_pressure ∈ [0,1]`

### Invariants (binding intent)

1. raising persistent mismatch must not increase continuity
2. bounded local mismatch should not cause immediate fracture
3. persistent mismatch should raise fracture pressure

### Notes

- P4 is *not* an element. It must not choose actions.
- Gauge may later refine cross-context transport of identity judgments, but gauge is not ontologically prior to ReID itself.
- P4 provides identity evidence that EC (and others) may use.

## Current implementation status

Current code now implements a **stateful admissibility-first realization** with:
- burden/admissibility bands learned from recent history
- continuity/fracture/admissibility updates over memory cohorts
- preserved/altered and burden side channels
- cohort-aware re-identification frequency

This remains bounded by kernel memory and finite traces, but it is now a substantive realization of the documented role rather than a thin wrapper.