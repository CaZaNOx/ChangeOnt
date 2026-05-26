# Problem Specification, Shape Derivation, and Kernel Input

Status: canonical input/shape split.

## Purpose

This file states what the current kernel receives from a problem and how those inputs are separated before execution.

The active chain is:

```text
public problem contract + current observation
→ Boundary / Adapter public packet
→ six-question shape prior
→ direct controls / gauge settings
→ kernel execution loop
```

## 1. Public problem contract

The public problem contract defines the lawful envelope of the problem:

```text
task anchor / continuation condition;
legal actions;
public observations;
public transition grammar;
public costs/rewards when exposed by the environment;
hidden/public distinction;
termination or success condition where applicable.
```

The contract must be parity-honest: it may expose only information available to fair baselines operating on the same problem stream.

## 2. Current observation

Each execution loop also receives the current local observation:

```text
current public signals;
available native actions;
visible local constraints;
current public_effect facts;
any public uncertainty/hiddenness indicators.
```

This observation does not replace the problem contract. It instantiates the current local situation inside that contract.

## 3. Boundary / Adapter duty

The adapter translates native problem information into public kernel-facing structure. It may publish:

```text
candidate expressions;
public facts;
public_effects / burden-effect facts;
problem_contract fields;
shape-prior inputs derived from public structure.
```

It must not publish:

```text
best-next-step advice;
policy rankings;
solver values;
hidden-state conclusions;
post-hoc shape assignments based on observed performance.
```

## 4. Six-question shape prior

The active regime descriptor is the six-question shape prior:

```text
hidden_decisiveness;
reshapeability;
local_cue_reliability;
revision_cost;
consequence_span;
topology_constraint.
```

The six-question prior is conceptually motivated and operationally active. It is not yet claimed as a proven minimal or complete law. See:

```text
74_SIX_QUESTION_SHAPE_PRIOR.md
100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md
```

## 5. Kernel input

The kernel receives:

```text
public candidate expressions;
public burden/effect facts;
continuation anchor;
shape_prior6 / direct controls;
current public observation;
prior continuation state where available.
```

The kernel then performs continuation identity construction, burden operation typing, relation derivation, recursive field update, collapse certification, and commitment/readout.

## 6. Acceptance rule

A problem-family adapter is acceptable only if its public contract and public_effect fields are sufficient for the kernel to derive burden/relation/collapse structure without hidden policy leakage.

If required public structure is absent, the canonical route fails closed or marks the step non-evidential. It must not rescue with first-legal, uniform, greedy, or baseline-policy behavior.
