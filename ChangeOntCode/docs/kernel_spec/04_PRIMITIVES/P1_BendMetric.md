# P1 BendMetric

## Purpose

P1 BendMetric encodes a minimal reusable notion of **difference in unfolding** between two traces.

Its role is to support:
- identity testing
- closure testing
- recurrence comparison
- path-family grouping

It is a primitive because some notion of bend / difference / non-equivalence is structurally unavoidable once change is treated as primitive.

---

## Primitive Role

P1 is a **comparison primitive**, not a full identity mechanism.

It does not decide what identity means globally.  
It provides a reusable distance-like quantity that elements such as `EC_Identity` or closure mechanisms may use.

---

## Inputs

P1 consumes:
- `trace_a`
- `trace_b`

A trace is a finite ordered sequence of tokens representing a local unfolding.

A token may be:
- symbolic
- tuple-like
- scalar-bucketed
- otherwise canonicalized by the caller

P1 does not define the full ontology of trace tokens.  
It defines how two already-provided traces are compared.

Optional config/input:
- `eps` for downstream threshold comparison
- padding token if needed by implementation

---

## Outputs

P1 returns a bend/difference quantity:
- `last_d: float`

Downstream logic may also derive:
- `identity_ok = (last_d <= eps)`

But the primitive itself is fundamentally the distance provider.

---

## State Mutation

P1 is ideally pure:
- no hidden global state
- no task memory
- no environment-specific storage

If implementation caches anything for efficiency, that cache must remain semantically irrelevant.

---

## Binding v1 Algorithm

For v1, P1 uses a minimal finite-trace comparison law:

1. If both traces are empty, return `last_d = 0.0`.
2. If exactly one trace is empty, return `last_d = 1.0`.
3. Let `L = max(len(trace_a), len(trace_b))`.
4. Pad shorter trace with a canonical pad token.
5. Compute normalized mismatch ratio over aligned positions:
   - mismatch count divided by `L`
6. Return the resulting value as `last_d`.

This is a **minimal v1 operationalization**, not a final metaphysical claim about bend.

---

## Why this primitive exists

If change is primitive, then any local identity or closure mechanism must distinguish:
- sufficiently similar unfoldings
- sufficiently different unfoldings

P1 is the current minimal encoding of that demand.

---

## Forbidden

P1 must not:
- use hidden environment state
- contain task-specific logic
- directly choose actions
- silently mutate kernel-global semantic state
- become a full identity mechanism by itself

---

## Telemetry

P1 does not emit telemetry directly.

Telemetry derived from P1 appears through element-level consumers, for example:
- `EC_Identity.last_d`
- `EC_Identity.same`

---

## Current Status

P1 v1 is acceptable as a minimal bend primitive.

Future versions may replace the exact comparison law, but the architectural role stays the same:
- P1 provides reusable bend/difference comparison
- identity and closure mechanisms consume it