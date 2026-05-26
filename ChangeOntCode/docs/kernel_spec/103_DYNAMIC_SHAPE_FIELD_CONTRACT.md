# 103. Dynamic Shape Field Contract

Status: contract + first-pass runtime implementation exists as of 2026-05-21; implementation remains provisional and structural, not empirical proof.  
Binds `_main` derivation: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md`.

## Purpose

This file defines what `DynamicShapeField` is allowed to mean in the kernel. It prevents “shape update” from becoming a hidden solver, reward-tuned patch, or family-specific policy rule.

The current runtime now implements:

```text
static six-question shape prior
+ direct controls
+ local shape-gauged resolver timing inside CommitmentSurface
+ first-pass persistent DynamicShapeField in `agents/co/runtime/surfaces/dynamic_shape_field.py`
```

The DynamicShapeField implementation is deliberately minimal: it persists generic local shape-state and deforms next-cycle controls from public retained trace. It is not a final topology, not a policy module, and not empirical evidence.

## Derived meaning of shape

Use the following distinction:

```text
shape-as-such:
  invariant fact that supportable structured continuation has some local relational-gauge organization.

problem-shape prior:
  initial public coarse regime descriptor derived from the public problem contract.

local shape-state:
  current relational-gauge/coarseness configuration of the bounded local unfolding.

dynamic shape update:
  lawful deformation of local shape-state from public action/result/trace and changed burden/relation/admissibility/coarseness.
```

The six-question prior is not the whole dynamic shape field. It is the current operational prior/gauge.

## Allowed evidence for shape update

A dynamic shape update may use only public or parity-honest retained trace such as:

```text
selected continuation / emitted native action;
observed public response;
legal/admissible action set changes;
public transition or observation change;
public burden-effect facts;
branch-internal burden operations;
RelationSurface relation topology;
RCF debt / grey / viability / recursion summaries;
CollapseCertificate blocker/resolver reasons;
public hiddenness/exposure status;
public failure/recovery events;
public topology discovery events;
public evidence that local cues became more or less reliable;
public evidence that revision became easier/harder;
public evidence that consequence span or delay amplification changed.
```

## Forbidden evidence

A dynamic shape update must not use:

```text
hidden state unless it was lawfully exposed;
DP/baseline value;
best action labels;
reward hindsight to retune shape;
family-private action thresholds;
future trajectory knowledge;
post-hoc benchmark success;
wall/graph/topology facts not publicly discovered;
native action-name bonuses such as “REPAIR is good”.
```

## Allowed update dimensions

The first-pass minimal shape-state tracks generic fields such as:

```text
shape_axes_effective:
  dynamic effective gauge derived from prior axes plus public trace, while retaining the original prior separately.

coarseness_radius:
  how much local detail may be collapsed without changing active burden/admissibility/relation/collapse consequence.

projection_horizon:
  how far continuation can be projected before uncertainty/burden/sensitivity makes the projection non-evidence-bearing.

relation_density:
  how entangled local branches/relations are under current public topology.

burden_persistence:
  whether carried burden is decaying, stable, or amplifying across recent public trace.

hiddenness_pressure:
  current public pressure from unrevealed structure or low cue reliability.

admissibility_pressure:
  whether recent choices are narrowing or widening future admissible continuation.

gauge_confidence:
  confidence that the current local comparison frame remains transportable across updates.
```

These are implemented first-pass runtime categories. Exact formulas remain provisional and require further grounding before empirical claims.

## Invariant / mutable split

The implementation must preserve this split:

```text
invariant / not directly mutable by shape update:
  legal environment topology;
  public action domain;
  problem contract facts;
  original shape_prior6 record;
  no-oracle boundary;
  baseline definitions.

mutable local shape-state:
  effective local gauge;
  coarseness/projection-horizon estimates;
  relation-density estimates;
  public burden persistence/amplification;
  public hiddenness/exposure pressure;
  admissibility narrowing/widening estimates;
  gauge confidence.
```

“Shape update” may change the local interpretation gauge. It may not edit the world.

## Generic update schema

The dynamic update has the target form:

```text
ShapeState_{t+1} = Update(
  ShapeState_t,
  problem_shape_prior,
  selected_continuation_t,
  public_observation_{t+1},
  retained_trace_{t+1},
  burden_delta_{t+1},
  relation_delta_{t+1},
  admissibility_delta_{t+1},
  coarseness_need_delta_{t+1}
)
```

subject to:

```text
no hidden optimality;
no reward retuning;
no action-name policy bonus;
no topology editing;
fail closed if required public evidence is absent.
```

## Relation to current shape-gauged resolver timing

The current `CommitmentSurface` contains a local, ephemeral shape gauge for resolver timing. It is allowed as a first approximation because it uses:

```text
shape_prior6 / direct controls;
carrier-only burden;
certificate/blocker pressure;
resolver support from public effects.
```

It remains distinct from DynamicShapeField: the CommitmentSurface gauge is current-step readout timing, while DynamicShapeField persists coarseness/projection/pressure state across cycles.

## Required implementation gates before code

First-pass implementation gate status: these items are now specified at a minimal level, but remain open for refinement:

```text
1. exact public trace inputs;
2. exact mutable fields;
3. no-oracle proof for each field;
4. update formula ledger entries;
5. microcase expectations;
6. ablation plan;
7. logging schema;
8. fail-closed behavior when shape update evidence is absent or malformed.
```

## Required telemetry if implemented

The runtime must log:

```text
shape_state_before;
shape_update_inputs;
shape_update_delta;
shape_state_after;
fields changed;
public evidence supporting each changed field;
fields explicitly not changed;
whether update was skipped/fail-closed;
whether dynamic shape affected next commitment.
```

## Claim boundary

This file gives the contract for the first-pass implementation. It does not claim that dynamic shape improves reward, proves CO, or establishes final mathematical topology.
