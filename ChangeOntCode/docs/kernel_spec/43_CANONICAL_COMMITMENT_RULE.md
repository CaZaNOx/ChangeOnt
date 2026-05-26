# 43. Canonical Commitment Rule

## Status

Active working implementation doctrine for `agents/co/runtime/surfaces/commitment_surface.py`.

This file derives the implemented commitment/readout rule from ChangeOnt concepts.
It is not a maintenance-specific policy and it is not part of six-question placement.

## Conceptual origin

The relevant ontology chain is:

`trace / residue -> recurrence -> invariant regime -> local comparability -> remaining transformation burden -> identity-through-change -> collapse / commitment`

A candidate continuation is not selected merely because it has the highest immediate local score.
It is selected when its support remains sufficiently stable under unresolved burden, contradiction, uncertainty, and the active regime controls.

## Layer placement

`CommitmentSurface` belongs to the kernel-runtime readout layer.

It is:

- not an ontological primitive,
- not a deep element,
- not a six-question axis,
- not adapter logic,
- not a family policy.

It is a runtime surface derived from the need to operationalize identity-through-change and collapse/commitment.

## Allowed inputs

The canonical commitment rule may consume only:

- admissible candidate identities,
- candidate-publication state produced by kernel/runtime surfaces,
- direct controls already projected from `shape_prior6`,
- generic signal-bus scores and kernel-native telemetry.

The rule may not consume:

- family names as policy branches,
- action labels as policy branches,
- maintenance thresholds,
- maze shortest paths,
- bandit UCB/TS formulas,
- adapter-authored best-action verdicts,
- hidden/oracle environment state.

## Operational derivation

### 1. Admissibility

Bounded local closure admits only some transformations.
Therefore the first readout step is to remove inadmissible candidates.

Implementation check:

- candidate must not be translator-masked,
- candidate must not be marked illegal/non-admissible.

### 2. Local comparability

Once candidates are admissible, they must be compared on shared generic quantities.

Implementation fields:

- `support_mass`
- `decision_state`
- `local_support`
- generic fused field score

### 3. Remaining transformation burden

A candidate can be locally attractive while carrying unresolved future cost or contradiction.
The commitment rule must therefore penalize burden before collapse.

Implementation fields:

- `contradiction_burden`
- `fracture_state`
- `contradiction`
- `burden_accumulation`
- `burden_trend`
- `continuation_instability`

### 4. Identity-through-change

A candidate is more commit-worthy if it preserves support across unfolding change.

Implementation fields:

- `commitment_stability`
- `persistence_state`
- `continuity`
- `continuation_viability`
- `support_persistence`

### 5. Nonclosure / reopening

If no candidate dominates and uncertainty or sampling demand is high, the rule must not pretend that clean commitment has already formed.

Implementation fields:

- `sampling_demand`
- `salience_state`
- `uncertainty`

### 6. Collapse / commitment

Only after admissibility, comparability, burden, stability, certificate state, and nonclosure checks does the rule select an action.

A non-ready/blocking certificate first prevents dominance-style earned collapse. If no dominance or reopen/sample decision is available, stable continuation remains possible, but it is certificate-aware: a comparable unblocked continuation displaces a blocked continuation. A blocked continuation may still be selected only when the unblocked alternatives are outside the comparable support/continuation band or when no unblocked alternative exists.

## Direct-control modulation

The six-question prior does not choose actions.
It projects to direct controls that modulate how strict the commitment rule is.

Examples:

- higher `local_authority` increases trust in local support;
- higher `nonlocal_authority` and `path_sensitivity` increase burden authority;
- higher `revision_permissibility` increases reopening/sampling pressure;
- higher `support_carry_forward` increases continuity/stability authority;
- higher `collapse_admissibility` makes clean dominance easier to collapse into action;
- higher `rival_breadth` widens rivalry and raises sampling pressure.

This relation is:

`shape_prior6 -> direct controls -> candidate comparison state -> commitment readout`

not:

`shape_prior6 -> family strategy -> action`.

## Implemented rule shape

The active implementation follows this staged order:

1. filter inadmissible candidates;
2. compute generic candidate assessment:
   - support,
   - burden,
   - stability,
   - sampling,
   - uncertainty;
3. test dominance;
4. if no safe dominance, test certificate-aware reopening/sampling:
   - prefer a comparable unblocked resolver/exposure branch over a blocked carrier-only branch;
   - allow blocked sampling when the selected branch has its own resolver operation or no unblocked resolver alternative exists;
5. otherwise choose certificate-aware stable continuation:
   - prefer a comparable unblocked continuation over a certificate-blocked branch;
   - allow continuation-under-burden only when the blocked branch is materially stronger or no unblocked alternative exists.

## Anti-smuggling invariant

If a proposed readout check cannot be traced to:

- admissibility,
- comparability,
- support,
- burden,
- recurrence/stability,
- nonclosure,
- or direct-control modulation,

then it is not part of the canonical commitment rule.

## Known limitation

This rule is still provisional. Current code is closer to the documented readout architecture because CommitmentSurface consumes certificate-aware candidate rows and certificate gates. That does not prove that the six-question bridge is sufficient or that CO is competitive across families.

Current validation status:

- structural trace validation is inspectable on the sampled cases;
- structural microcases pass without the previous stable-continuation watchpoint after the certificate-aware correction;
- real-adapter certificate-gating review now shows no standard-sample watchpoints and uses a sweep to exercise resolver-aware reopen/sample redirection;
- the continuation-gating probe preserves an overwhelming-support control where continuation-under-burden remains allowed;
- architecture acceptance still reports watchpoints for relation quality, branch identity trace quality, certificate reasons, public-effect formula grounding, and formula-ledger completeness;
- family reward/performance remains uninterpreted until those structural checks and controlled ablations are clean.

So this implementation is a structural correction, not a benchmark success claim.

## Earned-collapse closure update — 2026-05-06

Commitment is paper-claim safe only when collapse is earned without prohibited fallback. `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md` distinguishes forbidden policy fallback from non-evidential engineering safety.

Relation-aware commitment must tell whether candidate domination or stable continuation occurred after resolving or retaining relevant branch relations: relief, cancellation, quotient/equivalence, strong rivalry, shared evidence, and unresolved grey pressure. CommitmentSurface now consumes certificate-aware fields for dominance, reopen/sample, and stable-continuation gating, but the remaining watchpoint is quality: the reasons, gates, margins, and behavior-affecting coefficients still need broader trace and formula-ledger validation.
