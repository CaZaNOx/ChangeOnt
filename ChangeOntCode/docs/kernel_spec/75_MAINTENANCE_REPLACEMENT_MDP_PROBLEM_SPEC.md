# Maintenance / Machine-Replacement MDP Problem Family Spec

## Status

Implemented as a first controlled problem-family skeleton. This is **not yet executed evidence** for CO success.

Current files:

```text
environments/maintenance_replacement/env.py
agents/co/adapters/maintenance_replacement_adapter.py
experiments/runners/maintenance_replacement_runner.py
experiments/baselines/maintenance_replacement.py
experiments/studies/maintenance_replacement_stoa_compare_v1.py
agents/co/tests/maintenance_replacement_family_invariants.py
agents/co/tests/maintenance_replacement_stoa_baseline_invariants.py
```

## Why this family is being added

The current mature families test only a limited neighborhood:

- bandit: repeated action choice under reward uncertainty;
- renewal: timing / replenishment / phase-sensitive recurrence;
- maze: constrained movement through visible or partially visible topology.

Maintenance / machine replacement is a distinct, well-studied sequential-decision family. It can nevertheless be parameterized toward bandit-like, middle, and renewal-like regimes, making it useful for testing whether the six-question prior is a generic regime/context language rather than a family-local fitting layer.

## Native problem sketch

A machine has a health/degradation state. At each step the agent chooses among:

- `RUN`
- `INSPECT`
- `REPAIR`
- `REPLACE`
- `WAIT`

Running gives reward but may degrade health or trigger failure. Inspection may reveal state at cost. Repair/replacement restore health at cost. Waiting may allow limited recovery in some regimes. The objective is long-run reward/cost performance.

## Public problem contract fields

Allowed translator/public contract information:

- action labels and legality;
- visible or noisy health observation if exposed;
- observation mode: direct, partial, or hidden;
- public costs/rewards exposed by the environment;
- public failure penalty if specified;
- public horizon;
- visible feedback after each action.

Forbidden translator information:

- optimal repair/replace threshold if solver-derived;
- value-iteration policy or Q-values;
- hidden true health when only partial/hidden observation is public;
- future failure time unless exposed by the environment;
- best-next-action ranking;
- critical-state labels derived from an oracle planner.

## Canonical CO reading

This problem stresses:

- **trace / residue:** past operation changes present health and future risk;
- **identity through change:** the machine remains a continuing system through degradation and repair, while replacement tests identity conditions;
- **remaining transformation burden:** degradation and repair cost are unresolved burden;
- **local cue reliability:** immediate reward from running may be globally misleading;
- **revision cost:** delayed maintenance can make later recovery expensive;
- **consequence span:** action effects propagate beyond the next step.

## Presets and predicted six-question regimes

### A. `bandit_like`

- degradation near zero;
- health matters weakly;
- repair/replacement rarely useful;
- local reward evidence carries forward.

Expected shape direction:

```text
hidden_decisiveness: low to medium
reshapeability: low
local_cue_reliability: high
revision_cost: low
consequence_span: low to medium
topology_constraint: low to medium
```

### B. `middle`

- health matters but does not dominate;
- degradation and repair are meaningful;
- inspection can reduce uncertainty but costs;
- current reward remains informative but incomplete.

Expected shape direction:

```text
hidden_decisiveness: medium
reshapeability: medium
local_cue_reliability: medium
revision_cost: medium
consequence_span: medium to high
topology_constraint: medium
```

### C. `renewal_like`

- operation strongly degrades health;
- repair/replacement resets or restores future opportunity;
- timing/cycle management matters;
- bad timing has long-span consequences.

Expected shape direction:

```text
hidden_decisiveness: medium to high
reshapeability: medium to high
local_cue_reliability: low to medium
revision_cost: medium to high
consequence_span: high
topology_constraint: medium
```

## Baselines

Implemented baseline surfaces:

```text
experiments/baselines/maintenance_replacement.py
experiments/studies/maintenance_replacement_stoa_compare_v1.py
agents/co/tests/maintenance_replacement_stoa_baseline_invariants.py
```

Current baselines:

- `random`: uniform legal action.
- `threshold`: condition/control-limit maintenance policy using only public observed health.
- `threshold_opt`: small sampled public-observation grid search over threshold parameters.
- `finite_horizon_dp` / `dp`: known-model finite-horizon dynamic programming baseline, **parity-valid only when health is publicly directly observed**. It must refuse hidden/partial health rather than silently becoming an oracle.
- `q_learning` / `tabular_q`: sampled public-observation tabular Q-learning baseline. It is not an exact optimum and should be labeled as a trained sampled baseline.

No baseline should receive information hidden from CO, and CO must not receive policy/value information hidden from the baseline. If a future oracle upper bound is added, it must be named as an oracle upper bound and not used as a parity-honest comparator.

## First executed maintenance comparison status

`outputs/maintenance_replacement_stoa_compare_v1.json` is a first small baseline comparison over seeds `0,1,2`. It is **negative evidence for the current CO readout on this family**, not a success claim: threshold/optimized threshold and finite-horizon DP strongly outperform current CO in the tested regimes, while CO is near random or worse in the first run.

This should be classified as an active failure to audit, not explained away post hoc. The likely investigation surface is not the maintenance environment itself but the CO candidate/readout/commitment behavior on this action set: the adapter emits legal public candidates, the six-question shape derives, but the selected CO action behavior is not yet competitive with simple public baselines.

## First validation questions

Before making performance claims:

1. Does the derived shape move in the predicted direction across presets?
2. Do direct runtime controls change accordingly?
3. Do wrong shapes hurt in predictable ways?
4. Does CO differ from greedy threshold/myopic baselines for reasons tied to trace, burden, revision, and consequence span?
5. Are failures interpretable without post hoc relabeling?

## Non-claims

This family does not yet prove:

- that CO beats dynamic programming;
- that the six-question law is proven;
- that current CO readout is empirically competitive on maintenance;
- that negative first-run evidence can be explained away without further structural audit.
