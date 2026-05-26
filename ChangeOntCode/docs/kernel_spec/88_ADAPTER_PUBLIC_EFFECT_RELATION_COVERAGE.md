# 88. Adapter Public-Effect Relation Coverage

Status: implementation diagnostic / not benchmark evidence  
Date: 2026-05-06

## Purpose

`87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md` established that the kernel can derive relation topology from `public_effects` / `burden_effects` rows.  This file records the next wiring step: active adapters now publish lawful public burden/effect facts so the kernel-side `RelationSurface` has real family rows to consume.

This is **not** a performance claim.  It only verifies that the bridge can carry public facts into relation topology without adapter-authored policy relations.

## Boundary rule

Adapters may publish public transformation grammar:

- this candidate carries a public burden type;
- this candidate reduces a public burden type;
- this candidate exposes hiddenness/evidence;
- this candidate resets/cancels a public burden condition;
- this candidate buffers/absorbs a public burden condition;
- this candidate competes for a legal single decision slot.

Adapters must not publish:

- best-action claims;
- hidden true state;
- DP / baseline / oracle values;
- relation conclusions such as “B relieves A” when that conclusion should be derived by the kernel;
- shortest hidden route or optimal threshold facts.

## Implemented adapter publication

The following adapters now attach `public_effects` to candidate rows:

- `agents/co/adapters/bandit_adapter.py`
- `agents/co/adapters/maintenance_replacement_adapter.py`
- `agents/co/adapters/maze_adapter.py`
- `agents/co/adapters/latent_mechanism_adapter.py`
- `agents/co/adapters/renewal_adapter.py`

A shared helper in `agents/co/adapters/common.py` creates effect facts with explicit `public_basis` and `leakage_status`.

## Minimal family examples

### Bandit

Public facts:

- each arm competes for the single immediate action slot;
- sampling an arm carries and can reduce that arm-local reward uncertainty.

No hidden arm mean, optimal arm, regret-minimizing action, or policy value is published.

### Maintenance

Public facts:

- `RUN` can carry/postpone degradation and hiddenness burden;
- `INSPECT` can reveal hiddenness;
- `REPAIR` can reduce degradation;
- `REPLACE` can reset/cancel degradation-state burden;
- `WAIT` can buffer or carry degradation depending on public recovery/degradation cues.

No true hidden health or optimal threshold is published.

### Maze

Public facts:

- local visible movement can reduce or carry visible goal-distance burden;
- backtracking can carry path-revisit burden;
- partial observability can expose topology hiddenness;
- legal candidates compete for one immediate movement slot.

No shortest-path oracle or hidden map route is published.

### Latent mechanism

Public facts:

- visible movement can reduce or carry route-distance burden;
- interaction with a visible surface can expose mechanism hiddenness or transform mechanism burden;
- revisit/backtracking can carry path burden.

No active-switch truth or hidden mechanism policy is published.

### Renewal

Public facts:

- each symbol/action competes for one immediate sequence-action slot;
- choosing a symbol carries and can reduce symbol-local predictive uncertainty;
- public miss/context entropy can carry prediction burden.

No hidden phase, generator truth, or optimal symbol is published.

## Diagnostics

Added invariant module:

```bash
python -m agents.co.tests.adapter_public_effect_relation_coverage
```

Added diagnostic study:

```bash
python -m experiments.studies.adapter_public_effect_relation_coverage_v1
```

The diagnostic writes:

```text
outputs/adapter_public_effect_relation_coverage_v1.json
```

The current verified run reports:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "rows_with_public_effects": 20,
  "relations_total": 80
}
```

This means the real adapter rows now feed nonzero public-effect relation topology into the kernel-side derivation path.

## Important caveats

1. This is still not benchmark evidence.
2. Relation coverage does not imply reward improvement.
3. Relation publication is intentionally conservative and public-fact based.
4. The current family effects are first-pass public grammar and should be audited before final paper claims.
5. The next evidence-bearing step is to run CandidateSurface/RCF traces showing these derived relations actually alter quotient, grey, recursion, and collapse behavior for traceable reasons.

## Next implementation gap

The remaining gap is no longer “adapters publish no public effects.”  It is now:

> Do derived adapter relations materially and lawfully change RCF/CommitmentSurface behavior on real traces, without collapsing into generic rivalry noise or performance-tuned policy hints?

That requires relation-aware runtime traces and fixed-score / fixed-candidate ablations, not broad reward tuning.


## Branch-internal operation carrier correction

See `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md`. Public burden/effect facts must not disappear when they do not form a cross-branch relation. Branch-internal operations are first-class kernel carriers, while weak decision-slot competition remains procedural telemetry rather than strong rivalry or a collapse blocker.
