# Six-Question Shape Prior

## Purpose

The kernel receives two conceptually distinct inputs:

1. a **public problem contract** defining lawful actions, visible state, public costs/rewards, task anchor, and constraints;
2. a **six-question shape prior** giving a coarse generic regime/context prior for how change behaves inside that lawful envelope.

Active path:

```text
public problem_contract -> shape_prior6 -> direct_controls -> runtime/kernel
```

The translator must not solve the problem. It only exposes parity-honest public facts. The shape prior is derived from those public facts or declared in a reviewable way before testing.

## Scoring scale

The active public score set is fixed:

```text
0.00, 0.25, 0.50, 0.75, 1.00
```

The implementation may compute raw continuous estimates internally, but the exported `shape_prior6.axes` are quantized to the five public anchor values. Raw estimates are audit telemetry only and are not a second doctrine.

## The 6 canonical questions

### Q1. `hidden_decisiveness`
How much can hidden or unrevealed structure overturn currently best-looking local reasoning?

### Q2. `reshapeability`
How much can the effective problem structure itself change during solving?

### Q3. `local_cue_reliability`
How often does the locally best-looking move remain good once consequences unfold?

### Q4. `revision_cost`
How costly is it to commit wrongly and then revise?

### Q5. `consequence_span`
How far do the effects of a choice propagate before their full significance is visible?

### Q6. `topology_constraint`
How constrained is lawful movement through the action/state space?

## What is not part of the shape prior

The shape prior must not contain:

- best-next-step hints;
- path rankings;
- arm rankings;
- repair/replace thresholds derived by a solver;
- family-private strategy labels;
- exact wall layouts, hidden rewards, or hidden health as shape variables.

Those belong either in the public problem contract, if public and parity-honest, or nowhere.

## Runtime communication

The runtime contract actively communicates:

- `problem_contract`;
- `shape_prior6`;
- `direct_controls` derived from `shape_prior6`.

No alternative public placement vocabulary is active. Runtime contracts should communicate `problem_contract`, `shape_prior6`, and derived `direct_controls`.

## Current evidential status

The six-question prior is the current best placement candidate, not a proven global law. It must still be validated by:

- wrong-shape punishment;
- controlled deformation studies;
- transfer to distinct problem families;
- resistance to hidden translator/readout tuning.

---

## 2026-05-06 status clarification

The six-question shape prior is the active operational regime descriptor for current kernel validation. Its status is:

```text
conceptually motivated;
operationally active;
fixed for architecture validation;
not yet proven minimal, complete, or uniquely necessary.
```

The six axes may guide gauge/control settings, but they must not be presented as a final derived law until independent derivation and ablation establish their sufficiency, independence, and minimality. Any experiment using them must freeze the mapping before evidence runs or clearly mark parameter sweeps as exploratory.

See `100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md`.


## Relation to dynamic shape

The six-question shape prior is the current **initial/public regime gauge**. It is not a persistent DynamicShapeField.

A future dynamic shape implementation may derive an effective local shape-state from public trace, burden, relation, admissibility, hiddenness/exposure, and coarseness evidence. That future state must keep the original `shape_prior6` auditable and may not rewrite it after reward results. See `103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`.
