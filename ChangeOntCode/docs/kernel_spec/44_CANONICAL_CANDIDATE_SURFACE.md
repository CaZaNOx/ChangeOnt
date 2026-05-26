# 44 Canonical Candidate Surface

Status: active working contract, implementation-facing.

This file defines the canonical role of `CandidateEvidenceSurface` / CandidateSurface inside the current relation-aware execution loop.

## Layer placement

`CandidateEvidenceSurface` belongs to the kernel runtime machinery. It is not a six-question placement axis, not a problem adapter, not final readout, and not a deep ontology primitive.

Clean chain:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity
→ Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

## Ontological source

The surface operationalizes this part of the CO chain:

```text
trace / residue
→ recurrence
→ local comparability
→ remaining transformation burden
→ identity-through-change
→ collapse / commitment
```

A candidate is a possible local continuation. Candidate publication must therefore describe whether that continuation is supportable through unfolding change, not merely whether it has the best immediate cue.

## Canonical fields

The surface may publish only generic CO-native candidate structure:

- `local_support`: thin immediate support from public local evidence.
- `support_mass`: candidate-local evidence mass after uncertainty/testedness/coverage are accounted for.
- `burden_pressure`: bounded unresolved transformation burden for that candidate.
- `burden_relief`: relative relief a candidate offers when the candidate set contains burden.
- `preventive_support`: generic support for a lower-burden continuation under burden-sensitive controls.
- `sampling_demand`: pressure to keep nonclosure open when hiddenness/uncertainty/rivalry are high.
- `commitment_stability`: support that appears stable under expected change.
- `fracture_state`: candidate instability / contradiction burden.
- `decision_state`: publication summary for downstream commitment.

- `support_persistence`: support carrying across recent updates.
- `burden_accumulation`: unresolved transformation burden carrying or rising across updates.
- `burden_trend`: recent positive burden growth.
- `continuation_instability`: pressure that the continuation is losing coherence.
- `continuation_viability`: whether the continuation remains supportable through unfolding change.

## Forbidden fields as canonical drivers

The surface must not consume adapter-authored mature policy verdicts as direct action quality, including:

- optimal-action flags,
- threshold/control-limit decisions,
- shortest-path decisions,
- UCB/value-iteration scores,
- family-specific action preferences,
- `goal_relation`, `reward_relation`, or `context_relation` when these are already adapter-level rankings.

Such fields may exist in inactive packets for audit compatibility, but canonical publication must not depend on them.

## Preventive support rule

Some actions have low immediate local support but high continuation value because they reduce accumulated burden. CO needs this distinction; otherwise the readout collapses into local score picking.

The generic rule is:

```text
If candidate set burden is active,
and one admissible candidate has lower burden than the burden-heavy alternatives,
and the regime has high path/consequence/nonlocal sensitivity,
and the candidate has enough public evidence quality,
then that candidate gains preventive_support.
```

This rule must remain relative to generic candidate burden. It must not know action names or problem family names.

## Role of six-question controls

The six questions do not choose candidates. They modulate how candidate structure is published:

- high local authority / cue reliability lets local support dominate more;
- high nonlocal authority / hidden decisiveness increases sampling and burden sensitivity;
- high path sensitivity / consequence span amplifies burden and preventive support;
- high revision permissibility makes reopen/sampling and preventive alternatives more admissible;
- high support carry-forward stabilizes recurrent support.

## Required invariants

1. Changing another candidate cannot change a candidate's purely local evidence fields.
2. Adapter-authored goal/bestness relations do not change canonical publication.
3. Higher burden increases fracture and lowers decision support for the same local evidence.
4. When burden is active, a lower-burden candidate can gain preventive support without action-name checks.
5. Hiddenness/uncertainty controls increase sampling demand.
6. The same candidate packet under different direct controls can produce different publication rows.
7. No family-name or action-name literal may appear in the canonical surface implementation.

## Failure meaning

If candidate publication remains local-support dominated after this contract, then six-question placement can reach the runtime but still fail to causally shape action. That is a kernel-runtime failure, not a maintenance-specific failure.

## Continuation-state bridge

See also `46_CONTINUATION_STATE_AND_VIABILITY.md`. Candidate publication now uses a bounded continuation-state tracker so a candidate can lose viability when burden accumulates even if current local support remains high.

## Candidate publication into recursive continuation field

Candidate publication should be understood as seeding and updating the recursive continuation field, not merely emitting rows for max-score action selection. `47_RECURSIVE_CONTINUATION_FIELD.md` defines how candidate burden, relief, sampling demand, and continuation viability can become branch interaction, debt, quotient/merge pressure, and collapse-delay structure.

### Recursive field invariant dependency

Candidate publication seeds the recursive continuation field. It must therefore emit enough public, generic structure for the invariants in `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md` to be testable: local support, burden/debt cues, relief relation, uncertainty, admissibility, proximity/equivalence hints where public, and anti-smuggling audit metadata.


---

Implementation note: the minimal runtime contract for the first executable version is recorded in `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md`. That file is not a success claim; it is the v1 contract for abstract invariants and diagnostics.

## Conceptual closure update — 2026-05-06

Candidate publication is no longer sufficient if it emits only action-shaped scalar rows. For RCF to test a real continuation-field claim, CandidateSurface or a downstream RelationSurface must preserve and publish enough public structure for continuation identity and relation publication.

Binding follow-up contracts:

- `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md`
- `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`
- `79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md`

CandidateSurface may publish scalar support/burden fields as bounded proxies, but final paper use requires formula ledgers. It must not silently promote scalar burden-relief into relation-grounded relief unless the relation can be traced to public burden/effect facts.

A candidate row that contains `continuation_id` or `branch_id` must preserve that identity for downstream field interaction. Native `action` remains an interface expression, not the default continuation identity.
