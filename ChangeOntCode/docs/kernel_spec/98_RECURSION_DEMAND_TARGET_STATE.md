# 98. Recursion Demand Target State

Status: target-state contract with first-pass scheduler implementation; formal/multi-layer unfolding remains a watchpoint.  
Binds `_main` file: `TheoryOfChange_main/01_Statements/Clarification/S-CL-recursion-demand-vs-search-depth.md`.

## Definition

Recursion demand is not the desire to search deeper. It is the need to unfold another layer because the current layer cannot decide quotient, grey, relation, burden, hiddenness, or collapse status.

Search depth asks:

```text
what happens after more actions?
```

CO recursion demand asks:

```text
would another layer change burden, relation, quotient, grey, or collapse legitimacy?
```

## Positive triggers

Recursion demand may rise from:

```text
unresolved non-equivalent rivals;
high hiddenness above gauge tolerance;
masking pressure;
sparse high-consequence unresolved branch;
dense non-equivalent path region;
uncertain quotient boundary;
threshold/phase-shift pressure;
barrier ambiguity where relief exists but accessibility is unclear.
```

## Non-triggers

The following are not sufficient by themselves:

```text
many paths;
high uncertainty as a scalar;
high score gap;
problem difficulty;
weak decision-slot competition;
ordinary action-tree branching.
```

## Runtime carrier

Recursion demand may be carried by:

```text
branch_internal_* pressure fields;
field_grey_pressure;
field_recursion_budget / demand;
collapse_certificate_recursion_demand;
collapse blockers;
trace telemetry.
```

## Acceptance diagnostics

```text
dense equivalent paths -> quotient, not recursion;
dense non-equivalent paths -> grey/recursion;
sparse high-consequence unresolved branch -> recursion despite low density;
many irrelevant paths -> no recursion;
same scalar rows, changed relation topology -> changed recursion demand.
```

## Open status

The distinction from search depth is conceptually closed. A first-pass scheduler now exists at `ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py`. It derives bounded public structural recursion demand before CollapseCertificate. Exact coefficient grounding, real-trace false-positive/false-negative calibration, mature path-density estimation, and any actual second-layer unfolding expansion remain open implementation/formal work.
