# 97. Quotient / Equivalence Target State

Status: target-state contract with first-pass runtime helper; operational tolerance remains watchpoint.  
Binds `_main` file: `TheoryOfChange_main/01_Statements/Derivation/S-DR-quotient-equivalence-as-continuation-tolerance.md`.

## Definition

Two branches are quotient-equivalent only when their remaining differences no longer alter active continuation structure under the current anchor and gauge.

They must not quotient merely because of:

```text
same action label;
raw scalar-score similarity;
weak decision-slot competition;
visual/state similarity;
shared candidate source;
current high support.
```

## Required preservation targets

Before quotienting, the runtime must check that the remaining difference does not change:

```text
operative burden profile;
admissible transformations;
relation topology;
grey-preservation need;
recursion demand;
collapse consequence;
readout expression.
```

## Runtime carrier

Quotient state may appear as:

```text
quotient_id;
quotient_share_count;
quotient_resolved_rival_count;
collapse certificate quotient reasons;
relation type = equivalence;
telemetry for quotient basis.
```

## Acceptance diagnostics

Required diagnostics:

```text
same action, different burden regime -> not quotient;
different action, same continuation role -> may quotient;
dense equivalent paths -> quotient/merge, no recursion explosion;
dense non-equivalent paths -> no quotient, preserve grey/recursion;
weak decision-slot competition -> no quotient by itself;
same scalar score, different hiddenness/burden relation -> not quotient.
```

## Open status

The conceptual criterion is closed. The exact runtime tolerance is not final. Runtime approximations must be local, public-fact based, gauge-conditioned, and false-quotient audited before paper claims.


## 2026-05-21 first-pass runtime helper

A first-pass helper now exists at:

```text
ChangeOntCode/agents/co/runtime/surfaces/quotient_equivalence.py
```

It is intentionally conservative.  It derives equivalence only from accepted
public residual profiles passed through `RelationSurface`.  The profile preserves:

```text
public burden / relation domain;
burden operation family;
coarse magnitude band under generic gauge/coarseness;
public scope;
coupling;
threshold status;
basin status;
kind.
```

The helper must not quotient from:

```text
native action labels;
raw scalar-score similarity;
weak decision-slot competition;
rivalry/exclusion facts alone;
hidden/oracle/baseline/solver-like facts;
post-hoc reward or benchmark success.
```

Current diagnostics:

```text
ChangeOntCode/agents/co/tests/quotient_equivalence_first_pass_invariants.py
ChangeOntCode/experiments/studies/quotient_equivalence_first_pass_probe_v1.py
```

Claim boundary: this is a first-pass conservative approximation of quotienting.
It is sufficient for structural probes and implementation audit, but not final
tolerance calibration and not a publication-safe claim that CO has solved
quotient/equivalence.
