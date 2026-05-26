# 78. Runtime Safety and Fail-Closed Contract

Status: active fail-closed and no-rescue contract.

This file exists because robust software still needs error handling, but evidence-bearing CO execution must never be rescued by a non-CO policy.

## 1. Hard prohibition

The canonical CO action path must not rely on:

```text
classical proposal blending;
family-specific greedy rescue;
hidden planner hooks;
threshold-optimal rescue;
shortest-path rescue in hidden/partial maps;
DP / UCB / Q-learning / MCTS values as native CO decisions;
benchmark-regime conditionals;
action-name policy branches;
first-legal, uniform, or score-only rescue selection.
```

If any run depends on such behavior, it is not evidence for the CO kernel.

## 2. Fail-closed runtime safety

Malformed or empty runtime conditions may be reported as contract violations, but they must not be converted into action choices.

Examples of invalid or non-evidential conditions:

```text
no evidence-bearing candidate rows;
empty candidate list due to upstream failure;
missing signal bus for a required canonical surface;
selected branch cannot be projected through a lawful public boundary rule;
nonfinite numeric value that cannot be sanitized without changing policy semantics.
```

Permitted safety behavior must satisfy all conditions:

```text
it does not choose or improve policy performance;
it is family/action agnostic;
it is logged when triggered;
it marks the step as non-evidential;
evidence runs assert that it did not trigger.
```

The correct response to absent evidence is:

```text
raise/log contract violation → no evidence-bearing action for that step
```

not:

```text
choose first-legal action / uniform random / greedy score / baseline-policy rescue
```

## 3. Required telemetry

Any safety event must be labeled in a way that prevents it from being counted as CO behavior:

```text
engineering_safety_triggered: true
co_evidence_valid_for_step: false
safety_kind: <empty_input | numeric_sanitation | malformed_packet | projection_failure | forbidden_rescue_attempt>
```

If equivalent telemetry is absent, the affected step is paper-risky until audited.

## 4. Canonical degenerate cases

A valid CO-degenerate case is allowed only when it remains inside the CO machinery. Example:

```text
no cross-branch relations derivable from public facts
→ RelationSurface emits zero structural relations
→ branch-internal burden operations and weak procedural competition remain logged
→ RCF/certificate proceed with relation_count = 0
```

This is not a rescue selector. It is a traceable structural condition.

## 5. Sampling / randomness

Randomness or sampling is permitted only when a sampling branch is lawfully derived as a kernel continuation. It is not permitted as a substitute for missing evidence.

## 6. Required tests

```text
canonical runs assert engineering_safety_triggered == false for evidence-bearing steps;
malformed-packet tests trigger safety and mark the step non-evidential;
source scans forbid family/action policy literals in safety paths;
experiment summaries report safety trigger counts;
any forbidden rescue count invalidates the run as evidence.
```

## 7. Claim boundary

A code path may be robust engineering without being part of the theory. The paper may mention engineering safety for reproducibility, but such safety cannot be counted as CO behavior.

The canonical claim is supported only by steps where:

```text
translator boundary is clean;
shape/regime input is public and frozen;
kernel surfaces are active;
collapse is certificate-supported;
no non-CO rescue selector triggered.
```
