# 99. Relation Algebra Target State

Status: target-state contract; minimal algebra remains open formal watchpoint.  
Binds `_main` file: `TheoryOfChange_main/01_Statements/Clarification/S-CL-minimal-relation-algebra-status.md`.

## Named relations are derived cases

Active named relation types are readable derived cases, not arbitrary labels:

```text
relief;
cancellation;
exposure / shared evidence;
rivalry;
dependency;
proximity;
quotient/equivalence;
weak decision-slot competition.
```

## Deeper coupling basis

Each named relation must identify one or more underlying couplings:

```text
burden coupling;
admissibility coupling;
evidence/visibility coupling;
identity coupling;
collapse coupling.
```

Examples:

```text
relief = burden coupling that lowers same-type operative burden;
cancellation = admissibility/condition coupling that removes a burden-bearing condition;
exposure = evidence coupling that makes hidden burden available;
rivalry = admissibility coupling between continuation-level incompatible branches;
quotient = identity/collapse coupling where differences no longer matter;
weak decision-slot competition = procedural telemetry, not structural rivalry.
```

## Public basis rule

A RelationSurface relation must trace to public burden/effect facts. If a relation depends on hidden state, baseline value, optimality, future reward, or action-name policy, it is invalid for evidence-bearing CO runs.

## Runtime carrier

Relation records should include:

```text
source branch;
target branch;
relation type;
underlying coupling class;
public basis;
operation basis;
weight / strength if used;
leakage status;
weak-vs-strong status;
telemetry reason.
```

## Acceptance diagnostics

```text
weak competition must not become collapse blocker;
relief and cancellation must differ;
shared evidence/exposure must not count as relief;
relations must be sparse enough to preserve structure;
same scalar rows + different relation topology must change field/certificate when relation is operative;
relation counts must separate structural relations from procedural telemetry.
```

## Open status

The target derivation rule is closed. The complete minimal relation algebra is not yet proven. Future work must decide whether named relations reduce fully to coupling classes and how relation composition behaves.
