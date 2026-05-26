# First-Pass Completion Ledger — 2026-05-21

## Purpose

This ledger reframes the repo under the user's current development strategy:

```text
Pass 1: rough complete conceptual/code/problem-coverage pass.
Pass 2: refinement, hardening, critic-facing explanation, and stronger evidence.
Pass 3: publishable paper/book construction.
```

This repo is still in **Pass 1**.  The goal is not final elegance or empirical
proof.  The goal is to ensure that every concept/stage that CO needs exists at
least once in theory, docs, code, diagnostics, and problem coverage, so that the
second pass can refine a complete system rather than polish an incomplete one.

## Current first-pass status

| Area | Status | Notes |
|---|---|---|
| Change-first `_main` spine | present / needs refinement | Opening and outer-formation route exist.  The epistemic-to-ontological bridge still needs stronger critic-facing formulation. |
| Shape / CO-space / directed unfolding | present | `022A_S-DR-shape-space-directed-unfolding-from-change.md` derives first-pass shape, CO-space, coarseness, point-as-ball, and dynamic-shape target. |
| DynamicShapeField doctrine/spec | present | Docs `103` and `104` define public-trace-only implementation boundaries and microcase expectations. |
| DynamicShapeField runtime | first-pass implemented | `ChangeOntCode/agents/co/runtime/surfaces/dynamic_shape_field.py` persists local shape-state and deforms next-cycle controls only. |
| Dynamic shape microcases | present | `dynamic_shape_microcase_probe_v1.py` and `dynamic_shape_field_invariants.py` cover docs `103/104` cases structurally. |
| Dynamic shape ablation | present / minimal | `dynamic_shape_real_trace_ablation_v1.py` verifies state/control telemetry changes under public trace; no reward claim. |
| RelationSurface / public effects | present | Public-effect relation path is active and behavior-causal in prior probes. |
| RCF / continuation field | present / provisional | Relation-aware field exists; novelty and reduction against known algorithms remain unproven. |
| CollapseCertificate | present | Structured blockers/reasons exist. |
| CommitmentSurface | present | Certificate-aware, resolver-aware, fail-closed readout exists with local shape-gauged resolver timing. |
| Multi-step continuation identity | first-pass partial | Candidate continuation memory can now persist across different action expressions by public burden-domain key; generic sequence-level composition now has a first-pass implementation; behavioral sufficiency remains open. |
| Quotient/equivalence law | first-pass partial | `quotient_equivalence.py` derives conservative quotient/equivalence from public residual profiles; final tolerance and missed-quotient calibration remain open. |
| Recursion scheduler/budget | first-pass partial | `recursion_scheduler.py` derives bounded public structural recursion demand before certificates; actual multi-layer unfolding and real-trace calibration remain open. |
| Formula/coefficient grounding | incomplete | Ledger exists; DynamicShapeField update rates/effective-control deformation now need entries and sensitivity probes. |
| Current problem families | present | Bandit, renewal, maze, latent mechanism, maintenance/replacement exist as first-pass families. |
| Robot/simulation problems | pending | Should not be final-claim evidence until kernel integrity improves, but they belong in the first broad pass before final refinement. |
| Publication-facing theory | pending | Repo is internally navigable, not yet a critic-facing manuscript. |

## What changed in this update

```text
- Added first-pass persistent DynamicShapeField runtime carrier.
- Wired CandidateEvidenceSurface to use DynamicShapeField state for next-cycle effective controls.
- Added dynamic shape microcase invariants and probe.
- Added dynamic shape real-trace ablation probe.
- Added first-pass multi-step continuation-memory identity: public burden-domain memory can persist across different action expressions without collapsing RelationSurface branch IDs.
- Added first-pass quotient/equivalence helper: conservative public-residual-profile quotienting with false-quotient invariants.
- Added first-pass recursion-demand scheduler: dense equivalent regions contract, dense non-equivalent/sparse high-consequence unresolved cases raise bounded recursion telemetry.
- Updated stale open-points language from "derive contract" to "harden implementation/formula grounding".
- Updated kernel-doc index/reading guide to include first-pass dynamic shape.
```

## Current implementation boundary

DynamicShapeField currently:

```text
- uses public candidate rows, public relations, RCF/certificate telemetry, and explicit public observation/feedback annotations;
- persists coarseness_radius, projection_horizon, relation_density, burden_persistence, hiddenness_pressure, admissibility_pressure, and gauge_confidence;
- logs before/evidence/delta/after telemetry;
- can be disabled independently for ablation;
- deforms next-cycle controls but does not select actions directly.
```

DynamicShapeField does **not**:

```text
- use hidden state;
- read native action names;
- use reward hindsight by itself;
- edit topology or legal action domains;
- inspect baseline/DP values;
- prove CO works;
- establish final shape/space mathematics.
```

## Immediate remaining Pass-1 work

1. **Recursion scheduler calibration beyond first-pass helper**
   - current helper derives bounded public structural recursion demand;
   - still audit false-positive and false-negative demand across real traces;
   - still distinguish scheduler pressure from ordinary lookahead/search;
   - actual second-layer unfolding expansion remains unimplemented.

2. **Quotient/equivalence calibration beyond first-pass helper**
   - current helper handles conservative public residual-profile equivalence;
   - still measure missed quotient and false quotient behavior across real traces;
   - keep tolerance policy frozen before empirical evidence;
   - do not use scalar-score similarity or weak competition as quotient basis.

3. **Multi-stage continuation composition**
   - current update supports public burden-domain continuation memory across different action expressions;
   - still define sequence-level branches across different burden domains, e.g. exposure → relief → stable operation;
   - test cases such as `inspect → repair → run` as one higher continuation.

4. **Dynamic shape across real families**
   - run static-vs-dynamic ablations across all current families;
   - check whether DynamicShapeField changes behavior or only telemetry;
   - report either result honestly.

5. **Formula ledger update**
   - add entries for DynamicShapeField alpha, projection/coarseness formulas, hiddenness/admissibility pressure, and effective-control deformation;
   - mark all as first-pass/provisional unless derived more deeply.

6. **Robot/simulation first-pass problem design**
   - define lawful translator boundaries before implementation;
   - target changing affordance, partial exposure, embodied constraint, and dynamic coarsening;
   - avoid adding robot/sim as benchmark theatre before kernel integrity is clear.

7. **Conceptual completeness audit**
   - check whether the current concept set is enough for robot/sim domains;
   - specifically inspect projection horizon, affordance, exposure, environment coupling, and branch identity.

8. **Publication scaffold**
   - later add a critic-facing argument map, claim ledger, rival matrix, glossary, and evidence ledger.

## Claim boundary

This update advances Pass 1.  It does not justify broad empirical claims, novelty claims, or publication claims.  It makes the rough system more complete so the next pass has a fuller object to refine.

## 2026-05-22 current-kernel diagnostic map

Added `current_kernel_diagnostic_map_v1.py` and `research_reports/2026-05-22/CURRENT_KERNEL_DIAGNOSTIC_MAP_REPORT_2026-05-22.md`. The study runs the rough first-pass kernel across the current active families/modes with generic mechanism ablations: full current kernel, static-shape only, no quotient, no scheduler, and all three recent mechanisms disabled.

Status: diagnostic only. The run is one seed with short capped horizons so it can be executed during cold takeover. It is not benchmark evidence. It showed that DynamicShapeField, quotient/equivalence, and RecursionScheduler are telemetry-visible under ablation. Behavioral sensitivity is uneven: bandit and latent mechanism traces changed; maze, renewal, and maintenance/replacement mostly showed telemetry changes without short-horizon action/metric changes. This becomes a Pass-1 watchpoint for real-trace audits before robot/sim expansion.

## 2026-05-22 current-kernel watchpoint audit

Added `current_kernel_watchpoint_audit_v1.py` and `research_reports/2026-05-22/CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md`. This did **not** change kernel behavior; it audited the diagnostic-map outputs and code paths to determine why some recent mechanisms change telemetry but not actions.

Audit status: Pass-1 watchpoints remain. The audit found two high-severity alignment gaps:

```text
1. DynamicShapeField is currently only partly readout-visible: CandidateSurface uses its effective controls, but CommitmentSurface shape-gauged timing still reads static direct controls.
2. Recursion demand provenance is ambiguous: high recursion demand can appear in weak-decision-slot-only traces through inherited RCF field_recursion_budget.
```

Therefore robot/simulation expansion should wait until these two gaps and deep row-level trace logging are addressed.


## 2026-05-22 targeted hardening status

Completed first-pass hardening of three diagnostic watchpoints: DynamicShapeField effective controls are now readout-visible in CommitmentSurface; RecursionScheduler publishes split provenance channels and only structural demand feeds certificate recursion; current-family diagnostics now include row-level trace samples. This does not complete Pass 1: quotient real-trace audit and maintenance action-insensitivity remain open.

## 2026-05-22 quotient / maintenance audits

Added audit-only studies after targeted hardening:

- `quotient_accept_reject_audit_v1.py`: quotient provenance is now row-visible; no duplicate-signature missed-quotient bug was found in the capped diagnostic; quotient tolerance remains conservative and unfinished.
- `maintenance_action_insensitivity_audit_v1.py`: maintenance middle/renewal_like action-prefix insensitivity is confirmed; current evidence points to generic readout dominance / incomplete pre-blocking resolver timing, not a maintenance-specific fix.

Pass-1 implication: the rough kernel has enough trace visibility to continue auditing, but not enough to move to robot/sim. Next required slice is generic dominance/readout-swamping audit and cross-family pre-blocking resolver microcases.

## 2026-05-22 — Dominance/readout-swamping audit

Added a generic dominance/readout-swamping audit and cross-family pre-blocking resolver microcase probe. No behavior change was made beyond readout component telemetry and diagnostic logging. The audit identifies a generic carrier-gate/readout calibration site: carrier branches can remain selected despite resolver alternatives because the pre-blocking carrier-pressure gate is too strict in some borderline high-urgency cases, while support/stability/field mass can swamp burden/blocker penalties. This remains an open first-pass kernel watchpoint.

## 2026-05-22 generic carrier-gate calibration

A small generic readout calibration was applied after the dominance/readout-swamping audit: `preblocking_carrier_shape_urgency_weight` moved from `0.34` to `0.37` in `CommitmentSurface`. This is not maintenance tuning. It makes public shape urgency slightly more able to lower the pre-blocking carrier-pressure gate before resolver comparison.

See `research_reports/2026-05-22/GENERIC_CARRIER_GATE_CALIBRATION_REPORT_2026-05-22.md`. The cross-family pre-blocking microcases now report `cases=6`, `passed=5`, `observed=1`, `watchpoints=0`, while low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected. Current-family diagnostic map still runs `40/40` successfully. Maintenance action-prefix insensitivity remains unresolved (`insensitive_comparison_count=8`, `sensitive_comparison_count=0`).

Next step: freeze the Pass-1 kernel closure candidate, rerun mechanism/evaluation diagnostics, and decide whether remaining readout swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure. Do not add robot/sim or family-specific rules yet.

## 2026-05-22 — Sequence/readout trace audit

Added audit-only studies after generic carrier-gate calibration:

- `sequence_level_continuation_composition_audit_v1.py`: confirms first-pass public burden-domain memory groups different action expressions, and explicit ordered sequence-composition fields now exist in current diagnostic row telemetry (`sequence_field_rows = 511`; active rows = 176). This means branch≠action is improved but not complete: the kernel still lacks a generic way to compose phases such as exposure → relief → stabilized operation.
- `generic_readout_swamping_trace_audit_v1.py`: confirms remaining generic readout-swamping watchpoints. Support/stability/field mass remains high relative to penalties in many selected commitments, and carrier-with-resolver-alt cases often remain without shape-gauged resolver timing.

Pass-1 implication: the rough kernel is now a closure candidate. The next move is evaluation/freeze discipline: sequence on/off diagnostics, readout-swamping checks, and all-family mechanism maps. Robot/sim expansion remains premature until this evaluation is complete.


## 2026-05-22 kernel Pass-1 closure candidate

Generic sequence-level continuation composition has been implemented and wired. See `research_reports/2026-05-22/KERNEL_PASS1_CLOSURE_CANDIDATE_REPORT_2026-05-22.md`, `research_reports/2026-05-22/SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`, and the updated sequence/readout audits.

Current status: the known rough kernel mechanism set is now present as a Pass-1 closure candidate, not a final kernel. Next work should freeze/evaluate rather than add mechanisms: sequence on/off diagnostics, adapter-boundary tests, coefficient sensitivity, quotient false/missed quotient audit, and a current-family failure map. Robot/sim expansion remains premature until this evaluation is complete.

## 2026-05-22 Pass-1 kernel closure audit

Added `research_reports/2026-05-22/PASS1_KERNEL_CLOSURE_AUDIT_REPORT_2026-05-22.md` and `ChangeOntCode/experiments/studies/pass1_kernel_closure_audit_v1.py`. Verdict: rough known mechanism set present and diagnostic runs succeed, but this is only a closure candidate. Pass 1 is not complete as an evaluated system until blockers are characterized or fixed without adding unjustified mechanisms.

## 2026-05-25 context-conditioned expectation audit
Added `context_conditioned_expectation_audit_v1`. Status: diagnostic-only, no kernel behavior change. It classifies each full-current decision by public shape/gauge context and local structural triggers before judging mechanism relevance. Finding: aggregate action sensitivity was too coarse; sequence/quotient/recursion strong contexts show mostly action or gate/readout consumption, but DynamicShapeField has a medium under-consumption watchpoint.

## Pass-1 all-problem CO vs STOA/baseline comparison — 2026-05-25

A bounded all-current-problem comparison has been run and recorded in `research_reports/2026-05-25/PASS1_ALL_PROBLEM_STOA_COMPARISON_REPORT_2026-05-25.md` with raw outputs under `ChangeOntCode/outputs/pass1_all_problem_stoa_comparison_v1/`. It derives public shape reports for each active family/mode before comparing CO against repo-available public baselines/STOA-style baselines. This is diagnostic only: small seed count, capped horizons, no post-result tuning, and not publication-grade evidence. Results currently show CO is mostly below best public baselines, with a limited favorable/tie pattern only in latent-mechanism success metrics under the bounded setup.

## Pass-1 factor / causal sweep — 2026-05-25

Added `ChangeOntCode/experiments/studies/pass1_factor_causal_sweep_v1.py` and report `research_reports/2026-05-25/PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md`. This is a bounded diagnostic follow-up to the all-problem CO vs STOA comparison. It varies generic mechanism toggles, dynamic-shape update rate, counterfactual public shape profiles, and readout resolver gates. It is not a tuning run and counterfactual shapes are not canonical. Main result: no single factor explains the current weak STOA comparison; shape variation explains substantial variance in bandit/renewal/maintenance-renewal-like, but best CO variants usually remain below strong baselines. Maze is fine in the small visible case; latent is inconclusive under the shortened timeout-safe cap; maintenance middle requires longer-horizon phase/timing analysis rather than short-prefix interpretation.



## Update — 2026-05-25 causal investigation adjustment

Pass-1 kernel closure remains a research candidate, not a release-ready kernel. One generic shape-path defect was fixed: legitimate public contract values no longer collapse to `unknown` before shape derivation. This improved placement fidelity for affected contracts but does not resolve the STOA performance gap.

## 2026-05-25 targeted failure-cause audit

Added `pass1_targeted_failure_cause_audit_v1` to separate current weak CO-vs-STOA performance into bandit exploration/evidence-cadence, renewal recurrence/phase-retention, and maintenance longer-horizon gate/readout timing causes. This is diagnostic only: no kernel mechanism, problem-specific rule, or performance tuning was added.


## Relation-field concentration / function-like collapse update (2026-05-25)

The repo now includes a bounded first-pass treatment of function-like mappings as earned collapses of public relation-fields under shape/gauge. Theory anchors: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md` and `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`. Kernel contract: `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`. Runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`, consumed by RelationSurface/DynamicShapeField. This is telemetry and shape evidence, not a full probabilistic relation algebra and not an action policy.


## Domain-relative coarseness update (2026-05-25)

Added `research_reports/2026-05-25/DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md` plus theory/doc/code support for bounded domain-relative coarseness: `coarseness_radius` remains the global fallback, while `coarseness_by_domain` records active public relation/burden-domain resolution. This is telemetry/control-gauge support, not a new action policy.
