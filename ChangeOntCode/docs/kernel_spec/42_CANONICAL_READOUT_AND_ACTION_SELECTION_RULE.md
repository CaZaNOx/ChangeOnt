# 42. Canonical Readout and Action-Selection Rule

## Purpose

Define the canonical separation between:
- candidate enumeration,
- candidate publication,
- kernel commitment formation,
- and final action selection.

This file closes one ambiguity left open in the current repo:
- the candidate surface may publish kernel state,
- but it must not silently become the true policy law.

## Status

This is the active working readout doctrine. The current runtime implements this split through CandidateSurface, RelationSurface, RecursiveContinuationField, CollapseCertificate, first-pass DynamicShapeField next-cycle gauge update, and CommitmentSurface, but formula grounding and reason-quality audits remain open.

## Canonical route

The canonical route is the current certified loop:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity
→ Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
→ admissible native action expression
```

Not:

`adapter semantics -> candidate-local priority verdict -> action`

Older shorthand such as `kernel comparison/formation -> candidate publication -> commitment readout` is only acceptable as a loose description if it preserves the explicit RelationSurface, RCF, and CollapseCertificate stages.

## Layer split

### 1. Candidate enumeration
Responsibility:
- list admissible continuations,
- project native actions into the shared candidate schema,
- and mark prohibition / admissibility.

Allowed inputs:
- boundary Tier A evidence,
- boundary Tier B evidence only where explicitly tolerated.

Forbidden:
- preferred-action labels,
- route rankings,
- planner scores,
- mature relation verdicts standing in for kernel work.

### 2. Kernel comparison / formation
Responsibility:
- form support,
- form contradiction burden,
- form commitment stability,
- form revision pressure,
- form sampling demand,
- and compare admissible continuations under the active direct-control law.

This is where the actual CO work must happen.

### 3. Candidate publication
Responsibility:
- publish the candidate-local kernel state in a generic format,
- expose why a candidate is currently supported, unstable, contradicted, or under-sampled,
- remain descriptive rather than secretly decisive.

Candidate publication may summarize kernel state.
It may **not** import boundary-thick verdicts and present them as if they were kernel-native readout.

### 4. Commitment readout
Responsibility:
- compare published candidate states using the canonical readout rule,
- resolve whether the system is in commit / reopen / sample mode,
- and emit one admissible action or one explicit defer/reopen instruction if the runtime supports that mode.

## Canonical candidate publication record

The candidate publication layer should converge on publishing only kernel-native state such as:
- `admissible`
- `support_mass`
- `contradiction_burden`
- `commitment_stability`
- `revision_pressure`
- `sampling_demand`
- `nonlocal_authority`
- `path_sensitivity`
- optional audit fields explaining which kernel workers contributed

These are the right kinds of readout inputs because they are states of the unfolding comparison, not family-local solution hints.

## Working canonical readout rule

The readout rule should be explicit and auditable.

### Step 1: admissibility filter
Remove all non-admissible candidates.

### Step 2: dominance check
Among admissible candidates, first compare candidates by:
- high `support_mass`,
- low `contradiction_burden`,
- high `commitment_stability`.

If one candidate dominates on those three in a non-ambiguous way, it is selected.

### Step 3: reopen / sampling check
If no candidate dominates and the active state shows:
- high `revision_pressure`, or
- high `sampling_demand`,
then the readout must not pretend a clean commitment already exists.

In that case the runtime should either:
- choose an admissible candidate whose public operations can reopen, expose, reduce, cancel, buffer, or otherwise resolve the unresolved burden;
- or emit an explicit reopen / under-resolved state if the runner permits that mode.

A blocked branch that merely carries or masks the active burden must not be selected in reopen/sample mode when a comparable unblocked resolver candidate exists. Sampling may still select a blocked branch when that branch has its own resolver operation, such as sampling an uncertain arm to reduce that arm's uncertainty, or when no unblocked resolver alternative exists.

### Step 4: certificate-aware stable continuation

If conflict remains after Steps 2 and 3, choose stable continuation using only generic kernel-side quantities such as:

- stronger continuation support after burden,
- certificate readiness / blocker pressure,
- unresolved recursion or hiddenness pressure,
- higher `nonlocal_authority` when consequence depth is high,
- higher `path_sensitivity` when topology constraint is high.

A branch blocked by a non-ready certificate may still continue under unresolved burden when it is materially stronger than all unblocked alternatives. However, if a comparable unblocked continuation exists, the readout must prefer that unblocked continuation rather than selecting the blocked branch merely because it has the highest local continuation score.

No family-local semantic field may enter at this stage.

## Important anti-smuggling rule

The readout law may consume only:
- admissibility,
- kernel-native candidate state,
- and explicit direct-control settings derived from `shape_prior6`.

It may **not** consume:
- Tier C boundary evidence,
- posture labels as hidden action presets,
- or adapter-authored bestness/priority relations.

If a quantity entering readout cannot be traced back to kernel-native comparison state or to direct controls, the readout path is not canonical.

## Relation to direct controls

Readout is not independent of placement.
The six-question shape prior shapes comparison through the direct-control vector.

But the direct-control vector should shape:
- how support forms,
- how contradiction is tolerated,
- how rivalry is widened or narrowed,
- how nonlocal consequences matter,

not directly inject an action decision.

So the correct relation is:

`shape_prior6 -> direct_controls -> kernel comparison state -> readout`

not:

`shape_prior6 -> hidden posture preset -> action`

## Boundary consequence

Because readout must consume kernel-native state, boundary-thick fields like:
- `goal_relation`,
- `continuity_support`,
- `support_depth`,
- `contradiction_hint`,
- `trace_relation`,
- `priority`,

must either:
- be removed,
- be demoted to non-canonical audit residue,
- or be re-expressed as thin evidence that the kernel itself transforms.

## Candidate-surface consequence

A candidate surface is canonical only if it increasingly becomes:
- a publication surface for kernel-native candidate state,

and increasingly ceases to be:
- a hidden scoring layer built from adapter-authored relation verdicts.

## Current repo implication

In the current repo, the canonical repair direction has been implemented at architecture level: candidate rows are published, relation/field/certificate structure is attached, and CommitmentSurface is the final readout. Certificate-aware stable continuation now redirects comparable blocked continuations to unblocked alternatives. The remaining issue is not merely wiring; it is whether the attached reasons, formulas, margins, and gates are sufficiently grounded and behaviorally causal across traces.

## Validation consequence

A canonical readout law must be tested by checking:
1. whether action changes when the kernel-native candidate state changes,
2. whether action stays invariant when non-canonical Tier C residue is removed,
3. whether posture removal leaves a usable readout path,
4. whether direct-control changes alter the candidate state before they alter the final action.

If action changes only because hidden candidate-side scoring changed, the readout law is still not clean.


## Canonical exclusion

Non-canonical candidate scoring helpers are excluded from evidence-bearing readout unless they are explicitly routed through the documented candidate/certificate path and pass the same leakage, formula, and fail-closed audits.

## Readout from recursive continuation field

Canonical readout consumes field-adjusted continuation state rather than raw action-local scores. `47_RECURSIVE_CONTINUATION_FIELD.md` specifies the pre-readout layer: live continuations may interact, merge, cancel debt, increase recursion depth, or preserve grey ambiguity before `CommitmentSurface` collapses to an action expression.

### Recursive field invariant dependency

`CommitmentSurface` may count as CO-native evidence only when the recursive continuation field satisfies the abstract invariants in `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md` and the active trace shows certificate-supported readout. Family-level reward gains should not be read as evidence for a CO-native readout mechanic without that trace.
