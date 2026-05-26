# ChangeOnt

ChangeOnt is a research repo for a change-first ontology and its current experimental kernel implementation. The present repo state should be read as a coherence-and-validation workspace, not as evidence that the kernel already works empirically.

Start here:

```text
NEXT_AI_START_HERE.md
```

That file gives the current repo state, the canonical reading order, the code path, validation commands, and open work. Do not reconstruct the project from chat history when the repo files are available.

## Current status

Current working snapshot after this update:

```text
ChangeOnt_current_kernel_diagnostic_map_2026-05-22.zip
```

Latest user-held source artifact for this continuation:

```text
ChangeOnt_dynamic_shape_contract_theory_audit_2026-05-18.zip
```

Earlier verified base lineage:

```text
ChangeOnt_structural_formula_checks_fixes_2026-05-06.zip
```

This package also includes two 2026-05-15 audit records:

```text
FULL_REPO_AUDIT_REPORT_2026-05-15.md
  Full-repo audit/hardening pass.

SEMANTIC_RELEVANCE_AUDIT_REPORT_2026-05-15.md
  Stricter semantic relevance audit: classifies markdown/code files, checks the active route, fixes current-route defects, and records what remains only scanned/classified.
```

The current phase is:

```text
complete the first rough pass across concepts, docs, code, diagnostics, and problem coverage;
then use the second pass for refinement, critic-facing explanation, and stronger evidence.
```

Not claimed here:

```text
CO is proven;
the kernel is empirically useful;
RCF novelty is established;
broad benchmark evidence exists;
consciousness claims follow from this runtime.
```

## Canonical execution loop

The active runtime target is one loop:

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

Adapters publish public facts and public burden-effect facts. The kernel derives relations and collapse status. DynamicShapeField now persists first-pass local shape/coarseness state from public retained trace and deforms next-cycle controls. CommitmentSurface is the final readout and must respect earned-collapse certificate gates. Evidence-bearing CO runtime fails closed when required structure is absent; external baseline algorithms are comparison tools only.

## Repository map

```text
TheoryOfChange_main/
  Canonical ontology/_main material. This is the conceptual source line.

ChangeOntCode/docs/kernel_spec/
  Canonical operational target for the current kernel phase.
  Start with 00_INDEX.md and 00A_DOCS_READING_GUIDE.md.

ChangeOntCode/agents/co/
  Current CO implementation: boundary, adapters, placement controls,
  runtime surfaces, integration, and invariants.

ChangeOntCode/environments/
  Problem families used for structural and empirical testing.

ChangeOntCode/agents/stoa/ and ChangeOntCode/experiments/baselines/
  Baselines for comparison. They are not CO runtime fallbacks.

validation_outputs/ and root *2026-05-06.md reports
  Prior validation/report artifacts for this snapshot. Treat them as historical
  evidence about this repo state, not as broad performance proof.

CANONICAL_STRUCTURE_MAP.md
  Cross-map from _main → kernel docs → code → diagnostics.

OPEN_POINTS_AND_FUTURE_WORK.md
  Current implementation/test tasks and later research tracks.

FIRST_PASS_COMPLETION_LEDGER_2026-05-21.md
  Pass-1 status: what now exists, what remains incomplete, and what is not yet publication evidence.

PUBLICATION_TARGET_GAP_LEDGER_2026-05-21.md

CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md
  Diagnostic map across current active families under dynamic-shape/quotient/scheduler ablations; not benchmark evidence.

MULTI_STEP_CONTINUATION_IDENTITY_UPDATE_2026-05-21.md
  First-pass continuation-memory update: cross-action public burden-domain memory without branch-ID collapse.
  Gap ledger relative to the eventual critic-facing paper/book target.

FULL_REPO_AUDIT_REPORT_2026-05-15.md
  Full-repo audit findings, fixes, commands run, and remaining gaps from 2026-05-15.

SEMANTIC_RELEVANCE_AUDIT_REPORT_2026-05-15.md
SEMANTIC_RELEVANCE_AUDIT_LEDGER_2026-05-15.json
  Stricter file-classification and active-route coherence audit. Use this to see what was deeply read, what was scanned/classified, and what remains open.
```

## Minimal verification commands

From repo root:

```bash
cd ChangeOntCode
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.relation_path_trace_diagnostics
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
```

Passing these checks means the current structural/runtime contracts still hold for the tested cases. It does not establish empirical superiority.

## Maintenance rule

Keep the repo self-onboarding. When architecture changes, update in this order:

```text
TheoryOfChange_main conceptual source if needed
→ ChangeOntCode/docs/kernel_spec docs
→ ChangeOntCode/agents/co implementation
→ invariants/diagnostics
→ README / NEXT_AI_START_HERE / structure map / open-points file
```

Do not leave theory-relevant decisions only in chat.


## 2026-05-21 first-pass DynamicShapeField / continuation / quotient updates

This snapshot includes the first rough implementation slices needed for the current Pass-1 kernel-completion phase:

```text
ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py
ChangeOntCode/agents/co/runtime/surfaces/continuation_state.py
ChangeOntCode/agents/co/runtime/surfaces/quotient_equivalence.py

ChangeOntCode/agents/co/tests/dynamic_shape_field_invariants.py
ChangeOntCode/agents/co/tests/dynamic_shape_microcase_probe_invariants.py
ChangeOntCode/agents/co/tests/dynamic_shape_real_trace_ablation_invariants.py
ChangeOntCode/agents/co/tests/multi_step_continuation_identity_invariants.py
ChangeOntCode/agents/co/tests/quotient_equivalence_first_pass_invariants.py

ChangeOntCode/experiments/studies/dynamic_shape_microcase_probe_v1.py
ChangeOntCode/experiments/studies/dynamic_shape_real_trace_ablation_v1.py
ChangeOntCode/experiments/studies/multi_step_continuation_identity_probe_v1.py
ChangeOntCode/experiments/studies/quotient_equivalence_first_pass_probe_v1.py

FIRST_PASS_COMPLETION_LEDGER_2026-05-21.md
PUBLICATION_TARGET_GAP_LEDGER_2026-05-21.md

CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md
  Diagnostic map across current active families under dynamic-shape/quotient/scheduler ablations; not benchmark evidence.
MULTI_STEP_CONTINUATION_IDENTITY_UPDATE_2026-05-21.md
QUOTIENT_EQUIVALENCE_FIRST_PASS_PROBE_REPORT_2026-05-21.md
```

Boundaries:

```text
DynamicShapeField persists generic local shape/coarseness state and deforms next-cycle controls only.
Continuation memory can now persist across different action expressions by public burden-domain key, but generic sequence-level composition now has a first-pass implementation; behavioral sufficiency remains open.
Quotient/equivalence now has a first-pass public residual-profile helper, but final tolerance and real-trace false/missed quotient analysis remain open.
None of these updates proves reward improvement, CO novelty, or final mathematical topology.
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

## 2026-05-22 current-kernel watchpoint audit

After the current-kernel diagnostic map, `current_kernel_watchpoint_audit_v1.py` was added as a report-only audit. It reads the diagnostic map outputs and writes `CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md` plus `ChangeOntCode/outputs/current_kernel_watchpoint_audit_v1.json`.

The audit found that robot/simulation expansion should wait. DynamicShapeField is currently partly readout-invisible, because CandidateSurface uses dynamic effective controls but CommitmentSurface shape-gauged timing still reads static direct controls. Recursion demand also needs provenance splitting: high demand appears in weak-decision-slot-only traces because scheduler demand inherits RCF field_recursion_budget without separating structural recursion from sampling/uncertainty pressure.

This audit is not evidence for CO performance or novelty. It is a Pass-1 alignment warning.


## 2026-05-22 targeted hardening update

The latest package hardens the current-kernel diagnostic watchpoints: DynamicShapeField effective controls are now visible to CommitmentSurface, RecursionScheduler provenance is split into structural / sampling-uncertainty / weak-procedural channels, and the current-kernel diagnostic map now logs compact row-level traces. See `CURRENT_KERNEL_TARGETED_HARDENING_REPORT_2026-05-22.md`. Remaining watchpoints: quotient accept/reject audit and maintenance action-insensitivity.

## 2026-05-22 quotient / maintenance audit

After targeted hardening, two audit-only studies were added:

- `ChangeOntCode/experiments/studies/quotient_accept_reject_audit_v1.py` writes `QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md` and `ChangeOntCode/outputs/quotient_accept_reject_audit_v1.json`. It verifies that quotient accept/reject provenance is visible and that the capped diagnostic shows no duplicate-signature missed-quotient bug. It does **not** finalize quotient tolerance.
- `ChangeOntCode/experiments/studies/maintenance_action_insensitivity_audit_v1.py` writes `MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md` and `ChangeOntCode/outputs/maintenance_action_insensitivity_audit_v1.json`. It confirms maintenance middle/renewal_like action-prefix insensitivity under recent-mechanism ablations and classifies the likely issue as generic readout dominance / pre-blocking resolver timing, not a license for maintenance-specific tuning.

Next step: generic dominance/readout-swamping audit and cross-family pre-blocking resolver microcases. Do not add robot/sim or tune maintenance yet.

### 2026-05-22 Dominance/readout-swamping audit note

The latest first-pass audit added generic readout component telemetry plus cross-family pre-blocking resolver microcases. It did not tune maintenance or any other family. It found a generic carrier-gate/readout calibration watchpoint: explicit resolver alternatives can be present while a carrier branch remains selected because pre-blocking timing fails the carrier-pressure gate or support/stability/field mass swamps burden/blocker penalties. See `DOMINANCE_READOUT_SWAMPING_AUDIT_UPDATE_2026-05-22.md`, `DOMINANCE_READOUT_SWAMPING_AUDIT_REPORT_2026-05-22.md`, and `PREBLOCKING_RESOLVER_CROSS_FAMILY_MICROCASE_PROBE_REPORT_2026-05-22.md`.

## 2026-05-22 generic carrier-gate calibration

A small generic readout calibration was applied after the dominance/readout-swamping audit: `preblocking_carrier_shape_urgency_weight` moved from `0.34` to `0.37` in `CommitmentSurface`. This is not maintenance tuning. It makes public shape urgency slightly more able to lower the pre-blocking carrier-pressure gate before resolver comparison.

See `GENERIC_CARRIER_GATE_CALIBRATION_REPORT_2026-05-22.md`. The cross-family pre-blocking microcases now report `cases=6`, `passed=5`, `observed=1`, `watchpoints=0`, while low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected. Current-family diagnostic map still runs `40/40` successfully. Maintenance action-prefix insensitivity remains unresolved (`insensitive_comparison_count=8`, `sensitive_comparison_count=0`).

Next step: freeze the Pass-1 kernel closure candidate, rerun mechanism/evaluation diagnostics, and decide whether remaining readout swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure. Do not add robot/sim or family-specific rules yet.

## 2026-05-22 sequence/readout trace audit

After the generic carrier-gate calibration, two audit-only studies were added:

- `ChangeOntCode/experiments/studies/sequence_level_continuation_composition_audit_v1.py` writes `SEQUENCE_LEVEL_CONTINUATION_COMPOSITION_AUDIT_REPORT_2026-05-22.md` and `ChangeOntCode/outputs/sequence_level_continuation_composition_audit_v1.json`.
- `ChangeOntCode/experiments/studies/generic_readout_swamping_trace_audit_v1.py` writes `GENERIC_READOUT_SWAMPING_TRACE_AUDIT_REPORT_2026-05-22.md` and `ChangeOntCode/outputs/generic_readout_swamping_trace_audit_v1.json`.

Historical result before implementation: this audit initially found public burden-domain continuation memory but no explicit sequence-composition carrier. This has now been superseded by the first-pass sequence-composition implementation below.


## 2026-05-22 Pass-1 kernel closure candidate — sequence composition implemented

Generic first-pass sequence-level continuation composition has been implemented in `ChangeOntCode/agents/co/runtime/surfaces/sequence_composition.py` and wired into `CandidateSurface`. It derives public phase signatures from public effects/row telemetry and supports generic phase transitions such as exposure → relief and relief → stabilization without family names, native action-name rules, hidden state, reward hindsight, DP/baseline values, or topology editing.

New diagnostics:

- `ChangeOntCode/experiments/studies/sequence_composition_microcase_probe_v1.py` writes `SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md` and passes 5/5 microcases.
- `sequence_level_continuation_composition_audit_v1.py` now reports `sequence_field_rows=511` and `sequence_active_rows=176` in the capped current-family diagnostic sample.
- `current_kernel_diagnostic_map_v1.py` now runs 48/48 capped diagnostic runs with a `no_sequence` ablation variant.

Interpretation: the known Pass-1 kernel mechanism set now has a closure candidate. This is not proof, not final architecture acceptance, and not a reason to add robot/sim yet. The next step is freeze/evaluate: sequence on/off diagnostics, remaining readout-swamping analysis, adapter-boundary tests, coefficient sensitivity, and all-family behavior mapping. New kernel mechanisms should require a strict necessity gate.

## 2026-05-22 Pass-1 kernel closure audit

`PASS1_KERNEL_CLOSURE_AUDIT_REPORT_2026-05-22.md` is the current freeze/evaluation audit for the rough kernel closure candidate. It reports that the known rough mechanism files are present and the current diagnostic map runs succeed, but the repo is not release-ready or publication-ready. Remaining blockers include architecture/structural watchpoints, sequence-readout effect uncertainty, maintenance action-insensitivity, generic readout swamping, conservative quotient calibration, and adapter/formula grounding.

### 2026-05-25 Context-conditioned expectation audit
A diagnostic-only context-conditioned expectation audit was added in `CONTEXT_CONDITIONED_EXPECTATION_AUDIT_REPORT_2026-05-25.md` and `ChangeOntCode/experiments/studies/context_conditioned_expectation_audit_v1.py`. It corrects the earlier aggregate-ablation framing by classifying full-current steps by public shape/gauge context and local structural triggers before judging whether DynamicShapeField, sequence composition, quotienting, or recursion should matter. It found that sequence/quotient/recursion strong-context cases are mostly consumed by action or gate/readout effects, while DynamicShapeField still has a medium under-consumption watchpoint. No kernel behavior was changed.

### 2026-05-25 Dynamic-shape expectation investigation

Added audit-only follow-ups to the context-conditioned expectation audit:

- `DYNAMIC_SHAPE_SUSPICIOUS_CASE_INVESTIGATION_REPORT_2026-05-25.md`
- `DYNAMIC_SHAPE_DIRECTION_ADEQUACY_AUDIT_REPORT_2026-05-25.md`

These reports correct the earlier aggregate interpretation: most DynamicShapeField “suspicious non-effects” were actually score/margin effects not counted by the prior gate/action-only audit. DynamicShapeField is therefore not inert, but adequacy remains open, especially whether score effects are directionally strong enough in maintenance-like carrier/resolver contexts.

## 2026-05-25 maintenance DynamicShapeField resolution audit

Latest added audit: `MAINTENANCE_DYNAMIC_SHAPE_RESOLUTION_AUDIT_REPORT_2026-05-25.md`. This is audit-only and makes no kernel behavior change. It investigates maintenance-like cases where DynamicShapeField narrows dominance margins without changing the selected action. The audit finds DynamicShapeField is not inert in maintenance traces; many non-decisive cases remain below the current generic carrier/resolver gate, while `middle` still has generic gate/readout watchpoints. No maintenance-specific tuning is justified.

## Pass-1 all-problem CO vs STOA/baseline comparison — 2026-05-25

A bounded all-current-problem comparison has been run and recorded in `PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md` with raw outputs under `ChangeOntCode/outputs/pass1_all_problem_stoa_comparison_v1/`. It derives public shape reports for each active family/mode before comparing CO against repo-available public baselines/STOA-style baselines. This is diagnostic only: small seed count, capped horizons, no post-result tuning, and not publication-grade evidence. Results currently show CO is mostly below best public baselines, with a limited favorable/tie pattern only in latent-mechanism success metrics under the bounded setup.

## Pass-1 factor / causal sweep — 2026-05-25

Added `ChangeOntCode/experiments/studies/pass1_factor_causal_sweep_v1.py` and report `PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md`. This is a bounded diagnostic follow-up to the all-problem CO vs STOA comparison. It varies generic mechanism toggles, dynamic-shape update rate, counterfactual public shape profiles, and readout resolver gates. It is not a tuning run and counterfactual shapes are not canonical. Main result: no single factor explains the current weak STOA comparison; shape variation explains substantial variance in bandit/renewal/maintenance-renewal-like, but best CO variants usually remain below strong baselines. Maze is fine in the small visible case; latent is inconclusive under the shortened timeout-safe cap; maintenance middle requires longer-horizon phase/timing analysis rather than short-prefix interpretation.



### 2026-05-25 causal investigation + generic contract-vocabulary adjustment

A targeted causal investigation found one safe non-problem-specific correction: public problem-contract vocabulary used by shape derivation was too coarse. `drift=none` and `commitment_cost=medium_to_high` now survive normalization instead of collapsing to `unknown`; `shape_prior6` maps them to generic public regime pressures. This is not performance tuning and does not change canonical shapes based on results. See `PASS1_CAUSAL_INVESTIGATION_ADJUSTMENT_REPORT_2026-05-25.md`.

## 2026-05-25 targeted failure-cause audit

Added `pass1_targeted_failure_cause_audit_v1` to separate current weak CO-vs-STOA performance into bandit exploration/evidence-cadence, renewal recurrence/phase-retention, and maintenance longer-horizon gate/readout timing causes. This is diagnostic only: no kernel mechanism, problem-specific rule, or performance tuning was added.


## Relation-field concentration / function-like collapse update (2026-05-25)

The repo now includes a bounded first-pass treatment of function-like mappings as earned collapses of public relation-fields under shape/gauge. Theory anchors: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md` and `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`. Kernel contract: `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`. Runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`, consumed by RelationSurface/DynamicShapeField. This is telemetry and shape evidence, not a full probabilistic relation algebra and not an action policy.


## Domain-relative coarseness update (2026-05-25)

Added `DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md` plus theory/doc/code support for bounded domain-relative coarseness: `coarseness_radius` remains the global fallback, while `coarseness_by_domain` records active public relation/burden-domain resolution. This is telemetry/control-gauge support, not a new action policy.
