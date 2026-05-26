# 79. Candidate and Commitment Formula Grounding Protocol

Status: active procedural closure / formula ledgers still required.

This document does not finalize every scalar formula. It closes the procedural gap by defining what must be true before a formula in CandidateSurface, ContinuationState, RCF, or CommitmentSurface may be treated as canonical rather than provisional.

---

## 1. Problem

Several active runtime surfaces contain weighted mixtures and thresholds. Some are reasonable bounded proxies, but final paper standards require that active formulas not function as undocumented theory.

A formula is paper-risky when it is:

- not traceable to `_main` concepts;
- not specified in docs;
- not marked provisional;
- tuned to a family outcome;
- difficult to distinguish from hidden scoring or non-CO rescue selector.

---

## 2. Formula status classes

Every active formula must be marked as one of:

```text
canonical-derived
canonical-constrained-proxy
provisional-global-proxy
investigatory
audit-only
engineering-safety
inactive/off
forbidden
```

### canonical-derived
The formula follows directly from a documented law or invariant.

### canonical-constrained-proxy
The exact numeric form is a bounded implementation of a documented law. The sign, allowed inputs, and monotonic direction are conceptually fixed, but constants may be provisional.

### provisional-global-proxy
The formula is not final but is shared across families and not tuned to one benchmark. It may support investigation but not final proof.

### investigatory
Used to explore whether a concept may become canonical. Must not support paper claims.

### engineering-safety
Runtime guard only. Not evidential.

### forbidden
Violates translator boundary or hidden-solver rules.

---

## 3. Formula ledger template

Each active field/formula must eventually have an entry:

```text
Field / formula name:
Code path:
Surface/layer:
Status class:
_main grounding:
Docs contract:
Allowed inputs:
Forbidden inputs:
Monotonic commitments:
Numerical constants:
Why these signs/weights:
Family tuning risk:
Tests/invariants:
Telemetry:
Paper claim allowed:
Known gaps:
```

---

## 4. CandidateSurface fields needing ledgers

```text
local_support
support_mass
burden_pressure
burden_relief
preventive_support
sampling_demand
commitment_stability
fracture_state
decision_state
support_persistence
burden_accumulation
burden_trend
continuation_instability
continuation_viability
```

---

## 5. CommitmentSurface fields needing ledgers

```text
assessment support
assessment burden
assessment stability
assessment sampling
assessment uncertainty
dominance threshold
reopen/sampling condition
resolver-aware reopen/sample gate margin
sampling support-advantage limit for blocked carrier-only branches
certificate-aware stable-continuation margin
support advantage limit for continuation-under-burden
least-burden stable commitment candidate, if certified or not blocked by a comparable unblocked alternative
collapse readiness condition
```

Any fallback-like rescue selector is prohibited by `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md`; certified commitment must be justified by collapse structure, not rescue logic.

---

## 6. RCF fields needing ledgers

```text
field_debt
field_relief_support
field_grey_pressure
field_recursion_budget
field_collapse_readiness
field_viability
quotient_id
quotient_share_count
field_relation_count
```

RCF relation effects must additionally satisfy `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md` and `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`.

---

## 7. Numerical constants policy

Numerical constants are allowed only if classified:

1. fixed theoretical limit;
2. bounded normalization constant;
3. global implementation proxy fixed before experiments;
4. investigatory sweep parameter;
5. forbidden post-hoc tuned value.

A constant tuned to improve one family/regime may not be canonical evidence.

---

## 8. Minimal acceptance before final paper use

For a formula to support a final paper claim, it needs:

1. ledger entry complete;
2. no forbidden inputs;
3. monotonic direction justified;
4. constants classified;
5. source scan for family/action policy literals where applicable;
6. abstract invariant test;
7. telemetry showing active contribution;
8. ablation or diagnostic showing what the formula changes.

---

## 9. Current status boundary

Until formula ledgers are completed, active runtime surfaces should be described as:

```text
conceptually motivated provisional implementation of the documented kernel architecture
```

not as:

```text
fully derived final algorithmic form of ChangeOnt
```


---

## 9. Initial formula ledger for architecture-acceptance patch

This ledger does not finalize all constants. It records the minimum readout-affecting formulas introduced or touched by the acceptance-correction path.

| Field / formula | Code path | Status class | Allowed inputs | Forbidden inputs | Monotonic commitment | Paper claim status |
|---|---|---|---|---|---|---|
| `relation_weight` | `relation_surface._relation_weight` | canonical-constrained-proxy | public-effect magnitudes and confidence | rewards, hidden state, values, action names | stronger public effects produce stronger relation weights within 0..1 | mechanism diagnostic only |
| `burden_regime_band` | `relation_surface._magnitude_band` | canonical-constrained-proxy | public-effect magnitude / threshold status / basin status | raw hidden state, reward optimality | material regime changes may alter branch signature; within-band jitter should not | architecture identity diagnostic |
| `decision_slot_competition` | `relation_surface._derive_relations` | canonical-derived | legal single-readout-slot fact | policy preference, best-action claim | logs weak competition without unresolved-rival blocking | boundary/architecture claim |
| `collapse_blocker_pressure` | `collapse_certificate.derive_collapse_certificates` | provisional-global-proxy | structured blockers, strong rivalry, grey, debt | generic decision-slot competition alone, rewards | more unresolved blockers increases blocker pressure | mechanism diagnostic only |
| `resolver_support` | `collapse_certificate.derive_collapse_certificates` | provisional-global-proxy | quotient/equivalence, relief, cancellation, buffering, bounded debt/grey | action names, values | more resolution evidence increases support | mechanism diagnostic only |
| `earnedness` | `collapse_certificate.derive_collapse_certificates` | provisional-global-proxy | field readiness, resolver support, controls, blocker pressure | hidden policy/value | stronger readiness/resolution increases earnedness; blockers decrease it | mechanism diagnostic only |
| `recursion_demand` | `collapse_certificate.derive_collapse_certificates` | provisional-global-proxy | field recursion, proximity/recursion relations, strong unresolved rivalry, grey | action names, rewards | unresolved relation/grey pressure raises recursion demand | mechanism diagnostic only |
| `collapse_blocked` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | certificate blocker pressure, strong unresolved rivals, quotient resolution | raw relation telemetry, weak decision-slot competition alone | blockers reduce dominance/collapse readiness | mechanism diagnostic only |
| `relation_ready_bonus` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | certificate score, ready flag, quotient resolution | rewards, hidden state | stronger certificate readiness increases readout support | mechanism diagnostic only |
| `certificate_gate_open` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy | certificate ready flag, recursion demand, blocker pressure, collapse/revision controls | reward optimality, hidden policy, action labels | unresolved recursion/blocker pressure closes dominance gate unless certificate is ready | architecture compliance diagnostic |
| `certificate_blocks_dominance` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy | non-ready certificate, recursion demand, blocker pressure, explicit blockers | weak competition alone, raw legal actions, best-action hints | non-ready certificate with active unresolved structure blocks dominance-style collapse | architecture compliance diagnostic |
| `dominance_score` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | support, stability, field score, certificate readiness, burden | family labels, hidden values | support/resolution increase; burden/blockers decrease; dominance remains gated by certificate status | not final paper proof |
| `sampling_score` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | sampling, uncertainty, burden, recursion, blockers | hidden policy/value | unresolved/uncertain/recursive pressure increases reopening | not final paper proof |
| `continuation_score` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | support, stability, viability, certificate readiness, burden | hidden policy/value | stable lower-burden continuation preferred after non-dominance | not final paper proof |

All entries above remain barred from strong performance/novelty claims until their constants are either derived, frozen with ablation, or explicitly treated as global implementation parameters.

---

## 10. Real-trace validation formula watchpoints — 2026-05-06

`structural_trace_validation_v1` detected active weighted formulas across adapters and runtime surfaces.  This is not automatically a defect, but it keeps the current implementation below final paper-algorithm status.

### 10.1 Adapter public-effect magnitudes

| Field / formula area | Code path | Current status | Required grounding before paper use |
|---|---|---|---|
| bandit uncertainty / sampling public effects | `agents/co/adapters/bandit_adapter.py` | provisional-global-proxy | show magnitude is public-history uncertainty grammar, not best-arm policy |
| maintenance degradation / hiddenness / reset effects | `agents/co/adapters/maintenance_replacement_adapter.py` | provisional-global-proxy | show magnitudes use public degradation/cost/visibility only, not hidden health policy |
| maze topology / obstruction / local-reach effects | `agents/co/adapters/maze_adapter.py` | provisional-global-proxy | show magnitudes are visible topology grammar and not hidden shortest-path guidance |
| renewal phase / cycle effects | `agents/co/adapters/renewal_adapter.py` | provisional-global-proxy | show phase burden uses public recurrence position and not oracle timing |
| latent-mechanism hiddenness / affordance effects | `agents/co/adapters/latent_mechanism_adapter.py` | investigatory/provisional | show hiddenness/effect magnitudes are public/declared problem grammar, not latent-solver hints |

### 10.2 Trace-validation status

The current structural trace validation after carrier alignment and certificate-gate review found:

```json
{
  "relations_total": 80,
  "structural_relations": 16,
  "weak_decision_competition_relations": 64,
  "branch_internal_operation_rows": 20,
  "field_delta_positive_cases": 5,
  "commitment_changed_cases": 1,
  "cases_with_watchpoints": 0
}
```

This implies:

- relation topology and branch-internal burden operations can affect field/certificate state;
- weak competition remains common but is non-blocking procedural telemetry;
- distributed field deltas without action change may be valid stability cases when no single branch delta crosses the manual-review threshold;
- a non-ready certificate with high recursion/blocker pressure must block dominance-style earned collapse;
- constants remain mechanism-diagnostic only.

### 10.3 Paper claim restriction

Until formula entries are complete and ablations are run, active formulas may support only this claim:

```text
The implementation is a traceable provisional realization of the documented CO kernel architecture.
```

They may not yet support this claim:

```text
The implementation is the final derived algorithmic form of CO.
```

---

## 2026-05-06 target-state formula status update

This protocol is now bound to `100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md` and `96_CONCEPTUAL_CLOSURE_LEDGER.md`.

The target state is:

```text
No scalar field may affect evidence-bearing readout unless it has a ledger entry stating:
- what richer structure it compresses;
- which inputs are allowed;
- why signs/weights have their current direction;
- whether coefficients are conceptual, empirical, provisional, or inactive;
- whether they were fixed before evaluation;
- which diagnostics constrain them;
- what claim boundary they support.
```

Until this ledger is complete, formulas may remain active for architecture validation, but the implementation must be described as provisional and traceable, not as a final derived algorithm.

---

## 11. Real-adapter ablation formula status update — 2026-05-16

`real_adapter_structural_ablation_review_v1` confirms that several provisional
readout formulas are behavior-affecting on real adapter sweeps, not only on
microcases.

Key structural result:

```json
{
  "cases": 311,
  "no_public_effects_action_changes": 76,
  "no_public_effects_mode_changes": 28,
  "no_resolver_ops_action_changes": 71,
  "branch_internal_only_unique_scope_action_changes": 19,
  "no_weak_competition_action_changes": 0,
  "certificate_aware_reopen_changes_when_resolvers_removed": 66
}
```

### 11.1 Behavior-affecting formulas now requiring priority ledger entries

| Field / formula | Code path | Status class | Richer structure compressed | Current constraint evidence | Remaining gap |
|---|---|---|---|---|---|
| `resolver_support >= 0.08` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | whether a candidate publicly exposes, reduces, cancels, or buffers unresolved burden; transform/transfer pressure is tracked separately and is not resolver support without explicit resolution | removing resolver ops changes 71/311 actions and 66 certificate-aware reopen decisions | threshold magnitude not derived; resolver_formula_grounding_audit_v1 now constrains action-name independence and transform/nonresolver separation |
| `sampling_gate_margin` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy with provisional constants | how much sampling-score advantage a blocked carrier-only branch may retain before an unblocked resolver is treated as comparable | prevents carrier-only burden from winning over comparable public resolvers; real review has 0 unresolved watchpoints | constants are bounded but not derived from first principles |
| `sampling_support_advantage_limit` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy with provisional constants | how much raw support advantage allows continuation through unresolved carrier pressure during reopen/sample | prevents weak resolver from defeating overwhelmingly stronger blocked branch | threshold must be swept for over-timidity / over-permissiveness |
| `continuation_gate_margin` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy with provisional constants | comparability of unblocked stable continuation vs blocked stable continuation | microcases pass; real sweep currently triggers through reopen/sample rather than stable continuation | may remain mostly latent unless real states hit stable-continuation fork |
| `support_advantage_limit` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy with provisional constants | overwhelming-support exception for continuation under unresolved burden | keeps a blocked branch selectable only when unblocked alternative is too weak | magnitude not grounded; must remain provisional |
| `blocker_pressure` construction for gates | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | certificate blockers, recursion demand, carrier-only pressure, gate closure | removal of public effects changes selected-blocked status in 42/311 cases | component weights not fully justified |
| branch-internal resolver/carrier magnitudes | adapters + `relation_surface` + RCF/certificate | provisional-global-proxy | public burden-operation grammar from adapter facts | removing public effects removes branch-internal rows in 311/311 cases | adapter-specific magnitude grammar needs family-by-family ledger |

### 11.2 Current claim boundary after ablation

The implementation may now support this limited structural claim:

```text
In the current maintenance/latent/standard public-observation sweeps, public
burden/effect facts and resolver operations causally change CO commitment traces,
while weak decision-slot competition alone does not.
```

It still may not support:

```text
- reward-performance claims;
- final formula derivation claims;
- RCF novelty claims;
- broad empirical evidence claims.
```

### 11.3 Required next work

Before empirical studies are interpreted, the fields listed in §11.1 need either:

```text
1. completed ledger entries with signs/weights/inputs justified;
2. sensitivity sweeps showing robust qualitative behavior over reasonable ranges;
3. explicit classification as provisional global implementation parameters.
```



---

## 11. Formula sensitivity probe — 2026-05-16

`real_adapter_formula_sensitivity_probe_v1` perturbed the certificate-aware stable-continuation and resolver-aware reopen/sample coefficients across the current 311-case real-adapter public-observation sweep.

Summary:

```json
{
  "cases": 311,
  "baseline_certificate_aware_reopen_cases": 66,
  "baseline_certificate_aware_stable_cases": 0,
  "zero_comparability_margins_action_changes": 5,
  "resolver_threshold_nearly_disabled_action_changes": 66,
  "flat_blocker_terms_action_changes": 1
}
```

Interpretation boundary:

- resolver recognition is behavior-causal and therefore high-priority for grounding;
- moderate comparability-margin variation did not change real-sweep actions, but zeroing margins did change 5 actions, so the gate is active and cannot remain undocumented;
- blocker-pressure widening terms changed one real-sweep action and remain provisional pending targeted blocker-pressure probes;
- no result is reward evidence or parameter tuning evidence.

### 11.1 Active readout-coefficient ledger entries

| Coefficient / formula | Code path | Status class | Allowed inputs | Monotonic commitment | Sensitivity status | Paper claim allowed |
|---|---|---|---|---|---|---|
| `resolver_support_threshold` | `commitment_surface._canonical_commitment_choice` | canonical-constrained-proxy / constant provisional | branch-internal resolver support derived from public effects/certificates | higher threshold makes resolver alternatives harder to recognize | high causal importance: near-disable changes 66/311 actions | structural diagnostic only |
| `sampling_gate_margin_*` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | blocker pressure, revision, nonlocal authority, rivalry, collapse/local authority | larger margin permits resolver alternatives across wider sampling-score gaps | active: zero margins change 5/311 actions; moderate sweeps inert | structural diagnostic only |
| `sampling_support_advantage_*` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | same as sampling gate plus selected-vs-alternative support gap | larger limit lets resolver alternative beat stronger blocked carrier branch | active with sampling gate; exact split not yet isolated | structural diagnostic only |
| `continuation_gate_margin_*` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | blocker pressure, revision, rivalry, nonlocal authority, collapse/local authority | larger margin prefers unblocked continuation across wider continuation-score gaps | active in microcases; inert in current real sweep | structural diagnostic only |
| `support_advantage_limit_*` | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | same as continuation gate plus selected-vs-alternative support gap | larger limit lets unblocked continuation beat stronger blocked branch | active in microcases; inert in current real sweep | structural diagnostic only |
| blocker-pressure widening weights | `commitment_surface._canonical_commitment_choice` | provisional-global-proxy | certificate blocker pressure / recursion / gate closure / carrier pressure | stronger blocker pressure widens unblocked-alternative authority | weakly active: flat terms change 1/311 actions | structural diagnostic only |

Required next ledger work:

1. isolate `sampling_gate_margin` from `sampling_support_advantage_limit` in targeted microcases;
2. isolate `continuation_gate_margin` from `support_advantage_limit` in continuation microcases;
3. justify the resolver threshold as a minimal recognizability condition rather than a performance knob;
4. record all default constants as frozen structural defaults before empirical runs.

---

## 11. Resolver-threshold grounding update — 2026-05-16

`resolver_formula_grounding_audit_v1` showed that resolver recognition is one of the main behavior-causal levers in the current runtime.  A follow-up threshold microcase found that a flat base threshold was too permissive: a minimal resolver fact at the old floor could displace a much larger carrier-only burden as soon as it crossed `0.08`.

The certified readout now separates two questions:

```text
Is this public effect a resolver operation at all?
Is it adequate to the unresolved burden it is being used to reopen?
```

Current rule in `CommitmentSurface`:

```text
required_resolver_support = max(
    resolver_support_threshold,
    min(
        resolver_support_scaled_cap,
        resolver_support_scaled_base
        + resolver_support_carrier_weight * selected_blocked_branch.carrier_only_pressure
        + resolver_support_blocker_weight * selected_blocked_branch.blocker_pressure
    )
)
```

Default constants remain provisional global proxies:

| Constant | Default | Status | Meaning |
|---|---:|---|---|
| `resolver_support_threshold` | `0.08` | provisional-global-proxy | noise floor for recognizing non-trivial resolver evidence |
| `resolver_support_scaled_base` | `0.08` | provisional-global-proxy | base adequacy before scaling by selected blocked branch burden |
| `resolver_support_carrier_weight` | `0.12` | provisional-global-proxy | makes stronger carried burden require stronger resolver support |
| `resolver_support_blocker_weight` | `0.05` | provisional-global-proxy | makes certificate/blocker pressure require stronger resolver support |
| `resolver_support_scaled_cap` | `0.32` | provisional-global-proxy | prevents adequacy scaling from becoming a hard veto against resolvers |

Monotonic commitments:

- resolver support must come only from explicit reduce/relieve/prevent, reset/cancel, reveal/expose/reduce_hiddenness, or buffer/absorb public effects;
- transform/transfer pressure is not resolver support by itself;
- a weak resolver may be recorded but should not displace a heavily burdened blocked branch merely because it crossed the base floor;
- higher carrier-only pressure and higher blocker pressure should weakly raise required resolver adequacy;
- strong public resolver evidence should still displace comparable blocked carrier-only branches.

Diagnostics constraining this rule:

```text
resolver_threshold_microcase_probe_v1
resolver_formula_grounding_audit_v1
real_adapter_formula_sensitivity_probe_v1
real_adapter_certificate_gating_review_v1
```

Current microcase result:

```text
0.079 resolver support: no switch under high carrier pressure
0.08 resolver support: no switch under high carrier pressure
0.35 resolver support: switch under high carrier pressure
transform/transfer only: no resolver switch
reduce/expose/cancel/buffer: resolver switch when adequate
```

This is still not a final derivation.  The rule is a constrained proxy that blocks an identified structural error while preserving auditability.  It cannot support reward or novelty claims until the constants above are either further derived or frozen with ablation evidence.
