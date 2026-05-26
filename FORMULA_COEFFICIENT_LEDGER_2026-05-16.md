# Formula / Coefficient Ledger — 2026-05-16

Status: **provisional structural grounding ledger**.

This ledger records behavior-affecting constants in the current frozen baseline. It does not make performance claims. A constant marked `provisional-structural` is allowed for controlled validation only because it has a structural role and at least one diagnostic constraint; it is not a final derivation.

## Ledger discipline

For each coefficient, the required interpretation is:

- richer structure compressed;
- sign justification;
- magnitude status;
- constraining diagnostic;
- failure condition.

## CommitmentSurface formula parameters

| Parameter | Default | Status | Richer structure compressed | Sign / role | Current diagnostic constraint | Failure condition |
|---|---:|---|---|---|---|---|
| `resolver_support_threshold` | 0.08 | provisional-structural | non-trivial public resolver evidence | lower values admit noise-level resolver facts; higher values suppress exposure/relief/cancellation | `resolver_formula_grounding_audit_v1`; `resolver_threshold_microcase_probe_v1`; sensitivity near-disable changes 66/311 real actions | resolver at/noise floor displaces high burden, or real resolver alternatives become inert |
| `resolver_support_scaled_base` | 0.08 | provisional-structural | minimum burden-adequacy requirement before scaling | prevents flat threshold from authorizing weak resolvers against large carried burden | threshold microcases: 0.08 no longer displaces high carrier pressure | flat floor again behaves as magic action preference |
| `resolver_support_carrier_weight` | 0.12 | provisional-structural | adequacy scaling by selected branch carrier-only pressure | stronger carried burden requires stronger resolver support | threshold sweep first-switch curve rises with carrier pressure | weak resolver defeats high carrier burden, or no resolver can ever clear carrier burden |
| `resolver_support_blocker_weight` | 0.05 | provisional-structural | adequacy scaling by certificate/blocker pressure | stronger blocker pressure requires stronger resolver support | threshold microcases and real certificate review | blocker-heavy branches are cleared by tiny resolver facts |
| `resolver_support_scaled_cap` | 0.32 | provisional-structural | upper bound preventing adequacy from becoming hard veto | caps required resolver support so high-burden states remain resolvable | threshold sweep: strong resolvers clear high carrier pressure | cap makes resolver adequacy either impossible or too permissive |
| `sampling_gate_margin_floor` | 0.05 | provisional-structural | minimal comparability in reopen/sample score | avoids zero-margin brittleness | formula sensitivity: zero margins change 5/311 actions | tiny score jitter switches decisions unpredictably |
| `sampling_gate_margin_base` | 0.055 | provisional-structural | default resolver comparability after blocked sample | base permission for comparable resolver alternatives | real certificate review: 66 resolver-aware switches, 0 watchpoints | carrier-only blocked branch wins over comparable resolver |
| `sampling_gate_margin_cap` | 0.18 | provisional-structural | maximum sampling-score comparability window | prevents weak resolver from defeating much stronger sample pressure | resolver threshold microcases; formula sensitivity | unblocked resolver wins when not materially comparable |
| `sampling_gate_margin_blocker_weight` | 0.070 | provisional-structural | unresolved blocker pressure | more blocker pressure widens resolver authority | real certificate review and sensitivity profiles | blocker pressure has no effect on resolver authority |
| `sampling_gate_margin_revision_weight` | 0.030 | provisional-structural | revision permissibility | more revision allows reopening toward resolver | formula sensitivity profile | revision regime does not affect reopening authority |
| `sampling_gate_margin_nonlocal_weight` | 0.025 | provisional-structural | nonlocal authority / hidden structure relevance | hidden/nonlocal regimes widen resolver comparability | real adapter sweep includes hidden maintenance/latent cases | nonlocal regimes behave same as fully local regimes |
| `sampling_gate_margin_rival_weight` | 0.020 | provisional-structural | rivalry breadth | broader rivalry permits more reopening | ablation review | rivalry has no effect or acts like weak decision-slot competition |
| `sampling_gate_margin_collapse_narrowing` | 0.020 | provisional-structural | collapse admissibility | stronger collapse permission narrows reopening | formula sensitivity profile | collapse regime cannot stabilize readout |
| `sampling_gate_margin_local_narrowing` | 0.015 | provisional-structural | local authority | local authority narrows resolver reopening | formula sensitivity profile | local evidence cannot stabilize readout |
| `sampling_support_advantage_floor` | 0.10 | provisional-structural | minimum allowed support advantage for comparable resolver | avoids support-gap zero brittleness | formula sensitivity | tiny support differences dominate structural blockers |
| `sampling_support_advantage_base` | 0.13 | provisional-structural | default raw support comparability | compares blocked sample support vs resolver alternative | real certificate review: no unresolved resolver watchpoints | support gap ignored or over-authoritative |
| `sampling_support_advantage_cap` | 0.30 | provisional-structural | maximum support-gap exception | lets overwhelmingly stronger blocked branch continue | resolver threshold controls | weak resolver beats overwhelmingly stronger blocked branch |
| `sampling_support_advantage_blocker_weight` | 0.070 | provisional-structural | blocker pressure in support comparability | higher blocker pressure makes stronger support gap still comparable | real review, sensitivity | blocker status never affects support-gap judgment |
| `sampling_support_advantage_revision_weight` | 0.030 | provisional-structural | revision permissibility in support comparability | revision allows stronger resolver intervention | sensitivity profile | revision has no structural effect |
| `sampling_support_advantage_nonlocal_weight` | 0.020 | provisional-structural | nonlocal/hidden regime comparability | nonlocal regimes tolerate wider resolver intervention | real hidden sweeps | hidden regimes behave as local score cases |
| `sampling_support_advantage_collapse_narrowing` | 0.020 | provisional-structural | collapse admissibility narrowing | collapse permission protects strong local support | sensitivity profile | collapse regime cannot stabilize |
| `sampling_support_advantage_local_narrowing` | 0.015 | provisional-structural | local authority narrowing | local authority protects strong local support | sensitivity profile | local support is ignored |
| `continuation_gate_margin_floor` | 0.04 | provisional-structural | minimal comparability for stable continuation alternative | avoids zero-margin brittleness | structural continuation microcases | blocked stable branch wins despite comparable unblocked alternative |
| `continuation_gate_margin_base` | 0.045 | provisional-structural | default continuation comparability | lets comparable unblocked alternatives beat blocked stable continuation | continuation microcases; real sweep currently mostly bypassed by reopen/sample | stable continuation reduces to argmax after dominance failure |
| `continuation_gate_margin_cap` | 0.16 | provisional-structural | maximum continuation-score comparability | preserves continuation through burden when branch is materially stronger | overwhelming-support control | over-timid switching to weak alternatives |
| `continuation_gate_margin_blocker_weight` | 0.065 | provisional-structural | blocker pressure | more unresolved blocker pressure widens unblocked alternative authority | continuation microcases | blockers do not alter stable continuation |
| `continuation_gate_margin_revision_weight` | 0.030 | provisional-structural | revision permissibility | higher revision widens continuation switching | continuation microcases | revision regime inert |
| `continuation_gate_margin_rival_weight` | 0.020 | provisional-structural | rivalry breadth | rivalry widens unblocked alternative authority | ablation review | strong rivalry behaves like weak slot competition |
| `continuation_gate_margin_nonlocal_weight` | 0.020 | provisional-structural | nonlocal authority | hidden/nonlocal regimes widen unblocked alternative authority | microcases | hiddenness has no continuation effect |
| `continuation_gate_margin_collapse_narrowing` | 0.025 | provisional-structural | collapse admissibility | collapse permission narrows continuation switching | microcases | collapse readiness cannot stabilize |
| `continuation_gate_margin_local_narrowing` | 0.020 | provisional-structural | local authority | local authority narrows switching | microcases | local support cannot preserve continuation |
| `support_advantage_limit_floor` | 0.12 | provisional-structural | minimum raw support comparability in stable continuation | prevents tiny differences from deciding unresolved burden | continuation microcases | blocked branch wins by tiny support edge despite unblocked alternative |
| `support_advantage_limit_base` | 0.16 | provisional-structural | default support-gap allowance | separates comparable alternative from overwhelming support exception | continuation microcases | no meaningful exception boundary |
| `support_advantage_limit_cap` | 0.28 | provisional-structural | maximum support-gap allowance | allows continuation under burden when support is overwhelmingly stronger | overwhelming-support control | system always chooses safety/probe branch |
| `support_advantage_limit_blocker_weight` | 0.08 | provisional-structural | blocker pressure in support-gap comparison | stronger blocker pressure permits wider alternative comparison | continuation microcases | blocker pressure invisible |
| `support_advantage_limit_revision_weight` | 0.03 | provisional-structural | revision permissibility | higher revision widens alternative authority | continuation microcases | revision inert |
| `support_advantage_limit_nonlocal_weight` | 0.02 | provisional-structural | nonlocal authority | hidden/nonlocal regimes widen alternative authority | continuation microcases | nonlocality inert |
| `support_advantage_limit_collapse_narrowing` | 0.03 | provisional-structural | collapse admissibility | collapse readiness narrows alternative authority | continuation microcases | collapse readiness irrelevant |
| `support_advantage_limit_local_narrowing` | 0.02 | provisional-structural | local authority | local authority protects local continuation | continuation microcases | local authority cannot stabilize |

## Non-overridable readout formula groups still needing deeper derivation

These are not exposed as `commitment_formula_params` but affect behavior and therefore remain ledger obligations:

| Formula group | Current status | Required next grounding |
|---|---|---|
| `local_weight`, `stability_weight`, `burden_weight`, `sampling_weight` | provisional structural mix of direct controls | Derive weight signs from six-question regime basis and test via controlled direct-control sweeps. |
| `dominance_margin` | provisional structural margin | Isolate rivalry/revision/nonlocal/collapse/local terms in dominance microcases. |
| `burden_alarm` | provisional structural alarm | Test burden/revision/nonlocal sensitivity separately from resolver support. |
| `support`, `burden`, `stability` composite scores | provisional thin collapses | Map each score to richer row/field/certificate components and prove no component is an action-name proxy. |
| `dominance_score`, `sampling_score`, `continuation_score` | provisional readout surfaces | Ablate each component and verify mode changes for structural reasons. |

## Current stage judgment

The coefficient situation is now acceptable for **small frozen empirical sanity tests only**, not for performance claims. Constants must remain frozen during those tests. Any empirical result obtained after changing constants is invalid as evidence for this baseline.

## Added watchpoint: pre-blocking resolver timing — 2026-05-17

`mid_regime_repair_timing_probe_v1` exposes a coefficient/formula gap not covered by the existing resolver-aware blocked-branch rule.  The current resolver adequacy law applies when a selected carrier branch is already certificate-blocked.  In middle maintenance at public observed health 2, RUN can carry high degradation pressure while not crossing the formal block threshold; `reopen_or_sample` can then select RUN even when REPAIR has adequate public resolver support.

This introduces a future ledger item, not yet implemented:

| Item | Status | Structure compressed | Required grounding before implementation |
|---|---|---|---|
| pre-blocking resolver timing pressure | open / not implemented | degree to which high carrier-only burden plus consequence span should authorize a resolver before formal certificate blocking | must distinguish lawful repair timing from hidden threshold policy; must be constrained by mid-regime repair-timing microcases, real-family traces, and no post-result tuning |

Any future parameterization must preserve the existing distinction between:

```text
RUN through manageable burden
vs.
REPAIR because carried degradation has become continuation-relevant enough that resolver preference is earned
```

## 2026-05-17 update: shape-gauged pre-blocking resolver timing

The mid-regime repair-timing probe exposed that the prior resolver law acted mostly after formal certificate blocking.  The new correction is explicitly **shape-gauged** and applies across resolver operations, not only maintenance repair.

Doctrine:

```text
A resolver branch may bend commitment before the carrier branch is formally blocked only when:
1. the selected branch carries sufficient carrier-only burden;
2. the resolver branch has explicit public resolver support;
3. the current problem shape/direct-control gauge makes delay/revision/nonlocal consequence urgent enough;
4. the support/score gap remains within the local gauge;
5. transform/transfer alone are not counted as resolution.
```

This is a current-step local shape-gauge update, not a topology edit and not a hidden policy.  The base six-question problem shape remains the prior; current public branch pressure updates the gauge for the commitment calculation only.

New formula parameters introduced in `CommitmentSurface`:

| Parameter | Default | Status | Richer structure compressed | Sign / role | Current diagnostic constraint | Failure condition |
|---|---:|---|---|---|---|---|
| `preblocking_carrier_pressure_floor` | 0.42 | provisional-structural | minimum carried-burden pressure before pre-blocking timing may activate | prevents resolver bonus under light manageable burden | `shape_gauged_resolver_timing_probe_v1`; `mid_regime_repair_timing_probe_v1` | low-burden carriers are displaced by resolvers |
| `preblocking_carrier_pressure_base` | 0.70 | provisional-structural | high default pressure required absent urgent shape | makes low-urgency regimes preserve continuation | shape probe low-urgency cases keep carrier | low-urgency shape still forces resolver |
| `preblocking_carrier_shape_urgency_weight` | 0.37 | provisional-structural | shape urgency lowering the pressure threshold | urgent shapes permit earlier resolution while preserving low-urgency / weak-resolver / large-carrier-advantage negative controls | `preblocking_resolver_cross_family_microcase_probe_v1`; `dominance_readout_swamping_audit_v1` | shape has no effect on resolver timing, or loosening causes low-urgency/weak-resolver over-resolution |
| `preblocking_carrier_pressure_cap` | 0.72 | provisional-structural | upper bound on carrier-pressure requirement | prevents required pressure from exceeding visible scale | synthetic pressure sweeps | resolver timing impossible under high burden |
| `preblocking_resolver_support_floor` | 0.10 | provisional-structural | minimum non-noise resolver capacity | rejects tiny resolver facts | resolver threshold probes | weak/noise resolver displaces carrier |
| `preblocking_resolver_support_base` | 0.12 | provisional-structural | default resolver adequacy before pressure/shape scaling | base adequacy floor | shape/mid probes | resolver support threshold becomes arbitrary |
| `preblocking_resolver_carrier_weight` | 0.18 | provisional-structural | stronger carrier pressure requires stronger resolver support | prevents weak resolver clearing high burden | resolver threshold + mid timing probes | tiny resolver clears heavy carrier burden |
| `preblocking_resolver_shape_weight` | 0.10 | provisional-structural | urgent shape raises required resolver adequacy while permitting earlier timing | urgent regimes need real resolver capacity, not mere label | shape-gauged probe | urgent shape becomes universal resolver bonus |
| `preblocking_resolver_support_cap` | 0.46 | provisional-structural | upper bound on required resolver support | keeps high-burden states resolvable | mid synthetic matrix | no resolver can satisfy high-burden adequacy |
| `preblocking_score_margin_floor` | 0.05 | provisional-structural | minimal score comparability for pre-blocking resolver | avoids zero-margin brittleness | shape/mid probes | numerical jitter changes switches |
| `preblocking_score_margin_base` | 0.055 | provisional-structural | default score comparability | permits resolver only when score gap is not overwhelming | shape/mid probes | resolver defeats non-comparable carrier |
| `preblocking_score_margin_pressure_weight` | 0.08 | provisional-structural | carrier pressure widening score comparability | higher burden permits earlier resolver timing | mid synthetic matrix | pressure does not affect timing |
| `preblocking_score_margin_shape_weight` | 0.07 | provisional-structural | shape urgency widening score comparability | problem shape supplies the gauge | shape probe high vs low urgency | shape inert or action-specific |
| `preblocking_score_margin_revision_weight` | 0.03 | provisional-structural | revision permissibility | more revision allows resolver bending | shape probe | revision has no effect |
| `preblocking_score_margin_collapse_narrowing` | 0.02 | provisional-structural | collapse admissibility narrowing | collapse/local regimes preserve carrier continuation | shape probe low urgency | low urgency still over-resolves |
| `preblocking_score_margin_local_narrowing` | 0.02 | provisional-structural | local authority narrowing | local evidence protects continuation | shape probe low urgency | local authority cannot stabilize |
| `preblocking_support_margin_floor` | 0.08 | provisional-structural | minimum support comparability | avoids raw support zero-margin brittleness | shape/mid probes | jitter changes resolver timing |
| `preblocking_support_margin_base` | 0.11 | provisional-structural | default support gap allowance | keeps resolver timing comparable | shape/mid probes | weak resolver beats overwhelming carrier support |
| `preblocking_support_margin_pressure_weight` | 0.07 | provisional-structural | carrier pressure widening support comparability | stronger burden can overcome larger local support gap | mid synthetic matrix | carrier pressure invisible |
| `preblocking_support_margin_shape_weight` | 0.06 | provisional-structural | shape urgency widening support comparability | problem shape updates timing gauge | shape probe | shape does not modulate |
| `preblocking_support_margin_nonlocal_weight` | 0.02 | provisional-structural | nonlocal authority | hidden/nonlocal regimes permit earlier resolution | shape probe | nonlocality inert |
| `preblocking_support_margin_local_narrowing` | 0.02 | provisional-structural | local authority narrowing | local regimes protect local continuation | shape probe | local regimes over-resolve |
| `preblocking_resolver_advantage_margin` | 0.03 | provisional-structural | margin for resolver timing pressure over continuation advantage | avoids equality/rounding switches | shape/mid probes | equal pressure flips erratically |

Diagnostics constraining this group:

```text
shape_gauged_resolver_timing_probe_v1:
  low urgency resolver switches = 0
  high urgency resolver switches = 4
  transform/transfer resolver switches = 0

mid_regime_repair_timing_probe_v1:
  high-risk RUN-through-burden cases = 0
  synthetic matrix still contains both RUN and REPAIR choices
```

Remaining warning: these constants are still provisional.  They are derived in law-form from relation + shape gauge, but their magnitudes are not final empirical constants.  They must remain frozen for any evidence-bearing run.

## 2026-05-21 DynamicShapeField first-pass formula ledger entries

The first-pass `DynamicShapeField` has been implemented in
`ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py` and validated
only through structural microcases/ablations.  These parameters are **not** final
empirical constants and must not be tuned from reward results.

| Parameter / formula group | Default / status | Structure compressed | Sign / role | Current diagnostic constraint | Failure condition |
|---|---:|---|---|---|---|
| `DynamicShapeField.alpha` | 0.35 / provisional-structural | retention rate for local shape-state update | bounded EMA from public trace; prevents one event from overwriting prior shape | `dynamic_shape_field_invariants`; microcase probe | shape overreacts to single trace or never changes |
| `relation_density_target` | first-pass formula / provisional | density of explicit branch relations and field relation counts | higher density narrows coarseness and widens rivalry/nonlocal controls | high-coupling microcase | relation topology has no shape effect |
| `burden_persistence_target` | first-pass formula / provisional | carried debt, burden trend, carry pressure, grey pressure, transform/transfer redirection | raises urgency and shortens projection when burden persists | carrier-burden microcase | persistent burden does not affect shape |
| `hiddenness_target` | first-pass formula / provisional | hiddenness pressure, uncertainty, exposure support | hiddenness raises sampling/nonclosure pressure; successful exposure reduces pressure | exposure success/failure microcases | hiddenness is invented or exposure has no effect |
| `admissibility_target` | first-pass formula / provisional | public legal narrowing/widening and recursion/debt pressure | narrowing raises admissibility pressure and conservative projection | topology discovery and failed revision microcases | kernel edits topology or ignores public blocked transitions |
| `projection_target` | first-pass formula / provisional | projection horizon under coupling, burden persistence, hiddenness, admissibility | high coupling/burden shortens projection; stable low pressure permits longer projection | carrier-burden and high-coupling microcases | projection grows under unresolved high burden |
| `coarseness_target` | first-pass formula / provisional | local collapse/coarsening permission under low coupling vs dense/high hiddenness | stable low coupling widens coarseness; high coupling narrows | stable/ high-coupling microcases | coarseness ignores relation/burden/hiddenness |
| `gauge_confidence_target` | first-pass formula / provisional | transportability confidence of current comparison gauge | successful exposure and low hiddenness increase confidence; redirect/hiddenness decrease | exposure and transform microcases | gauge confidence becomes reward-confidence proxy |
| `effective_controls` deformation | first-pass formula / provisional | dynamic shape-state interpreted as next-cycle gauge | urgency raises path/nonlocal/revision/rival pressure; coarsening/local confidence protects collapse/locality | real-trace ablation | DynamicShapeField either directly chooses actions or has no visible ablation |

Boundary:

```text
DynamicShapeField may modulate next-cycle controls from public retained trace.
It may not select native actions, inspect action names, use hidden state, use
reward alone, consume DP/baseline values, or edit topology/action domains.
```

Required next work:

```text
- run static-vs-dynamic ablations across all current problem families;
- add sensitivity probes for DynamicShapeField alpha and effective-control deformation;
- classify which formula parts are conceptual necessities vs implementation approximations;
- keep defaults frozen before any dynamic-shape empirical comparison.
```


## 2026-05-21 Quotient / equivalence first-pass formula ledger entries

The first-pass quotient helper has been implemented in
`ChangeOntCode/agents/co/runtime/surfaces/quotient_equivalence.py`.  It is a
structural approximation of doc `97`, not a final equivalence tolerance and not
a benchmark-tuned state abstraction.

| Parameter / formula group | Default / status | Structure compressed | Sign / role | Current diagnostic constraint | Failure condition |
|---|---:|---|---|---|---|
| `quotient_operation_family` | fixed public operation-family map / provisional-structural | burden-operation aliases such as carry/increase/amplify or reduce/relieve/prevent | permits different expressions with the same continuation role to quotient without action-name rules | `quotient_equivalence_first_pass_invariants` | aliases fail to quotient or unrelated operations quotient |
| `quotient_magnitude_band` | first-pass coarse bands / provisional-structural | residual magnitude under generic gauge/coarseness | absorbs harmless jitter while preserving low/medium/high/critical burden-regime differences | same-expression different-regime invariant | same scalar/action or different burden regime quotients |
| `quotient_profile_signature` | exact equality of public residual-profile entries / conservative | burden domain, kind, operation family, scope, band, threshold, basin, coupling | quotient only when remaining public differences do not alter active continuation structure under current gauge | public residual-profile probe | scalar score similarity or weak competition becomes quotient |
| `quotient_coarseness_adjustment` | small generic band widening from `coarseness_radius` / provisional | gauge-conditioned local coarseness | allows coarser profiles only through generic dynamic shape state, not problem family | helper source invariant + microcases | coarseness becomes family/action policy |

Boundary:

```text
Quotient/equivalence may use accepted public residual profiles only.
It may not use native action labels, hidden state, reward hindsight, baseline/DP
values, weak decision-slot competition, or family-specific thresholds.
```

Required next work:

```text
- run real-trace false quotient and missed quotient audits;
- compare against ordinary state abstraction / bisimulation-style reductions;
- test quotient behavior under dynamic shape/coarseness ablation;
- keep quotient defaults frozen before any evidence-bearing empirical comparison.
```


## 2026-05-21 recursion scheduler first-pass coefficients

Status: first-pass structural approximation; not final derivation and not performance-tuned.

File: `ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py`

Behavior-affecting quantities:

```text
scheduler_gain composition from path_sensitivity, revision_permissibility,
nonlocal_authority, rival_breadth, and contradiction/consequence sensitivity;

raw demand weights for unresolved_relation, sparse_high_consequence,
field_grey, hidden_pressure, field_debt, threshold pressure, and
non_equivalent_density;

quotient_pressure and resolver_relief subtraction weights;

mode thresholds: 0.42 preserve/monitor, 0.62 request unfolding layer;
budget thresholds: 0.42, 0.66, 0.82.
```

Justification status:

```text
These values are not derived final constants. They encode the target-state rule
that recursion demand rises when another layer could change burden, relation,
quotient, grey, hiddenness, or collapse status, and falls when equivalence or
resolution contracts the field. They require sensitivity probes and real-trace
calibration before any evidence-bearing claim.
```

## 2026-05-22 audit additions: quotient provenance and maintenance readout swamping

The quotient accept/reject audit adds no new behavior-affecting quotient coefficients. It adds provenance logging for accepted/rejected public residual profiles so false/missed quotient analysis can be performed before any tolerance change.

The maintenance action-insensitivity audit adds no maintenance-specific coefficients. It identifies the next formula-grounding target as generic readout dominance / pre-blocking resolver timing. Any future adjustment must be justified across families and microcases, not by maintenance reward improvement.

## 2026-05-22 update: generic carrier-gate calibration

The dominance/readout-swamping audit exposed that the pre-blocking resolver path could fail before resolver comparison in high-urgency borderline carrier cases.  The calibration is generic: `preblocking_carrier_shape_urgency_weight` was moved from `0.34` to `0.37`, increasing the ability of public shape urgency to lower the carrier-pressure gate.

Guardrails preserved by the cross-family microcase probe:

```text
low-urgency carrier remains protected
weak resolver remains protected
large carrier advantage remains protected
no family names or action-name rules are used
```

The calibration did not resolve maintenance action-prefix insensitivity in the capped diagnostic; first-pass sequence composition now exists, but this remains a readout/sequence-consumption watchpoint rather than a license for family-specific repair timing.


## 2026-05-22 — Sequence-composition first-pass coefficients

Status: provisional structural coefficients, not empirically tuned and not publication-grounded.

Implemented in `ChangeOntCode/agents/co/runtime/surfaces/sequence_composition.py`:

- phase thresholds: exposure/relief/carry/transfer/stabilize thresholds around 0.18–0.34;
- domain compatibility floors: exact domain = 1.0, same coupling/scope/relation-scope partial compatibility, exposure-to-relief/stabilize hiddenness bridge ≤ 0.58;
- transition support mixtures for carry→expose, carry→relieve, expose→relieve, relief/exposure→stabilize, continued relief;
- current-candidate topology attenuation = 0.62 relative to observed selected-feedback sequence;
- bounded sequence-to-existing-channel boosts through preventive support, resolver support, relief support, persistence, viability, stability, and decision state.

These numbers are first-pass operational approximations. They must be tested by sequence on/off diagnostics and negative controls. They must not be interpreted as derived constants or tuned evidence.
