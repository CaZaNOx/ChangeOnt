# Canonical Structure Map

This file maps the current ChangeOnt source chain from conceptual theory to kernel docs, code, and diagnostics. It is not a new doctrine; it is an index for onboarding and maintenance.

## 1. Source chain

```text
TheoryOfChange_main/
→ ChangeOntCode/docs/kernel_spec/
→ ChangeOntCode/agents/co/
→ ChangeOntCode/agents/co/tests/ and ChangeOntCode/experiments/studies/
```

Meaning:

```text
TheoryOfChange_main establishes the conceptual chain.
Kernel docs translate the relevant part of that chain into an operational target.
Code implements the operational target.
Diagnostics check whether the implementation still matches the target.
Empirical studies may test usefulness only after the structural path is clean.
```

## 2. Canonical theory locations

```text
TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md
  Current reference stack into the theory graph.

TheoryOfChange_main/01_Statements/
  Statement-level derivations, clarifications, definitions, assumptions,
  corollaries, counterfactuals, and foundational truths.

TheoryOfChange_main/03_Derivation/graph.mmd
TheoryOfChange_main/03_Derivation/graph.yaml
  Overview graph artifacts for the statement network.

TheoryOfChange_main/06_Summaries/
  Human-readable summary guides. Use summaries as aids, not as replacements
  for the referenced statement files when precision matters.
```

## 3. Kernel-doc reading anchors

```text
ChangeOntCode/docs/kernel_spec/00_INDEX.md
  Canonical clean-set index.

ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
  Reading order for implementation work.

ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
  Target runtime architecture.

ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
  Ledger of conceptual closures and remaining open boundaries.

ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
  Gate that marks the certified docs target used for code audit.
```

## 4. Docs-to-code map

| Kernel responsibility | Primary docs | Primary code | Primary diagnostics |
|---|---|---|---|
| Boundary / public translation | `16_TRANSLATOR_BOUNDARY_CONTRACT.md`, `77_PUBLIC_BURDEN_EFFECT_SCHEMA.md`, `08_TRANSLATORS/README.md` | `agents/co/boundary/`, `agents/co/adapters/` | `problem_contract_invariants.py`, `family_packet_alignment_invariants.py`, `relation_surface_public_effect_invariants.py` |
| Shape controls / regime basis | `34_CANONICAL_PROBLEM_DEFINITION_AND_PLACEMENT_BASIS.md`, `74_SIX_QUESTION_SHAPE_PRIOR.md`, `100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md` | `agents/co/placement/` | `shape_prior6_contract_invariants.py`, `shape_prior6_active_path_invariants.py` |
| Candidate publication | `44_CANONICAL_CANDIDATE_SURFACE.md`, `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md` | `agents/co/runtime/surfaces/candidate_surface.py`, `continuation_state.py` | `candidate_surface_publication_invariants.py`, `continuation_state_invariants.py` |
| Burden operations | `84_BURDEN_OPERATION_ALGEBRA.md`, `86_MINIMAL_BURDEN_FORMAL_SKELETON.md`, `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md` | candidate/relation/field row carriers in `agents/co/runtime/surfaces/` | `kernel_structure_carrier_alignment_invariants.py`, `burden_relation_microdiagnostics.py` |
| Relation derivation | `80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md`, `87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md`, `99_RELATION_ALGEBRA_TARGET_STATE.md` | `agents/co/runtime/surfaces/relation_surface.py` | `relation_surface_public_effect_invariants.py`, `relation_path_trace_diagnostics.py` |
| RecursiveContinuationField | `47_RECURSIVE_CONTINUATION_FIELD.md`, `48_RECURSIVE_CONTINUATION_FIELD_INVARIANTS_AND_NOVELTY_BOUNDARY.md`, `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md`, `50_RECURSIVE_CONTINUATION_FIELD_IMPLEMENTATION_READINESS.md` | `agents/co/runtime/surfaces/continuation_field.py` | `recursive_continuation_field_invariants.py`, `recursive_continuation_field_relation_support_invariants.py` |
| Collapse certificate | `91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md`, `85_RELATION_TO_COLLAPSE_DIAGNOSTIC_CONTRACT.md` | `agents/co/runtime/surfaces/collapse_certificate.py` | `collapse_certificate_readout_invariants.py`, `structural_trace_validation_invariants.py` |
| Final readout | `43_CANONICAL_COMMITMENT_RULE.md`, `42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md`, `78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md` | `agents/co/runtime/surfaces/commitment_surface.py` (final readout), `agents/co/core/combinators/C_pipeline.py` (orchestrator only) | `commitment_surface_readout_invariants.py`, `no_classical_fallback_fail_closed_invariants.py`, `certified_runtime_alignment_invariants.py`, `code_vs_docs_pipeline_compliance_invariants.py` |
| Structural validation | `89_RELATION_PATH_TRACE_VALIDATION.md`, `92_ARCHITECTURE_ACCEPTANCE_AUDITS.md`, `94_REAL_TRACE_STRUCTURAL_VALIDATION_AND_FORMULA_GROUNDING.md` | `experiments/studies/structural_trace_validation_v1.py` | `structural_trace_validation_invariants.py`, `relation_path_trace_diagnostics.py` |

## 5. Root reports for this snapshot

```text
research_reports/2026-05-06/DOCS_CERTIFICATION_PASS_2026-05-06.md
  Documents the certified canonical docs target.

research_reports/2026-05-06/CODE_DOC_FULL_ALIGNMENT_2026-05-06.md
  Documents the code/docs alignment pass before the later structural formula fix.

research_reports/2026-05-06/VALIDATION_PACK_REPORT_2026-05-06.md
  Documents validation-pack results and remaining watchpoints at that time.

research_reports/2026-05-06/STRUCTURAL_TRACE_AND_FORMULA_HOTSPOT_REVIEW_2026-05-06.md
  Documents the latest structural/formula fix: certificate gates block dominance-style
  commitment when non-ready certificates still carry blocker/recursion pressure.
```

One handover-mentioned report name was not present exactly in the uploaded artifact:

```text
KERNEL_STRUCTURE_CARRIER_ALIGNMENT_FIXES_2026-05-06.md
```

Equivalent carrier-alignment material appears to be represented by the kernel docs and tests around `95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md` and `kernel_structure_carrier_alignment_invariants.py`, but this map does not claim the missing report exists.

## 6. Validation status boundary

Current structural checks can show that tested code paths preserve the architecture contracts. They do not show:

```text
- benchmark superiority;
- final formula grounding;
- final quotient tolerance beyond first-pass public residual-profile helper;
- final recursion scheduler correctness;
- novelty against all known algorithms;
- consciousness or subjectivity results.
```


## 7. Full audit record

```text
research_reports/2026-05-15/FULL_REPO_AUDIT_REPORT_2026-05-15.md
  Records the full repo audit pass, including TheoryOfChange_main validation fixes, no-fallback code fix, pycache removal, commands run, and remaining watchpoints.


research_reports/2026-05-15/SEMANTIC_RELEVANCE_AUDIT_REPORT_2026-05-15.md
  Records the stricter semantic relevance audit: file classification, active-route deep checks, derivation graph repair, shared fail-closed adapter action validation, and remaining limits.

research_reports/2026-05-15/SEMANTIC_RELEVANCE_AUDIT_LEDGER_2026-05-15.json
  Machine-readable classification/read-depth ledger. It is an audit aid, not proof that every historical or exploratory file was philosophically rederived line by line.
```

## 2026-05-16 stage-gate baseline

The latest validation/freeze artifacts are:

- `STRUCTURAL_BASELINE_FREEZE_2026-05-16.md`
- `FORMULA_COEFFICIENT_LEDGER_2026-05-16.md`
- `research_reports/2026-05-16/SYSTEMATIC_MECHANISM_ABLATION_REVIEW_2026-05-16.md`
- `research_reports/2026-05-16/REAL_FAMILY_MANUAL_TRACE_REVIEW_REPORT_2026-05-16.md`
- `research_reports/2026-05-16/FROZEN_EMPIRICAL_SANITY_SMOKE_REPORT_2026-05-16.md`
- `research_reports/2026-05-16/STAGE_GATE_EXECUTION_REPORT_2026-05-16.md`

Interpretation boundary: these are structural/formula/runtime-sanity artifacts. They do not prove CO, RCF novelty, or empirical usefulness.

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


- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md` — explicit derivation of shape, CO-space, directed unfolding, tension/burden, coarseness, point-as-ball, and dynamic shape update as the target for the first-pass runtime carrier.


Dynamic shape / coarseness target:
- `TheoryOfChange_main/01_Statements/02_Outer_Formation/022A_S-DR-shape-space-directed-unfolding-from-change.md` derives local shape, CO-space, directed unfolding, coarseness, point-as-ball, and dynamic shape update as a target.
- `ChangeOntCode/docs/kernel_spec/103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` specifies what the first-pass persistent DynamicShapeField may update.
- `ChangeOntCode/docs/kernel_spec/104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md` lists microcase gates now backed by first-pass structural tests.
- Current runtime now implements first-pass persistent dynamic shape state in `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py`, while retaining static shape prior and local shape-gauged resolver timing as separate mechanisms.


## 2026-05-21 multi-step continuation-memory update

```text
research_reports/2026-05-21/MULTI_STEP_CONTINUATION_IDENTITY_UPDATE_2026-05-21.md
ChangeOntCode/agents/co/runtime/surfaces/continuation_state.py
ChangeOntCode/agents/co/tests/multi_step_continuation_identity_invariants.py
ChangeOntCode/experiments/studies/multi_step_continuation_identity_probe_v1.py
```

This is first-pass structural support for branch≠action persistence.  It is not yet full sequence-level branch composition.


## 2026-05-21 quotient/equivalence first-pass helper

```text
Theory / target:
- ChangeOntCode/docs/kernel_spec/97_QUOTIENT_EQUIVALENCE_TARGET_STATE.md

Runtime carrier:
- ChangeOntCode/agents/co/runtime/surfaces/quotient_equivalence.py
- ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py

Diagnostics:
- ChangeOntCode/agents/co/tests/quotient_equivalence_first_pass_invariants.py
- ChangeOntCode/experiments/studies/quotient_equivalence_first_pass_probe_v1.py
- research_reports/2026-05-21/QUOTIENT_EQUIVALENCE_FIRST_PASS_PROBE_REPORT_2026-05-21.md
```

Boundary: quotienting is conservative and public-residual-profile based.  It is not scalar similarity, weak competition, action-label grouping, topology editing, or state-abstraction proof.


## 2026-05-21 recursion scheduler first-pass update

`ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py` now provides a first-pass bounded public structural recursion-demand scheduler between RCF and CollapseCertificate. It is not hidden lookahead, not an action selector, and not final recursion theory. See `research_reports/2026-05-21/RECURSION_SCHEDULER_FIRST_PASS_PROBE_REPORT_2026-05-21.md`.

## Current-kernel diagnostic map

```text
Concept/doc target: complete rough first-pass kernel before final refinement.
Code/study: ChangeOntCode/experiments/studies/current_kernel_diagnostic_map_v1.py
Invariant: ChangeOntCode/agents/co/tests/current_kernel_diagnostic_map_invariants.py
Report: research_reports/2026-05-22/CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md
Purpose: map mechanism visibility/action sensitivity across current families under DynamicShapeField / quotient / scheduler ablations.
Boundary: diagnostic only, not benchmark evidence.
```


## Targeted hardening report

- `research_reports/2026-05-22/CURRENT_KERNEL_TARGETED_HARDENING_REPORT_2026-05-22.md` records the DynamicShapeField readout-visibility fix, recursion provenance split, and deeper diagnostic trace logging.

## 2026-05-22 quotient / maintenance audit reports

Additional first-pass audit reports:

```text
research_reports/2026-05-22/QUOTIENT_ACCEPT_REJECT_AUDIT_REPORT_2026-05-22.md
research_reports/2026-05-22/MAINTENANCE_ACTION_INSENSITIVITY_AUDIT_REPORT_2026-05-22.md
```

Code/studies:

```text
ChangeOntCode/experiments/studies/quotient_accept_reject_audit_v1.py
ChangeOntCode/experiments/studies/maintenance_action_insensitivity_audit_v1.py
ChangeOntCode/agents/co/tests/quotient_accept_reject_audit_invariants.py
ChangeOntCode/agents/co/tests/maintenance_action_insensitivity_audit_invariants.py
```

Boundary: both are audit-only. They do not tune, benchmark, or prove CO. They narrow the next work to generic readout dominance/pre-blocking resolver microcases before robot/sim.

## 2026-05-22 Dominance/readout-swamping audit additions

- `research_reports/2026-05-22/DOMINANCE_READOUT_SWAMPING_AUDIT_UPDATE_2026-05-22.md` — compact handoff for the generic readout-swamping audit.
- `research_reports/2026-05-22/DOMINANCE_READOUT_SWAMPING_AUDIT_REPORT_2026-05-22.md` — report generated by `experiments.studies.dominance_readout_swamping_audit_v1`.
- `research_reports/2026-05-22/PREBLOCKING_RESOLVER_CROSS_FAMILY_MICROCASE_PROBE_REPORT_2026-05-22.md` — report generated by `experiments.studies.preblocking_resolver_cross_family_microcase_probe_v1`.
- `ChangeOntCode/experiments/studies/dominance_readout_swamping_audit_v1.py` — generic audit over current-family diagnostic traces.
- `ChangeOntCode/experiments/studies/preblocking_resolver_cross_family_microcase_probe_v1.py` — anonymous cross-family shape-profile microcases for pre-blocking resolver timing.
- `ChangeOntCode/agents/co/tests/dominance_readout_swamping_audit_invariants.py` and `preblocking_resolver_cross_family_microcase_invariants.py` — claim-boundary and negative-control invariants.

These additions do not change commitment behavior except for diagnostic component telemetry. They identify a generic carrier-gate/readout calibration watchpoint and explicitly forbid family-specific repair rules.

## 2026-05-22 generic carrier-gate calibration

A small generic readout calibration was applied after the dominance/readout-swamping audit: `preblocking_carrier_shape_urgency_weight` moved from `0.34` to `0.37` in `CommitmentSurface`. This is not maintenance tuning. It makes public shape urgency slightly more able to lower the pre-blocking carrier-pressure gate before resolver comparison.

See `research_reports/2026-05-22/GENERIC_CARRIER_GATE_CALIBRATION_REPORT_2026-05-22.md`. The cross-family pre-blocking microcases now report `cases=6`, `passed=5`, `observed=1`, `watchpoints=0`, while low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected. Current-family diagnostic map still runs `40/40` successfully. Maintenance action-prefix insensitivity remains unresolved (`insensitive_comparison_count=8`, `sensitive_comparison_count=0`).

Next step: freeze the Pass-1 kernel closure candidate, rerun mechanism/evaluation diagnostics, and decide whether remaining readout swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure. Do not add robot/sim or family-specific rules yet.

## 2026-05-22 sequence/readout trace audit additions

Audit-only additions after generic carrier-gate calibration:

```text
ChangeOntCode/experiments/studies/sequence_level_continuation_composition_audit_v1.py
ChangeOntCode/experiments/studies/generic_readout_swamping_trace_audit_v1.py
ChangeOntCode/agents/co/tests/sequence_level_continuation_composition_audit_invariants.py
ChangeOntCode/agents/co/tests/generic_readout_swamping_trace_audit_invariants.py
research_reports/2026-05-22/SEQUENCE_LEVEL_CONTINUATION_COMPOSITION_AUDIT_REPORT_2026-05-22.md
research_reports/2026-05-22/GENERIC_READOUT_SWAMPING_TRACE_AUDIT_REPORT_2026-05-22.md
```

These files are diagnostic/audit artifacts, not final kernel evidence. They now establish that public burden-domain continuation memory exists and generic sequence-composition carriers are present, while behavioral adequacy remains pending.


## 2026-05-22 kernel Pass-1 closure candidate

Generic sequence-level continuation composition has been implemented and wired. See `research_reports/2026-05-22/KERNEL_PASS1_CLOSURE_CANDIDATE_REPORT_2026-05-22.md`, `research_reports/2026-05-22/SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`, and the updated sequence/readout audits.

Current status: the known rough kernel mechanism set is now present as a Pass-1 closure candidate, not a final kernel. Next work should freeze/evaluate rather than add mechanisms: sequence on/off diagnostics, adapter-boundary tests, coefficient sensitivity, quotient false/missed quotient audit, and a current-family failure map. Robot/sim expansion remains premature until this evaluation is complete.
