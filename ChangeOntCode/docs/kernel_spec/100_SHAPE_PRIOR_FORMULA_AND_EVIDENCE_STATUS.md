# 100. Shape Prior, Formula, and Evidence Status

Status: conceptual/experimental boundary contract.  
Binds `_main` file: `TheoryOfChange_main/01_Statements/Clarification/S-CL-shape-prior-formula-and-evidence-status.md`.

## Shape prior status

The six-question shape prior is active and may set kernel controls:

```text
hidden_decisiveness;
reshapeability;
local_cue_reliability;
revision_cost;
consequence_span;
topology_constraint.
```

Its status is:

```text
conceptually motivated;
operationally active;
fixed for architecture validation;
not yet proven minimal, complete, or uniquely necessary.
```

The docs/code may use it as a frozen regime descriptor. They must not claim final theoretical sufficiency or minimality until ablation and derivation support that.

## Dynamic shape status

After the `_main` derivation `022A_S-DR-shape-space-directed-unfolding-from-change`, distinguish:

```text
shape-as-such:
  invariant fact that structured continuation has local relational organization.

problem-shape prior:
  fixed public six-question regime descriptor used by the current runtime.

local shape-state:
  future dynamic relational-gauge/coarseness state updated only from public retained trace.
```

Current code implements the problem-shape prior and local shape-gauged commitment corrections. It does **not** yet implement a persistent DynamicShapeField. Future work is governed by `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` and `104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md`.

## Formula status categories

Every active formula affecting field/certificate/readout must be classified as one of:

```text
conceptual constraint;
implementation approximation;
empirical parameter;
provisional diagnostic coefficient;
inactive / inactive residue.
```

## Required formula ledger fields

For every scalar field that affects readout:

```text
field name;
canonical concept compressed;
allowed inputs;
formula;
sign rationale;
coefficient status;
fixed-before-run status;
diagnostics constraining it;
claim boundary;
known failure modes.
```

## Evidence status

Architecture diagnostics are not reward evidence. They show wiring and mechanism behavior. Broader benchmark evidence is interpretable only when:

```text
boundary leakage audit passes;
non-CO rescue selectors are absent;
relation/certificate traces are coherent;
formula and shape status is documented;
baselines are fair and external;
logs connect behavior to mechanisms.
```

## Acceptance diagnostics

```text
formula ledger completeness scan;
shape-control freeze check;
relation/certificate causal trace;
formula-ablation or sensitivity checks where conceptually needed;
no post-hoc retuning before benchmark interpretation.
```

## Open status

Still open: six-axis minimality/independence, exact coefficient values, burden-regime thresholds, quotient tolerance calibration, full formula ledger coverage, and the persistent dynamic shape/coarseness update law.
