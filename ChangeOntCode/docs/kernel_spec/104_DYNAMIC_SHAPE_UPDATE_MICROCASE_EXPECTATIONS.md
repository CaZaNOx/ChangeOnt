# 104. Dynamic Shape Update Microcase Expectations

Status: expectations + first-pass structural tests implemented as of 2026-05-21; still not runtime reward evidence.  
Depends on: `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` and `_main` derivation `022A`.

## Purpose

These expectations define what dynamic shape implementation must do before it is allowed into evidence-bearing empirical runs. They are written before implementation to reduce the risk of benchmark-driven tuning.

Each microcase must be tested without native action-name bonuses, hidden state, or baseline guidance.

## Microcase 1 — repeated carrier burden amplifies local urgency

Given:

```text
branch C carries unresolved burden across repeated public trace;
branch C has no resolver operation;
branch R has explicit public resolver support for C's carried burden;
original shape prior is unchanged.
```

Expected:

```text
local shape-state records increased burden_persistence / delay pressure;
projection_horizon shortens or resolver timing pressure rises;
shape update does not mutate original shape_prior6;
resolver pressure can increase next-cycle commitment sensitivity.
```

## Microcase 2 — successful exposure reduces hiddenness pressure

Given:

```text
branch R exposes/reveals previously hidden public structure;
subsequent observation confirms reduced hiddenness or improved cue reliability.
```

Expected:

```text
hiddenness_pressure decreases;
gauge_confidence or local_cue_reliability_effective may increase;
coarseness radius may shrink locally if new distinctions become operative;
no hidden state is recorded unless exposed.
```

## Microcase 3 — failed exposure does not invent knowledge

Given:

```text
branch R attempts exposure;
observation gives no new public distinction.
```

Expected:

```text
hiddenness_pressure may remain or increase;
no topology/reward/hidden fact is inferred;
shape update logs skipped or inconclusive evidence.
```

## Microcase 4 — topology discovery updates known admissibility, not actual topology

Given:

```text
maze-like public exploration discovers a blocked transition.
```

Expected:

```text
known_admissibility changes;
local topology_constraint_effective may rise;
projection horizon through that region shortens;
actual environment topology is not edited by the kernel.
```

## Microcase 5 — stable low-coupling projection permits coarsening

Given:

```text
a local relation remains stable across trace;
small distinctions inside a region do not alter burden, admissibility, relation topology, or collapse consequence.
```

Expected:

```text
coarseness_radius can widen for that region;
point-like collapse becomes more admissible;
telemetry records which distinctions were judged non-operative.
```

## Microcase 6 — high coupling / sensitivity consumes projection horizon

Given:

```text
small public differences repeatedly change burden or admissibility outcomes;
relations are dense or unstable.
```

Expected:

```text
projection_horizon shortens;
coarseness_radius narrows;
recursion or nonclosure demand may rise;
commitment becomes less collapse-ready.
```

## Microcase 7 — resolver relation changes shape only when relation is explicit

Given:

```text
candidate R has native name suggesting repair/inspect/sample, but no public resolver effect.
```

Expected:

```text
no resolver-driven shape update;
no action-name bonus;
shape_state_after differs only if other public evidence supports it.
```

## Microcase 8 — transform/transfer is not resolution by itself

Given:

```text
candidate T transforms or transfers burden without reduce/reveal/cancel/buffer evidence.
```

Expected:

```text
transform pressure may affect openness or nonclosure;
resolver support does not rise solely from transform/transfer;
shape update may mark redirected burden, not resolved burden.
```

## Microcase 9 — revision success lowers future revision pressure

Given:

```text
branch R revises a prior commitment;
public response shows revision was admissible and not highly costly.
```

Expected:

```text
revision_cost_effective may decrease locally;
reshapeability_effective may increase locally;
no global prior axis is overwritten.
```

## Microcase 10 — failed revision raises narrowing pressure

Given:

```text
branch R attempts revision;
public response shows blocked, costly, or narrowing outcome.
```

Expected:

```text
admissibility_pressure rises;
projection horizon may shorten;
future collapse should be more conservative in that region.
```

## Microcase 11 — reward alone does not update shape

Given:

```text
a branch receives higher/lower reward but no public burden, admissibility, relation, hiddenness, or topology evidence changes.
```

Expected:

```text
reward may be logged as outcome;
shape update must not infer hidden shape changes from reward alone;
performance hindsight cannot retune shape.
```

## Microcase 12 — shape update ablation is visible

Given:

```text
a dynamic shape implementation is active;
a matching run disables dynamic shape update but keeps all other kernel components fixed.
```

Expected:

```text
shape_state telemetry differs;
any commitment difference is traceable to specific public shape-update fields;
if no behavior changes occur, that is reported honestly rather than hidden.
```

## Pass condition for implementation readiness

A dynamic shape implementation can enter broader structural validation only when:

```text
all microcases pass;
all update fields have formula ledger entries;
logs expose before/update/after shape state;
ablation can disable dynamic shape independently;
no microcase uses hidden state, action names, reward hindsight, or baseline policy;
existing no-fallback and adapter-boundary invariants still pass.
```
