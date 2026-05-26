# Next AI Start Here

This is the cold-onboarding entry point for the current ChangeOnt repo snapshot.

Use repo files as truth. Do not rely on chat-only handover claims when a file can be checked.

## 0. Current artifact status

This repo continues from the user-held artifact:

```text
ChangeOnt_dynamic_shape_contract_theory_audit_2026-05-18.zip
```

This updated working snapshot is:

```text
ChangeOnt_multistep_continuation_first_pass_2026-05-21.zip
```

Earlier lineage included:

```text
ChangeOnt_structural_formula_checks_fixes_2026-05-06.zip
```

Verified in the 2026-05-18 artifact and this 2026-05-21 continuation:

```text
shape/space derivation present:
- TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md

dynamic shape contract/spec present:
- ChangeOntCode/docs/kernel_spec/103_DYNAMIC_SHAPE_FIELD_CONTRACT.md
- ChangeOntCode/docs/kernel_spec/104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md

first-pass DynamicShapeField implementation present after 2026-05-21 update:
- ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py
- ChangeOntCode/agents/co/tests/dynamic_shape_field_invariants.py
- ChangeOntCode/experiments/studies/dynamic_shape_microcase_probe_v1.py
- ChangeOntCode/experiments/studies/dynamic_shape_real_trace_ablation_v1.py

active runtime surface files present:
- ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py
- ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
- ChangeOntCode/agents/co/runtime/surfaces/continuation_field.py
- ChangeOntCode/agents/co/runtime/surfaces/collapse_certificate.py
- ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py
- ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
```

This snapshot has structural validation reports and invariants. It includes a 2026-05-15 full-repo audit report at `FULL_REPO_AUDIT_REPORT_2026-05-15.md` and a stricter semantic relevance audit at `SEMANTIC_RELEVANCE_AUDIT_REPORT_2026-05-15.md` with a machine ledger at `SEMANTIC_RELEVANCE_AUDIT_LEDGER_2026-05-15.json`. It does not contain broad empirical proof that CO works.

## 1. Operating standard

Separate these layers at all times:

```text
1. ontology / TheoryOfChange_main conceptual chain
2. kernel docs / operational target
3. code implementation
4. diagnostics / tests
5. empirical evidence
6. future conceptual research
```

Truth outranks preservation. If code does not implement a claim, say that. If a test is structural rather than empirical, say that. If a result is only a report from a prior run, do not turn it into a fresh claim without rerunning or inspecting the artifact.

## 2. Canonical architecture

The active runtime target is:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity
→ Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ DynamicShapeField update / next-cycle gauge
→ CommitmentSurface
```

Interpretation:

```text
Boundary / Adapter:
  Publishes public observations, legal/admissible action expressions,
  public effects, and problem-shape inputs without solving the task.

CandidateSurface:
  Publishes candidate rows and initial candidate evidence. It is intake,
  not final readout.

Continuation Identity:
  Interprets candidate expressions as continuation-pressure signatures.
  A branch is not identical to an action.

Burden Operations:
  Carries operation facts such as carry, amplify, expose, buffer, mask,
  relieve, cancel, transfer, transform, threshold, and phase-shift.

RelationSurface:
  Derives branch relations from public effects kernel-side. It separates
  structural relation from weak procedural competition.

RecursiveContinuationField:
  Updates debt, relief support, grey pressure, recursion demand, collapse
  readiness, quotient/equivalence markers, and viability.

CollapseCertificate:
  Checks whether collapse is earned and preserves the reason structure.

DynamicShapeField:
  Persists first-pass local shape/coarseness state from public retained trace.
  It deforms next-cycle controls only; it does not select native actions.

CommitmentSurface:
  Emits the native action as final readout while respecting certificate gates.
  It fails closed when required CO evidence is absent.
```

## 3. Reading order

There is one authoritative onboarding route. Start with the reference stack and follow the nested order it gives. `00_INDEX.md` is a catalog after the stack is understood, not a competing first instruction.

Read in this order:

```text
1. TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md
2. TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md
3. TheoryOfChange_main/00_Meta/TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md
4. ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
5. ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
6. ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md
7. ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
8. ChangeOntCode/docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
9. ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
10. ChangeOntCode/docs/kernel_spec/03C_IMPLEMENTATION_FIDELITY_STATUS.md
11. ChangeOntCode/docs/kernel_spec/00_INDEX.md
12. CANONICAL_STRUCTURE_MAP.md
13. OPEN_POINTS_AND_FUTURE_WORK.md
14. FIRST_PASS_COMPLETION_LEDGER_2026-05-21.md
15. PUBLICATION_TARGET_GAP_LEDGER_2026-05-21.md

MULTI_STEP_CONTINUATION_IDENTITY_UPDATE_2026-05-21.md
  First-pass continuation-memory update: cross-action public burden-domain memory without branch-ID collapse.
16. FULL_REPO_AUDIT_REPORT_2026-05-15.md
15. SEMANTIC_RELEVANCE_AUDIT_REPORT_2026-05-15.md
```

Then inspect the implementation path in this concrete order. The folder list alone is not enough for cold onboarding.

```text
Boundary / packet contracts:
  ChangeOntCode/agents/co/boundary/packet_schema.py
  ChangeOntCode/agents/co/boundary/problem_packet.py
  ChangeOntCode/agents/co/boundary/observation_mapper.py
  ChangeOntCode/agents/co/boundary/action_mapper.py
  ChangeOntCode/agents/co/boundary/update_mapper.py

Adapters / public facts and public_effects:
  ChangeOntCode/agents/co/adapters/common.py
  ChangeOntCode/agents/co/adapters/bandit_adapter.py
  ChangeOntCode/agents/co/adapters/renewal_adapter.py
  ChangeOntCode/agents/co/adapters/maze_adapter.py
  ChangeOntCode/agents/co/adapters/latent_mechanism_adapter.py
  ChangeOntCode/agents/co/adapters/maintenance_replacement_adapter.py
  ChangeOntCode/agents/co/adapters/probes.py

Placement / six-question public regime basis:
  ChangeOntCode/agents/co/placement/shape_prior6.py
  ChangeOntCode/agents/co/placement/control.py
  ChangeOntCode/agents/co/placement/control_defaults.py
  ChangeOntCode/agents/co/placement/regime.py

Runtime surfaces / active loop:
  ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py
  ChangeOntCode/agents/co/runtime/surfaces/continuation_state.py
  ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
  ChangeOntCode/agents/co/runtime/surfaces/continuation_field.py
  ChangeOntCode/agents/co/runtime/surfaces/collapse_certificate.py
  ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py
  ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
  ChangeOntCode/agents/co/runtime/surfaces/telemetry.py

Integration / canonical runtime assembly:
  ChangeOntCode/agents/co/integration/manifest_loader.py
  ChangeOntCode/agents/co/integration/component_factory.py
  ChangeOntCode/agents/co/integration/core_builder.py
  ChangeOntCode/agents/co/integration/core_assembly.py
  ChangeOntCode/agents/co/integration/dependency_validator.py

Diagnostics / minimum structural evidence path:
  ChangeOntCode/agents/co/tests/certified_runtime_alignment_invariants.py
  ChangeOntCode/agents/co/tests/no_classical_fallback_fail_closed_invariants.py
  ChangeOntCode/agents/co/tests/candidate_surface_publication_invariants.py
  ChangeOntCode/agents/co/tests/relation_surface_public_effect_invariants.py
  ChangeOntCode/agents/co/tests/kernel_structure_carrier_alignment_invariants.py
  ChangeOntCode/agents/co/tests/collapse_certificate_readout_invariants.py
  ChangeOntCode/agents/co/tests/structural_trace_validation_invariants.py
  ChangeOntCode/agents/co/tests/relation_path_trace_diagnostics.py
  ChangeOntCode/agents/co/tests/code_vs_docs_pipeline_compliance_invariants.py
```

When validating the conceptual source line, do not stop at the route README files. `FIRST_LAYER_CANONICAL_PATH.md` points to route directories; read each route README and then the numbered files inside that route in filename order.

## 4. Current repo state summary

Conceptual status:

```text
TheoryOfChange_main is acceptable as the conceptual source line for the
current kernel-architecture phase, but later formal and consciousness tracks
remain open.
```

Docs status:

```text
ChangeOntCode/docs/kernel_spec is the canonical operational target for this
phase. The 2026-05-06 certification report says the docs were cleaned into a
canonical implementation target, with limitations explicitly retained.
```

Code status:

```text
The active surfaces and invariants exist. Structural trace checks passed in
baseline verification during this onboarding pass. Code alignment does not mean
empirical proof.
```

Open status:

```text
formula grounding, quotient/equivalence calibration beyond the first-pass public residual-profile helper, recursion scheduling,
sequence-level continuation identity, controlled empirical validation, and known-
algorithm comparison remain open.
```

## 5. Verification commands

From repo root:

```bash
python tools/validate_toc_main.py
cd ChangeOntCode
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.candidate_surface_publication_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.relation_path_trace_diagnostics
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
python -m agents.co.tests.dynamic_shape_field_invariants
python -m agents.co.tests.multi_step_continuation_identity_invariants
python -m agents.co.tests.quotient_equivalence_first_pass_invariants
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
python -m experiments.studies.architecture_acceptance_audit_v1
```

Treat passing structural checks as permission to proceed to controlled diagnostics, not as proof of benchmark usefulness.

## 6. Next phase after onboarding

Proceed in this order:

```text
1. full invariant suite
2. structural trace validation
3. relation-path trace
4. architecture acceptance audit
5. ablations:
   - RelationSurface on/off
   - public_effects present/stripped
   - branch-internal operations present/stripped
   - CollapseCertificate on/off
   - same scalar rows with different relation topology
6. manual trace review across bandit, maintenance, maze, renewal, latent mechanism
7. only then broader family studies and fair baseline comparisons
```

Do not tune performance to make the kernel look good. Freeze constants for evidence-bearing studies, log seeds and JSONL, label oracle baselines honestly, and report regressions.

## 7. Maintenance instructions

When changing the repo:

```text
- update docs before code when the target changes;
- update code before claiming implementation alignment;
- add or update invariants when behavior-affecting structure changes;
- keep README, this file, CANONICAL_STRUCTURE_MAP.md, and OPEN_POINTS_AND_FUTURE_WORK.md current;
- keep exploratory/future research clearly outside the active implementation target;
- do not leave theory-relevant decisions only in chat.
```

## 2026-05-16 stage-gate baseline

The latest validation/freeze artifacts are:

- `STRUCTURAL_BASELINE_FREEZE_2026-05-16.md`
- `FORMULA_COEFFICIENT_LEDGER_2026-05-16.md`
- `SYSTEMATIC_MECHANISM_ABLATION_REVIEW_2026-05-16.md`
- `REAL_FAMILY_MANUAL_TRACE_REVIEW_REPORT_2026-05-16.md`
- `FROZEN_EMPIRICAL_SANITY_SMOKE_REPORT_2026-05-16.md`
- `STAGE_GATE_EXECUTION_REPORT_2026-05-16.md`

Interpretation boundary: these are structural/formula/runtime-sanity artifacts. They do not prove CO, RCF novelty, or empirical usefulness.

## 2026-05-17 frozen logged empirical mini-suite

The first frozen logged empirical mini-suite has now executed:

- `FROZEN_LOGGED_EMPIRICAL_MINI_SUITE_REPORT_2026-05-17.md`
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

- `FOCUSED_FROZEN_EMPIRICAL_MINI_BENCHMARK_REPORT_2026-05-17.md`
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


Dynamic shape / coarseness target:
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md` derives local shape, CO-space, directed unfolding, coarseness, point-as-ball, and dynamic shape update as a target.
- `ChangeOntCode/docs/kernel_spec/103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` specifies what the first-pass persistent DynamicShapeField may update.
- `ChangeOntCode/docs/kernel_spec/104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md` lists microcase gates now backed by first-pass structural tests.
- Current runtime now implements first-pass persistent dynamic shape state in `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py`, while retaining static shape prior and local shape-gauged resolver timing as separate mechanisms.


## 2026-05-21 recursion scheduler first-pass update

`ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py` now provides a first-pass bounded public structural recursion-demand scheduler between RCF and CollapseCertificate. It is not hidden lookahead, not an action selector, and not final recursion theory. See `RECURSION_SCHEDULER_FIRST_PASS_PROBE_REPORT_2026-05-21.md`.

## Latest continuation note — current-kernel diagnostic map

After the recursion-scheduler first-pass package, the next slice added a current-kernel diagnostic map:

```text
ChangeOntCode/experiments/studies/current_kernel_diagnostic_map_v1.py
ChangeOntCode/agents/co/tests/current_kernel_diagnostic_map_invariants.py
CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md
```

It runs the rough kernel across current active families/modes under generic ablations: full current, static shape, no quotient, no scheduler, and minimal recent core. Treat it as a mechanism-visibility and action-sensitivity map only. Do not cite it as benchmark evidence.

## Latest continuation note — current-kernel watchpoint audit

After the current-kernel diagnostic map, a watchpoint audit was added:

```text
ChangeOntCode/experiments/studies/current_kernel_watchpoint_audit_v1.py
CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md
ChangeOntCode/outputs/current_kernel_watchpoint_audit_v1.json
```

The audit did not change kernel behavior. It found that the next task should be targeted kernel hardening, not robot/sim expansion:

```text
1. DynamicShapeField effective controls must become visible to CommitmentSurface readout/gating, not only CandidateSurface.
2. Recursion pressure provenance must be split so sampling/uncertainty/weak-procedural pressure does not masquerade as structural recursion demand.
3. Deep row-level trace logging is needed before interpreting telemetry-only action-insensitive families.
```


## Current next step after targeted hardening

Start with `CURRENT_KERNEL_TARGETED_HARDENING_REPORT_2026-05-22.md` and `CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md`. Do not add robot/sim yet. Next audit quotient missed/false-equivalence by logging accept/reject reasons, then use the new row-level traces to diagnose maintenance action-insensitivity.

## Latest continuation note — quotient and maintenance audit

After `ChangeOnt_current_kernel_targeted_hardening_2026-05-22.zip`, two audit-only studies were added:

```text
ChangeOntCode/experiments/studies/quotient_accept_reject_audit_v1.py
ChangeOntCode/experiments/studies/maintenance_action_insensitivity_audit_v1.py
ChangeOntCode/agents/co/tests/quotient_accept_reject_audit_invariants.py
ChangeOntCode/agents/co/tests/maintenance_action_insensitivity_audit_invariants.py
```

Read:

```text
QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md
MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md
```

Current result: quotienting is now auditable and no duplicate-signature missed-quotient bug was found in the capped diagnostic, but quotient tolerance remains conservative and unfinished. Maintenance middle/renewal_like remain action-insensitive under recent-mechanism ablations; the audit points to generic readout dominance / incomplete pre-blocking resolver timing rather than a maintenance-specific rule. Next step: generic dominance/readout-swamping audit plus cross-family pre-blocking resolver microcases. Do not add robot/sim yet.

## 2026-05-22 immediate watchpoint

Before adding robot/sim problems, read `DOMINANCE_READOUT_SWAMPING_AUDIT_UPDATE_2026-05-22.md`. The current kernel has a generic readout-swamping/carrier-gate calibration watchpoint. Do not patch it with problem-specific rules. If changing behavior, use only a generic carrier-gate calibration guarded by the cross-family pre-blocking resolver microcases.

## 2026-05-22 generic carrier-gate calibration

A small generic readout calibration was applied after the dominance/readout-swamping audit: `preblocking_carrier_shape_urgency_weight` moved from `0.34` to `0.37` in `CommitmentSurface`. This is not maintenance tuning. It makes public shape urgency slightly more able to lower the pre-blocking carrier-pressure gate before resolver comparison.

See `GENERIC_CARRIER_GATE_CALIBRATION_REPORT_2026-05-22.md`. The cross-family pre-blocking microcases now report `cases=6`, `passed=5`, `observed=1`, `watchpoints=0`, while low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected. Current-family diagnostic map still runs `40/40` successfully. Maintenance action-prefix insensitivity remains unresolved (`insensitive_comparison_count=8`, `sensitive_comparison_count=0`).

Next step: freeze the Pass-1 kernel closure candidate, rerun mechanism/evaluation diagnostics, and decide whether remaining readout swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure. Do not add robot/sim or family-specific rules yet.

## Latest continuation note — sequence/readout trace audit

After `ChangeOnt_generic_carrier_gate_calibration_2026-05-22.zip`, two audit-only studies were added:

```text
ChangeOntCode/experiments/studies/sequence_level_continuation_composition_audit_v1.py
ChangeOntCode/experiments/studies/generic_readout_swamping_trace_audit_v1.py
ChangeOntCode/agents/co/tests/sequence_level_continuation_composition_audit_invariants.py
ChangeOntCode/agents/co/tests/generic_readout_swamping_trace_audit_invariants.py
```

Reports:

```text
SEQUENCE_LEVEL_CONTINUATION_COMPOSITION_AUDIT_REPORT_2026-05-22.md
GENERIC_READOUT_SWAMPING_TRACE_AUDIT_REPORT_2026-05-22.md
```

Current result: first-pass public burden-domain continuation memory exists and generic ordered sequence-composition carriers are now present. In the current diagnostic sample, `sequence_field_rows = 511` and `sequence_active_rows = 176`. Generic readout-swamping traces remain: support/stability/field mass can dominate unresolved burden/resolver structure, and many carrier-with-resolver-alt steps do not trigger shape-gauged timing.

Next step: treat the rough Pass-1 kernel as a closure candidate and evaluate it. Do not add maintenance-specific `INSPECT -> REPAIR -> RUN` logic, native action-name rules, or robot/sim expansion until diagnostics justify the move.


## 2026-05-22 kernel Pass-1 closure candidate

Generic sequence-level continuation composition has been implemented and wired. See `KERNEL_PASS1_CLOSURE_CANDIDATE_REPORT_2026-05-22.md`, `SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`, and the updated sequence/readout audits.

Current status: the known rough kernel mechanism set is now present as a Pass-1 closure candidate, not a final kernel. Next work should freeze/evaluate rather than add mechanisms: sequence on/off diagnostics, adapter-boundary tests, coefficient sensitivity, quotient false/missed quotient audit, and a current-family failure map. Robot/sim expansion remains premature until this evaluation is complete.

## Current latest audit checkpoint — 2026-05-22

Read `PASS1_KERNEL_CLOSURE_AUDIT_REPORT_2026-05-22.md` before adding code. The repo should now be treated as a Pass-1 kernel closure candidate, not a finished kernel. Do not add new mechanisms unless the necessity gate is passed. The next work should evaluate/fix the recorded blockers: sequence-readout consumption, maintenance/readout insensitivity, adapter-boundary adversarial tests, and formula/coefficient grounding.

## Latest diagnostic note — context-conditioned expectation audit (2026-05-25)
Before changing readout or adding mechanisms, read `CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md`. The audit shows that raw action-difference counts are insufficient. Expected mechanism relevance must be conditioned on public shape/gauge plus local burden/relation/sequence/certificate triggers. Current verdict: sequence, quotient, and recursion are mostly consumed when strongly expected; DynamicShapeField remains a readout-consumption watchpoint.

### Latest audit note — DynamicShapeField expectation investigation

Before changing DynamicShapeField or CommitmentSurface, read:

1. `CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md`
2. `DYNAMIC_SHAPE_SUSPICIOUS_CASE_INVESTIGATION_REPORT_2026-05-25.md`
3. `DYNAMIC_SHAPE_DIRECTION_ADEQUACY_AUDIT_REPORT_2026-05-25.md`

The latest investigation says the earlier DynamicShapeField suspicious count mostly reflected audit-method over-strictness: score/margin effects were present even when actions/gate booleans did not change. The remaining question is direction/adequacy, not existence. Do not add a new mechanism or tune family-specific behavior from the old suspicious count.

## Latest audit note — 2026-05-25

Read `MAINTENANCE_DYNAMIC_SHAPE_RESOLUTION_AUDIT_REPORT_2026-05-25.md` after the DynamicShapeField expectation reports. It narrows the maintenance issue: DynamicShapeField often moves margins, so the problem is not absence/inertness. The remaining watchpoint is whether current generic carrier/resolver gates are too conservative in phase-structured contexts, especially maintenance `middle`. Do not patch maintenance-specific behavior.

## Pass-1 all-problem CO vs STOA/baseline comparison — 2026-05-25

A bounded all-current-problem comparison has been run and recorded in `PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md` with raw outputs under `ChangeOntCode/outputs/pass1_all_problem_stoa_comparison_v1/`. It derives public shape reports for each active family/mode before comparing CO against repo-available public baselines/STOA-style baselines. This is diagnostic only: small seed count, capped horizons, no post-result tuning, and not publication-grade evidence. Results currently show CO is mostly below best public baselines, with a limited favorable/tie pattern only in latent-mechanism success metrics under the bounded setup.

## Pass-1 factor / causal sweep — 2026-05-25

Added `ChangeOntCode/experiments/studies/pass1_factor_causal_sweep_v1.py` and report `PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md`. This is a bounded diagnostic follow-up to the all-problem CO vs STOA comparison. It varies generic mechanism toggles, dynamic-shape update rate, counterfactual public shape profiles, and readout resolver gates. It is not a tuning run and counterfactual shapes are not canonical. Main result: no single factor explains the current weak STOA comparison; shape variation explains substantial variance in bandit/renewal/maintenance-renewal-like, but best CO variants usually remain below strong baselines. Maze is fine in the small visible case; latent is inconclusive under the shortened timeout-safe cap; maintenance middle requires longer-horizon phase/timing analysis rather than short-prefix interpretation.



## Latest status note — 2026-05-25 causal investigation adjustment

The latest pass applied one conservative generic correction to the public contract/shape path: extended vocabulary for `drift=none` and ordinal commitment costs such as `medium_to_high`. Treat this as a boundary/shape-fidelity fix, not a benchmark-tuned shape selection. The factor/performance deficits remain multi-causal; see `PASS1_CAUSAL_INVESTIGATION_ADJUSTMENT_REPORT_2026-05-25.md`.

## 2026-05-25 targeted failure-cause audit

Added `pass1_targeted_failure_cause_audit_v1` to separate current weak CO-vs-STOA performance into bandit exploration/evidence-cadence, renewal recurrence/phase-retention, and maintenance longer-horizon gate/readout timing causes. This is diagnostic only: no kernel mechanism, problem-specific rule, or performance tuning was added.


## Relation-field concentration / function-like collapse update (2026-05-25)

The repo now includes a bounded first-pass treatment of function-like mappings as earned collapses of public relation-fields under shape/gauge. Theory anchors: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md` and `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`. Kernel contract: `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`. Runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`, consumed by RelationSurface/DynamicShapeField. This is telemetry and shape evidence, not a full probabilistic relation algebra and not an action policy.


## Domain-relative coarseness update (2026-05-25)

Added `DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md` plus theory/doc/code support for bounded domain-relative coarseness: `coarseness_radius` remains the global fallback, while `coarseness_by_domain` records active public relation/burden-domain resolution. This is telemetry/control-gauge support, not a new action policy.
