# P5 TemporalOps
Current classification: **Provisional**

Useful order-support primitive, but not yet closed as deepest canonical doctrine.

## What this primitive is
P5 provides the minimal temporal-shaping operators the kernel needs **after** some local predecessor order has already been earned. It does not introduce primitive global time. It packages reusable ways of weighting, decaying, cooling, and summarizing ordered traces.

In practice, P5 is where the kernel gets things like:
- exponential moving summaries,
- decay,
- hysteresis,
- cooldown,
- and bounded windows.

## Why this primitive exists
The theory does not treat time as a first imported absolute. But once the route has earned weak local predecessor structure and retained differentiation, the runtime still needs reusable operators for saying:
- older bearing counts less than fresher bearing,
- sustained pressure matters differently than a single spike,
- a just-fired switch should not immediately refire.

P5 exists to provide that **generic temporal shaping** without deciding what the world means.

## What P5 is not
P5 is not:
- a primitive ontology of time,
- a world-clock,
- a semantic interpreter,
- or a policy chooser.

It is a reusable mathematical/operator layer for already-earned ordered traces.

## Inputs and outputs
**Input:** ordered traces or per-step scalar/vector signals.

**Output:** shaped summaries such as:
- EMA-like values,
- decay-weighted counts,
- cooldown gates,
- hysteresis states,
- bounded temporal windows.

## Invariants
1. **Causal directionality:** output at step `t` depends only on inputs available up to `t`.
2. **Monotone decay:** older evidence influence must not increase merely by advancing the index.
3. **Boundedness:** for bounded inputs, bounded summaries remain bounded.
4. **Semantics-neutrality:** P5 shapes order and persistence; it does not decide the meaning of the signals it receives.

## Why this matters for later components
Elements such as HAQ, EC, headers, and collapse controllers need generic ways to work with ordered traces. Without P5, each element would reimplement its own temporal machinery and the kernel would lose consistency.

## Current implementation status
P5 is a valid and useful primitive. It remains dependent on the still-evolving weak-local predecessor doctrine upstream, but as an implementation primitive it is well motivated and reusable.