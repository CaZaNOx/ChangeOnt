# Canonical Problem Definition and Placement Basis

## Canonical chain

The active canonical chain is:

```text
public problem contract -> six-question shape prior -> direct controls -> kernel unfolding
```

## Two distinct inputs to the kernel

### 1. Public problem contract
The problem contract contains parity-honest information that any legitimate baseline could also receive from the same environment, for example:
- start state / task anchor / win condition;
- legal actions;
- prohibited actions;
- public transition rules;
- public exceptions;
- public rewards/costs if exposed by the environment.

### 2. Six-question shape prior
The shape prior is a generic, coarse regime/context analysis derived from the public problem contract and visible stream. It is not the full problem definition.

The active canonical questions are:
1. hidden decisiveness;
2. reshapeability;
3. local cue reliability;
4. revision cost;
5. consequence span;
6. topology constraint.

See `74_SIX_QUESTION_SHAPE_PRIOR.md` for the explicit rubric.

## Runtime status after cleanup

The intended runtime story is now:

```text
problem_contract + shape_prior6 -> direct_controls
```

The active runtime contract uses `problem_contract`, `shape_prior6`, and derived `direct_controls`.

## Anti-handwave rule

The six-question shape prior must be derived from:
- the public problem specification;
- the visible stream available to parity-honest baselines.

It must not be assigned by family intuition, hidden strategy knowledge, or observed performance after trying multiple shapes.


## Dynamic shape boundary

The active chain above is a **static public prior** plus derived direct controls. It is not the full dynamic shape/coarseness field derived in `_main` `022A`.

A future dynamic shape-state may be updated from public retained trace, changed burden, relation topology, admissibility, and coarseness requirements, but only under `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`. The original public problem contract and original `shape_prior6` record must remain auditable and must not be overwritten by runtime reward or hidden policy information.
