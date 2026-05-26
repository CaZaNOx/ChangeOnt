# Problem Specification and Six-Question Shape Prior

Status: active `_main` bridge for problem specification and regime placement.

## Core split

A bounded problem is given to the kernel in two conceptually distinct ways.

### 1. Public problem specification

This defines the lawful local closure:

```text
observations exposed by the environment;
lawful actions;
transition legality;
prohibited transitions;
task anchor / success / failure / termination condition;
public reward or cost semantics if exposed by the environment;
hidden/public distinction where applicable.
```

This is the problem envelope. It is not a policy.

### 2. Six-question shape prior

The same public problem can be analyzed as a generic change-regime using the six-question prior:

```text
hidden decisiveness;
reshapeability;
local cue reliability;
revision cost;
consequence span;
topology constraint.
```

This is a coarse regime approximation used to set kernel controls/gauge. It is not the full problem definition and must not encode a solution.

## Active chain

```text
public problem contract
→ six-question shape prior
→ direct runtime controls / gauge settings
→ kernel unfolding and earned collapse
```

## Anti-tuning rule

The split remains honest only if:

```text
the public specification is translator-thin and parity-honest;
the shape prior is derived from generic public questions;
neither side smuggles family-local solving logic;
shape mappings are frozen before evidence runs or labeled exploratory.
```

The translator may expose that a wall blocks a move, that inspection can reduce hiddenness, or that repair can reduce degradation. It may not expose “best next move,” hidden policy, solver value, or post-hoc regime labels.

## Current evidential status

The six-question prior is active and conceptually motivated, but not yet proven minimal, independent, or complete. That status is explicit rather than hidden. See:

```text
ChangeOntCode/docs/kernel_spec/74_SIX_QUESTION_SHAPE_PRIOR.md
ChangeOntCode/docs/kernel_spec/100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md
```
