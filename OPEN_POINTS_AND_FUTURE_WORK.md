# Open Points and Future Work

This file separates current-phase engineering/test work from later formal, empirical, and conceptual research. It should be updated whenever an open point is resolved, deferred, or promoted into the active target.

## 1. Current-phase implementation and validation tasks

These are appropriate next tasks after cold onboarding remains clean.

```text
- Re-run the full invariant suite after each behavior-affecting change. The 2026-05-15 full audit ran the current suite successfully; that does not remove the need to rerun it after edits.
- Re-run structural trace validation and relation-path trace after each behavior-affecting change.
- Maintain the shared adapter action-validation helper and source invariant added in the semantic relevance audit; extend it if new adapters are added.
- Complete targeted docstrings/comments for active boundary, adapter, placement, runtime, integration, and diagnostic functions without boilerplate.
- Maintain the current structural probes:
  - `structural_ablation_probe_v1.py` checks public-effect/relation ablations across sampled adapter rows.
  - `structural_microcase_probe_v1.py` checks targeted synthetic cases for weak competition, hiddenness/exposure, relief, cancellation, and quotient/equivalence.
- Maintain and interpret second-stage continuation-gating microcases:
  - `structural_continuation_gating_probe_v1.py` now protects certificate-aware stable continuation;
  - comparable unblocked alternatives should displace certificate-blocked continuations;
  - overwhelming-support blocked continuations may still continue under unresolved burden;
  - the new margins must be entered into the formula/coefficient ledger before empirical claims.
- Maintain and interpret real-adapter certificate-gating review:
  - `real_adapter_certificate_gating_review_v1.py` checks whether the certificate-aware readout law fires on real adapter rows;
  - current standard samples do not require stable-continuation redirection;
  - the sweep exposed and now protects resolver-aware reopen/sample redirection, so blocked carrier-only branches should not beat comparable unblocked resolver branches.
- Review manual traces across bandit, maintenance, maze, renewal, and latent mechanism.
- Keep adapter public-effect coverage honest and free of hidden policy conclusions.
- Keep CommitmentSurface as final readout and fail closed when CO evidence is absent.
```

## 2. Formula ledger / coefficient grounding

Current status: improved, incomplete.

For every behavior-affecting scalar, record:

```text
- what richer structure it compresses;
- why these inputs are included;
- why the signs are correct;
- why the weights are provisional, conceptual, empirical, or fixed;
- whether the scalar affects readout;
- what tests constrain it;
- what failure would force revision.
```

## 3. Quotient / equivalence tolerance

Current status: first-pass partial.

Implemented on 2026-05-21:

```text
- `quotient_equivalence.py` derives conservative equivalence from public residual profiles;
- relation_surface now delegates quotient derivation to that helper;
- quotient invariants reject same native expression alone, same scalar score alone, weak decision-slot competition, rivalry/exclusion-only facts, and hidden/solver-like facts;
- `quotient_equivalence_first_pass_probe_v1.py` records the structural probe.
```

Concept target:

```text
Branches quotient when remaining differences no longer alter active continuation
burden, admissibility, relation topology, recursion demand, or collapse consequence
under the current gauge.
```

Open work:

```text
- refine tolerance policy beyond first-pass coarse residual bands;
- measure false quotient and missed quotient behavior on real traces;
- calibrate by regime without post-hoc performance tuning;
- document reduction cases where quotienting becomes known abstraction machinery.
```

## 4. Recursion scheduler / budget

Current status: first-pass partial.

Implemented on 2026-05-21:

```text
- `recursion_scheduler.py` derives bounded public structural recursion demand;
- CandidateSurface wires it before CollapseCertificate;
- scheduler telemetry records demand, budget, mode, and reasons;
- ablation toggle can disable it for diagnostic maps.
```

Concept target:

```text
Recursion demand arises when another layer may change burden, relation, quotient,
grey, or collapse status.
```

Open work:

```text
- audit false-positive / false-negative demand on real traces;
- define actual second-layer unfolding expansion, if any;
- keep the scheduler distinct from search/lookahead in evidence-bearing runtime;
- calibrate coefficients before empirical claims.
```

## 5. Multi-step continuation identity / composition

Current status: first-pass partial.

Implemented on 2026-05-21:

```text
- continuation memory can derive from public burden-domain evidence;
- different native action expressions over the same public burden domain can share temporal memory;
- RelationSurface branch IDs remain distinct, so memory sharing does not merge current branches;
- native action/candidate fallback remains last resort only.
```

Open work:

```text
- evaluate first-pass sequence-level branch composition across different burden domains;
- model transitions such as exposure → relief → stable operation;
- connect continuation-memory groups to future quotient/equivalence without premature merge;
- test robot/simulation cases where one continuation must change action expression over time.
```

## 6. Empirical validation

Before evidence claims:

```text
- freeze constants;
- log seeds and JSONL;
- enforce budget parity;
- label oracle baselines explicitly;
- check translator boundary leakage;
- report regressions honestly;
- separate structural interpretation from reward performance.
```

Recommended order:

```text
1. structural checks
2. targeted ablations
3. family manual traces
4. limited preregistered family studies
5. broader baseline comparisons
```

## 7. Known-algorithm comparison

Before novelty claims, compare RCF behavior against:

```text
MCTS / tree search;
dynamic programming;
belief propagation / message passing;
active inference;
options;
successor representations;
state abstraction;
heuristic search;
constraint satisfaction / graph search.
```

Classify shared mechanisms, reduction cases, interpretation differences, and operational differences.

## 8. Later formal work

Later formal work includes:

```text
- fuller HAQ/gauge grounding;
- typed path algebra / semiring / quantale roles where earned;
- MDL/compressibility status;
- loopiness distinctions;
- creative option birth;
- dissociation cascade;
- stronger local comparability and metric/quotient derivations.
```

These are not automatic current-runtime claims.

## 9. Consciousness and meaning scope

Safe current bridge:

```text
meaning-like relevance = retained difference that changes continuation burden,
salience, admissibility, or collapse-readiness.
```

Not claimed:

```text
- consciousness solved;
- AI consciousness established;
- proto-conscious standing established;
- felt subjectivity derived from current kernel tests.
```

Later consciousness work requires a separate target theory, test protocol, and claim boundary.

## 10. Exploratory material rule

Exploratory files may remain only if their status is explicit and they do not override the active docs. If an exploratory idea becomes implementation-relevant, promote it through the normal chain:

```text
TheoryOfChange_main if conceptually necessary
→ kernel_spec target doc
→ code
→ diagnostics
→ onboarding/index updates
```

### Real-adapter ablation follow-up — 2026-05-16

`real_adapter_structural_ablation_review_v1` shows public effects are now
behavior-causal in the broad maintenance/latent/standard sweep:

```text
no_public_effects: 76 action changes / 311 cases
no_resolver_ops: 71 action changes / 311 cases
no_weak_competition: 0 action changes / 311 cases
```

This strengthens the need for formula-ledger work before empirical claims.  The
next open item is not another readout patch unless a watchpoint appears; it is
coefficient grounding and sensitivity review for resolver and gate margins.



### Formula/coefficient grounding — active priority

Current status after `real_adapter_formula_sensitivity_probe_v1`:

- `resolver_support_threshold` is behavior-causal: disabling resolver recognition changes 66/311 real-adapter actions after transform-only pressure was removed from resolver support.
- comparable-alternative margins are active but less fragile in the current real sweep: zeroing them changes 5/311 actions; moderate narrowing/widening changes none.
- blocker-pressure widening terms are weakly active in the real sweep: flat terms change 1/311 action.

Required before empirical reward claims:

1. complete ledger entries for all readout-affecting coefficients;
2. isolate sampling gate vs support-advantage limits in microcases;
3. isolate continuation gate vs support-advantage limits in microcases;
4. freeze defaults before any performance study;
5. forbid retuning these constants to repair family-level reward regressions.

### Resolver-threshold adequacy update — 2026-05-16

`resolver_threshold_microcase_probe_v1` found and closed a formula gap in resolver-aware `reopen_or_sample`: the old flat `0.08` resolver threshold was too permissive in controlled high-carrier cases.  `CommitmentSurface` now requires resolver support to be adequate to the selected blocked branch's carrier-only pressure and blocker pressure, not merely above a fixed noise floor.

Current protected behavior:

```text
0.079 resolver support: no switch under high carrier pressure
0.08 resolver support: no switch under high carrier pressure
0.35 resolver support: switch under high carrier pressure
transform / transfer only: no resolver switch
reduce / expose / cancel / buffer: resolver switch when adequate
```

Open work remains:

```text
- ground `resolver_support_carrier_weight`, `resolver_support_blocker_weight`, and `resolver_support_scaled_cap` more deeply;
- test whether the scaled adequacy law remains stable under broader real-family traces;
- ensure the adequacy law does not become a hidden conservative action policy;
- keep these constants frozen before any empirical reward study.
```

## 2026-05-16 stage-gate update

New baseline/testing artifacts:

- `STRUCTURAL_BASELINE_FREEZE_2026-05-16.md`
- `FORMULA_COEFFICIENT_LEDGER_2026-05-16.md`
- `research_reports/2026-05-16/SYSTEMATIC_MECHANISM_ABLATION_REVIEW_2026-05-16.md`
- `research_reports/2026-05-16/REAL_FAMILY_MANUAL_TRACE_REVIEW_REPORT_2026-05-16.md`
- `research_reports/2026-05-16/FROZEN_EMPIRICAL_SANITY_SMOKE_REPORT_2026-05-16.md`
- `research_reports/2026-05-16/STAGE_GATE_EXECUTION_REPORT_2026-05-16.md`

Status: the current structural baseline is frozen for controlled validation. A small empirical sanity smoke has executed, but it is not benchmark evidence. Remaining major open points are deeper derivation of non-overridable score-mixture constants, quotient/equivalence tolerance, recursion scheduling, multi-step continuation identity, and fair frozen benchmark comparisons.

## 2026-05-17 frozen logged empirical mini-suite

The first frozen logged empirical mini-suite has now executed:

- `research_reports/2026-05-17/FROZEN_LOGGED_EMPIRICAL_MINI_SUITE_REPORT_2026-05-17.md`
- `ChangeOntCode/experiments/studies/frozen_logged_empirical_mini_suite_v1.py`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/runs.jsonl`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/structural_telemetry.jsonl`
- `ChangeOntCode/outputs/frozen_logged_empirical_mini_suite_v1/summary.json`

Scope boundary: this is a smoke/telemetry mini-suite with explicit public baselines across all active families. It is not benchmark evidence, not tuning evidence, not CO proof, and not an RCF novelty claim.

Observed smoke status:

```text
runs = 23
co_runs = 7
baseline_runs = 16
families = bandit, renewal, maze, maintenance_replacement, latent_mechanism
structural_telemetry_records = 238
canonical_modes = dominance: 182, reopen_or_sample: 26, stable_continuation: 30
```

Next stage: use the focused maintenance mini-benchmark for trace-level failure analysis and only then decide whether broader frozen mini-benchmarks are justified.

## 2026-05-17 focused frozen empirical mini-benchmark

The first focused benchmark-shaped run has now executed on the maintenance/replacement family, where direct, partial, and hidden observation regimes exercise burden carrying, exposure, and resolver behavior.

- `research_reports/2026-05-17/FOCUSED_FROZEN_EMPIRICAL_MINI_BENCHMARK_REPORT_2026-05-17.md`
- `ChangeOntCode/experiments/studies/focused_frozen_empirical_mini_benchmark_v1.py`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/runs.jsonl`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/structural_telemetry.jsonl`
- `ChangeOntCode/outputs/focused_frozen_empirical_mini_benchmark_v1/summary.json`

Scope boundary: this is a small-N frozen mini-benchmark with explicit public baselines and no post-result tuning. It is not broad benchmark evidence, not CO proof, not novelty evidence, and not grounds for coefficient adjustment.

Observed preliminary status:

```text
runs = 27
co_runs = 9
baseline_runs = 18
family = maintenance_replacement
structural_telemetry_records = 720
canonical_modes = dominance: 360, reopen_or_sample: 3, stable_continuation: 357
CO vs best public baseline: bandit_like lower, middle lower, renewal_like higher
```

Interpretation: CO shows a promising preliminary signal only in the hidden/renewal-like regime and underperforms simple public baselines in direct/partial regimes. Treat this as a diagnostic result: the next work is failure analysis and trace comparison, not tuning.

## Mid-regime repair-timing watchpoint — 2026-05-17

`mid_regime_repair_timing_probe_v1` was added after the focused maintenance failure analysis.  It isolates the `observed_health = 2` middle-regime issue without tuning the kernel.

Current finding:

```text
Adapter-public sweep cases: 252
High-risk RUN-through-burden cases: 12
Synthetic pressure-matrix cases: 144
Synthetic REPAIR selections: 49
```

Interpretation:

- REPAIR is recognized as a public resolver when degradation pressure is present.
- Synthetic cases show the resolver path is not inert: sufficiently high carrier pressure plus adequate REPAIR visible support can switch to REPAIR.
- In adapter-public health-2 cases, however, RUN can still be selected by `reopen_or_sample` under high carrier-only pressure because the RUN branch is not formally certificate-blocked.

Open doctrine/formula question:

```text
Should adequate resolver preference require the carrier branch to already be certificate-blocked,
or should high carrier-only burden plus an adequate resolver create pre-blocking repair-timing pressure?
```

Do not tune this to match the threshold baseline.  The next correction, if any, must be framed as a readout-law/formula-grounding decision and then retested against structural probes and frozen empirical logs.

## 2026-05-17 shape-gauged resolver timing update

The earlier mid-regime repair-timing open point has been converted into a generic implementation and probe:

- `ChangeOntCode/experiments/studies/shape_gauged_resolver_timing_probe_v1.py`
- `research_reports/2026-05-17/SHAPE_GAUGED_RESOLVER_TIMING_PROBE_REPORT_2026-05-17.md`
- updated `mid_regime_repair_timing_probe_v1.py`

Current doctrine:

```text
branch relation alone is not enough;
problem shape supplies the gauge for when relation-mediated resolver pressure should matter now.
```

The implementation is not maintenance-specific and does not inspect native action names.  It uses carrier-only pressure, resolver support, direct controls derived from the six-question shape prior, and current public branch pressure to form a local shape gauge for the commitment step.

Still open:

- the new pre-blocking timing constants require deeper derivation and must remain frozen for empirical testing;
- real-family trace review should verify that the update does not create universal inspect/repair/sample bias;
- focused maintenance benchmark outputs generated before this update should not be compared as if they were current-baseline evidence.


## Dynamic shape / coarseness field

Status after 2026-05-21 first-pass implementation:

```text
- `_main` derivation exists: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md`.
- Contract/spec exists: `ChangeOntCode/docs/kernel_spec/103_DYNAMIC_SHAPE_FIELD_CONTRACT.md`.
- Microcase expectations exist: `ChangeOntCode/docs/kernel_spec/104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md`.
- Minimal runtime carrier now exists: `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py`.
- Structural microcase probe exists: `ChangeOntCode/experiments/studies/dynamic_shape_microcase_probe_v1.py`.
- Real-trace structural ablation exists: `ChangeOntCode/experiments/studies/dynamic_shape_real_trace_ablation_v1.py`.
```

Current boundary:

```text
This is first-pass implementation, not proof that dynamic shape improves reward,
not a final topology, and not evidence for CO novelty.
```

Remaining open work:

```text
- deepen formula-ledger grounding for DynamicShapeField update rates and effective-control deformation;
- test dynamic shape across all active problem families;
- check whether it changes behavior for structural reasons or only telemetry;
- evaluate static-shape-only vs dynamic-shape-enabled ablations;
- prevent dynamic shape from becoming reward hindsight, hidden solver behavior, or family-specific timing policy;
- later connect it to robot/simulation affordance and coarseness problems.
```


## Recursion scheduler / unfolding demand

Status after 2026-05-21 first-pass implementation:

```text
- Target-state doc exists: `ChangeOntCode/docs/kernel_spec/98_RECURSION_DEMAND_TARGET_STATE.md`.
- First-pass runtime carrier exists: `ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py`.
- First-pass invariants exist: `ChangeOntCode/agents/co/tests/recursion_scheduler_first_pass_invariants.py`.
- First-pass probe exists: `ChangeOntCode/experiments/studies/recursion_scheduler_first_pass_probe_v1.py`.
```

Current boundary:

```text
The scheduler derives bounded public structural recursion demand before
CollapseCertificate. It does not perform hidden lookahead, simulate undisclosed
futures, choose actions, or edit topology.
```

Remaining open work:

```text
- calibrate false-positive / false-negative recursion demand on real traces;
- distinguish scheduler pressure from ordinary search/lookahead in reports;
- connect scheduler output to any future actual second-layer unfolding mechanism;
- update formula sensitivity/ledger coverage for demand thresholds and budgets;
- compare against known search/planning expansion criteria before publication use.
```

## 10. Current-kernel diagnostic map

Current status: first-pass diagnostic map added on 2026-05-22.

Implemented:

```text
- `current_kernel_diagnostic_map_v1.py` runs the current rough kernel across active problem families;
- ablations: full_current, static_shape, no_quotient, no_scheduler, minimal_recent_core;
- report: `research_reports/2026-05-22/CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md`;
- invariant: `current_kernel_diagnostic_map_invariants.py`.
```

Open work:

```text
- rerun with more seeds/horizons after the next structural fixes;
- inspect families where telemetry changes but actions do not;
- audit false-positive recursion demand and missed quotient cases;
- do not use this diagnostic as benchmark evidence.
```

## 11. Current-kernel watchpoint audit — 2026-05-22

Current status: audit completed after the current-kernel diagnostic map.

Implemented:

```text
- `ChangeOntCode/experiments/studies/current_kernel_watchpoint_audit_v1.py` reads the diagnostic map outputs and classifies watchpoints;
- report: `research_reports/2026-05-22/CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md`;
- JSON output: `ChangeOntCode/outputs/current_kernel_watchpoint_audit_v1.json`.
```

Main audit findings:

```text
1. DynamicShapeField is partly readout-invisible: it deforms CandidateSurface effective controls, but CommitmentSurface final shape-gauged timing still reads static header/direct controls rather than the dynamic effective-control snapshot.
2. Recursion pressure provenance is ambiguous: high recursion demand occurs in bandit/renewal traces where RelationSurface relations are only weak decision-slot competition. The scheduler ignores weak competition directly, but inherits RCF field_recursion_budget without source-channel separation.
3. Quotienting is conservative but missed-quotient status is unaudited because real traces do not yet log quotient profile accept/reject reasons deeply enough.
4. Maintenance middle/renewal_like remain action-insensitive under recent-mechanism ablations in the capped diagnostic; this may be correct non-decisiveness or readout swamping.
5. Diagnostic log depth is too shallow for final interpretation: row-level commitment assessments, dynamic effective controls, and quotient rejection reasons must be logged before behavioral claims.
```

Required next work before robot/simulation expansion:

```text
- merge DynamicShapeField effective controls into CommitmentSurface readout controls without allowing dynamic shape to select actions directly;
- split recursion/field pressure provenance into structural-recursion, sampling/uncertainty, and weak-procedural channels;
- add deep row-level trace logging for selected families;
- rerun the current-family diagnostic map after those fixes;
- do not use the current map or audit as benchmark evidence.
```


## Post-hardening open points — 2026-05-22

- Quotient/equivalence needs real-trace accept/reject reason logging and false/missed-equivalence audit.
- Maintenance middle/renewal-like action-insensitivity remains unresolved even after DynamicShapeField readout visibility and recursion provenance split.
- Robot/simulation problems remain postponed until the current-kernel watchpoints above are understood.

## 12. Quotient accept/reject audit — 2026-05-22

Current status: audit completed after targeted hardening.

Added:

```text
ChangeOntCode/experiments/studies/quotient_accept_reject_audit_v1.py
ChangeOntCode/agents/co/tests/quotient_accept_reject_audit_invariants.py
research_reports/2026-05-22/QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md
ChangeOntCode/outputs/quotient_accept_reject_audit_v1.json
```

Result:

- quotient accept/reject provenance is now visible in relation telemetry and row traces;
- no duplicate-signature missed-quotient bug was found in the capped current-family diagnostic;
- accepted singleton profiles dominate, so quotienting remains conservative and mostly trace/identity annotation outside matched residual profiles.

Still open:

- design explicit false-quotient and missed-quotient real-trace/microcase audits;
- compare the quotient helper against state abstraction / bisimulation-style reductions;
- do not loosen quotient bands or tolerance based on benchmark outcomes.

## 13. Maintenance action-insensitivity audit — 2026-05-22

Current status: audit completed after targeted hardening.

Added:

```text
ChangeOntCode/experiments/studies/maintenance_action_insensitivity_audit_v1.py
ChangeOntCode/agents/co/tests/maintenance_action_insensitivity_audit_invariants.py
research_reports/2026-05-22/MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md
ChangeOntCode/outputs/maintenance_action_insensitivity_audit_v1.json
```

Result:

- maintenance middle and renewal_like remain action-prefix insensitive under recent-mechanism ablations in the capped diagnostic;
- the audit does not justify a maintenance-specific rule;
- the likely issue is generic readout dominance / stable-continuation swamping and incomplete generic pre-blocking resolver timing.

Next open step:

- add a generic dominance/readout-swamping audit;
- add cross-family pre-blocking resolver microcases;
- only after those decide whether the commitment formula needs a generic adjustment.

## Dominance / readout-swamping audit — 2026-05-22

Status: audited, not yet fixed.

The current kernel diagnostic map plus cross-family pre-blocking microcases show that some carrier branches remain selected despite explicit resolver alternatives because the generic pre-blocking carrier-pressure gate rejects the resolver path before comparison, or because support/stability/field mass swamps burden/blocker penalties. This is a generic readout calibration watchpoint, not a maintenance-specific tuning license.

Next lawful options:

1. leave runtime unchanged and gather broader traces;
2. implement a small generic carrier-gate calibration guarded by low-urgency, weak-resolver, and large-carrier-advantage negative controls.

Do not add native action-name rules, problem-family thresholds, reward hindsight, DP/baseline values, or maintenance-specific repair timing.

## Generic readout / carrier-gate status — 2026-05-22

Generic carrier-gate calibration completed: `preblocking_carrier_shape_urgency_weight` changed from `0.34` to `0.37`, guarded by cross-family microcases. This is not maintenance tuning and does not license family-specific repair rules.

Remaining open:

```text
sequence on/off evaluation and remaining readout-swamping trace audit
maintenance action-prefix insensitivity explanation after sequence composition
adapter-boundary and coefficient-sensitivity tests
robot/simulation problem design after kernel watchpoints are cleaner
```


## Sequence-level continuation composition — first-pass implemented, adequacy open

Status: implemented as a generic first-pass ordered composition layer; behavioral adequacy remains open.

`sequence_composition.py` derives public phase signatures and generic sequence transitions from public effects and row telemetry. The sequence microcase probe passes 5/5 cases, and `sequence_level_continuation_composition_audit_v1.py` now reports `sequence_field_rows=511` and `sequence_active_rows=176` in the capped diagnostic sample.

Required next work:

- run sequence on/off diagnostics across current families;
- audit whether readout consumes public sequence-phase evidence without collapsing into dominance scoring or a classical planner;
- check maintenance action-prefix insensitivity after sequence composition without adding maintenance-specific rules;
- perform adapter-boundary and coefficient-sensitivity audits before robot/sim expansion;
- add no new kernel mechanisms unless they pass the necessity gate.

## Pass-1 kernel closure audit blockers — 2026-05-22

Current audit: `research_reports/2026-05-22/PASS1_KERNEL_CLOSURE_AUDIT_REPORT_2026-05-22.md`. The known rough mechanism set is present, but the repo is not release-ready. Open blockers: architecture acceptance watchpoints; structural trace watchpoints; sequence composition effect not yet proven beyond telemetry; maintenance middle/renewal-like action-insensitivity; generic readout swamping; conservative quotient calibration; adapter-boundary and formula-grounding risk.

## Context-conditioned expectation audit follow-up
`research_reports/2026-05-25/CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md` adds the missing context-conditioned check. It does not justify new mechanisms or tuning. Follow-up should inspect DynamicShapeField strong-context under-consumption and determine whether it is (a) legitimate non-effect, (b) readout/wiring weakness, or (c) architecture limitation.

## DynamicShapeField direction / adequacy follow-up

Status: audit-only follow-ups added 2026-05-25. The prior context-conditioned audit over-counted DynamicShapeField suspicious non-effects because it did not count material dominance-score/margin changes as readout consumption. Remaining open point: determine whether DynamicShapeField score effects are directionally adequate in maintenance-like carrier/resolver contexts. This is a readout/control adequacy question, not a new-concept license.

## Maintenance DynamicShapeField resolution audit follow-up — 2026-05-25

Status: audit completed in `research_reports/2026-05-25/MAINTENANCE_DYNAMIC_SHAPE_RESOLUTION_AUDIT_REPORT_2026-05-25.md`. DynamicShapeField is not inert in maintenance-like traces. Remaining open point: eight `middle` cases classify as generic gate/readout underweighting watchpoints and ten cases require manual trace review. Next acceptable work is generic gate/readout adequacy microcases or broader Pass-1 evaluation; maintenance-specific tuning remains disallowed.

## Pass-1 all-problem CO vs STOA/baseline comparison — 2026-05-25

A bounded all-current-problem comparison has been run and recorded in `research_reports/2026-05-25/PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md` with raw outputs under `ChangeOntCode/outputs/pass1_all_problem_stoa_comparison_v1/`. It derives public shape reports for each active family/mode before comparing CO against repo-available public baselines/STOA-style baselines. This is diagnostic only: small seed count, capped horizons, no post-result tuning, and not publication-grade evidence. Results currently show CO is mostly below best public baselines, with a limited favorable/tie pattern only in latent-mechanism success metrics under the bounded setup.

## Pass-1 factor / causal sweep — 2026-05-25

Added `ChangeOntCode/experiments/studies/pass1_factor_causal_sweep_v1.py` and report `research_reports/2026-05-25/PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md`. This is a bounded diagnostic follow-up to the all-problem CO vs STOA comparison. It varies generic mechanism toggles, dynamic-shape update rate, counterfactual public shape profiles, and readout resolver gates. It is not a tuning run and counterfactual shapes are not canonical. Main result: no single factor explains the current weak STOA comparison; shape variation explains substantial variance in bandit/renewal/maintenance-renewal-like, but best CO variants usually remain below strong baselines. Maze is fine in the small visible case; latent is inconclusive under the shortened timeout-safe cap; maintenance middle requires longer-horizon phase/timing analysis rather than short-prefix interpretation.



## Post-factor causal investigation open points — 2026-05-25

A safe generic contract-vocabulary normalization was applied. Remaining open points are not solved by that fix: bandit exploration/update cadence, renewal phase extraction, maintenance longer-horizon gate/readout timing, adapter-boundary adversarial tests, and coefficient sensitivity. Do not choose counterfactual shapes from performance results.

## 2026-05-25 targeted failure-cause audit

Added `pass1_targeted_failure_cause_audit_v1` to separate current weak CO-vs-STOA performance into bandit exploration/evidence-cadence, renewal recurrence/phase-retention, and maintenance longer-horizon gate/readout timing causes. This is diagnostic only: no kernel mechanism, problem-specific rule, or performance tuning was added.


## Relation-field concentration / function-like collapse update (2026-05-25)

The repo now includes a bounded first-pass treatment of function-like mappings as earned collapses of public relation-fields under shape/gauge. Theory anchors: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md` and `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`. Kernel contract: `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`. Runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`, consumed by RelationSurface/DynamicShapeField. This is telemetry and shape evidence, not a full probabilistic relation algebra and not an action policy.


## Domain-relative coarseness update (2026-05-25)

Added `research_reports/2026-05-25/DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md` plus theory/doc/code support for bounded domain-relative coarseness: `coarseness_radius` remains the global fallback, while `coarseness_by_domain` records active public relation/burden-domain resolution. This is telemetry/control-gauge support, not a new action policy.
