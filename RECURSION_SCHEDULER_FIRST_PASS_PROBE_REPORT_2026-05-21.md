# Recursion Scheduler First-Pass Probe Report — 2026-05-21

## Scope

This report records a first-pass implementation of bounded CO recursion-demand scheduling.
It is a structural diagnostic only. It is not empirical evidence that CO works,
not proof of novelty, and not a replacement for quotient/recursion formalization.

## Implemented files

```text
ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py
ChangeOntCode/agents/co/tests/recursion_scheduler_first_pass_invariants.py
ChangeOntCode/experiments/studies/recursion_scheduler_first_pass_probe_v1.py
```

## Runtime placement

```text
CandidateSurface
→ RelationSurface
→ RecursiveContinuationField
→ RecursionScheduler
→ CollapseCertificate
→ CommitmentSurface
```

The scheduler attaches public structural recursion telemetry before certificates.
It may raise `field_recursion_budget` and `branch_internal_recursion_pressure`
for certificate gating. It does not create candidates, inspect native interface
expressions, simulate hidden futures, or choose a commitment.

## Positive structural triggers

The scheduler may raise demand from:

```text
non-equivalent relation density;
relation types that may alter next-layer burden/relation/quotient/collapse status;
sparse high-consequence unresolved pressure;
hiddenness above gauge tolerance;
masking pressure;
threshold/phase-shift pressure;
field grey pressure;
field debt pressure.
```

## Explicit non-triggers

```text
dense equivalent paths → quotient/contract, not recursion inflation;
weak decision-slot competition → logged only;
many rows without structural pressure → no recursion demand;
same scalar rows without relation topology → no structural recursion reason.
```

## Probe result

`python -m experiments.studies.recursion_scheduler_first_pass_probe_v1` produced:

```text
cases = 4
dense_equivalent_contracts max_demand = 0.0
dense_non_equivalent_requests max_demand ≈ 0.457
sparse_high_consequence_requests max_demand ≈ 0.501
weak_competition_only_low max_demand ≈ 0.061
```

## Invariant result

`python -m agents.co.tests.recursion_scheduler_first_pass_invariants` passed.

The invariants check:

```text
dense equivalent region contracts instead of inflating recursion;
dense non-equivalent region raises bounded structural recursion;
sparse high-consequence unresolved branch may request unfolding despite low density;
many irrelevant rows do not create demand;
same scalar rows with changed relation topology change demand;
weak decision-slot competition alone is not a trigger;
scheduler feeds certificates without selecting the interface expression;
source contains no problem-family or native-policy literals.
```

## Remaining watchpoints

```text
coefficients are first-pass and require ledger/sensitivity work;
no actual second-layer unfolding expansion is implemented yet;
path density is relation-local, not a mature continuation graph estimate;
real-trace false-positive / false-negative recursion audits remain open;
known-algorithm comparison remains open.
```
