# Publication Target Gap Ledger — 2026-05-21

## Purpose

The final target is not merely a runnable repo.  It is a publishable CO theory
paper/essay/book-level work, possibly with a separate code/results paper, that
survives serious criticism and shows non-trivial added value over competitors.

This ledger records what is missing relative to that final target.

## Final target shape

```text
philosophical motivation and justification
→ clear statement of CO
→ contestor/rival-theory handling
→ rigorous concept derivation without obvious gaps
→ operational concepts justified from theory
→ implementation explanation
→ SOTA/baseline comparison
→ difficult-domain evidence, especially robot/simulation-like problems
→ honest failure/novelty analysis
```

## Current publication gaps

| Gap | Current repo status | Required before publication |
|---|---|---|
| Critic-facing thesis | scattered across `_main`, docs, reports | one clear thesis and argument map |
| Epistemic-to-ontological bridge | present but still fragile | precise wording of what the immediate datum licenses and what extra argument is needed |
| Rival philosophical comparison | partial | serious comparison to process philosophy, pragmatism, enactivism, dynamical systems, active inference, etc. |
| Rival algorithmic comparison | initial doc exists | stronger comparison to MDP/POMDP, DP, MCTS, options, successor representations, belief-state methods, state abstraction, control theory |
| Glossary | distributed | critic-facing glossary: definition, need, what it is not, closest analogue, runtime carrier |
| Formula grounding | ledger exists but incomplete | all behavior-affecting formulas classified as derived/provisional/empirical/diagnostic |
| Dynamic shape | first-pass implementation now exists | family ablations, formula grounding, failure cases |
| Multi-step branch identity | first-pass partial | public burden-domain memory can cross action expressions; full sequence-level branch composition needed for robot/sim and strong branch≠action claims |
| Quotient/equivalence | first-pass partial | public residual-profile helper exists; final tolerance, real-trace false/missed quotient analysis, and reduction against state abstraction remain open |
| Robot/sim evidence | absent | lawful first-pass problem definitions, translators, baselines, diagnostics, and honest results |
| Evidence ledger | reports exist | one claim-to-evidence table separating structural probes, smoke runs, benchmarks, and failures |

## Reader-friendliness gaps

```text
- root remains report-heavy and dated-report-heavy;
- current docs are AI-onboarding friendly but not yet human-paper friendly;
- some concepts use internal names before giving critic-facing equivalents;
- derivation status needs clearer labels: strict derivation vs definition vs operational hypothesis;
- open points need continued maintenance whenever implementation state changes.
```

## Non-negotiable publication rule

No final paper claim may outrun this chain:

```text
theory derivation
→ operational necessity
→ code carrier
→ structural diagnostic
→ fair empirical comparison
→ rival-method distinction
```

If any link is missing, the claim must be weakened or marked as future work.


## 2026-05-21 recursion scheduler first-pass update

`ChangeOntCode/agents/co/runtime/surfaces/recursion_scheduler.py` now provides a first-pass bounded public structural recursion-demand scheduler between RCF and CollapseCertificate. It is not hidden lookahead, not an action selector, and not final recursion theory. See `research_reports/2026-05-21/RECURSION_SCHEDULER_FIRST_PASS_PROBE_REPORT_2026-05-21.md`.

## 2026-05-22 diagnostic-map implication for publication target

The current-kernel diagnostic map is useful for the eventual paper only as an internal evidence-preparation artifact. It shows whether recent CO mechanisms are visible and behavior-causal under ablation, but it is not publication evidence.

Publication relevance: it sharpens future claims by identifying which mechanisms currently change behavior and which mostly change telemetry. This helps prevent the final manuscript from claiming operational consequences before they are shown.

Remaining publication gap: the project still needs longer frozen studies, stronger baselines, robot/simulation domains, and rival-framework comparison before any claim that CO has non-trivial added value over competitors.

## 2026-05-22 watchpoint audit publication boundary

`research_reports/2026-05-22/CURRENT_KERNEL_WATCHPOINT_AUDIT_REPORT_2026-05-22.md` is useful for publication preparation only as a negative/disciplinary artifact: it prevents premature claims. It shows that the first-pass kernel has visible mechanisms, but also that DynamicShapeField readout visibility, recursion-pressure provenance, quotient miss auditing, and diagnostic trace depth are not yet publication-grade.

Publication implication:

```text
Do not claim that dynamic shape, recursion demand, or quotient/equivalence have mature operational evidence yet.
Do not move to robot/simulation evidence as if the current kernel is already clean.
First fix the identified alignment gaps, then rerun the current-family diagnostic map with deeper traces.
```


## 2026-05-22 publication-relevance update

The repo now has a clearer evidence trail for dynamic-shape readout visibility and recursion-provenance separation. This improves eventual critic-facing explainability, but it still does not support publication claims of empirical usefulness or novelty. Remaining critic-facing gaps: quotient equivalence must be auditable, and maintenance action-insensitivity must be explained before robot/sim claims.

## 2026-05-22 quotient / maintenance audit publication boundary

The new quotient and maintenance audits improve critic-facing honesty, but they do not create publication evidence.

Allowed wording:

- quotient equivalence is now provenance-auditable in capped current-family diagnostics;
- no duplicate-signature missed-quotient bug was found in that diagnostic;
- maintenance action-insensitivity is a known unresolved first-pass watchpoint.

Disallowed wording:

- quotient/equivalence is final;
- maintenance behavior validates CO;
- action-insensitivity proves correct non-decisiveness;
- maintenance should be fixed with a family-specific repair rule.

Next publication-relevant gap: demonstrate, with generic microcases and cross-family traces, whether readout dominance/pre-blocking resolver timing is a principled CO mechanism or a heuristic swamping artifact.

## 2026-05-22 — Publication relevance: readout-swamping gap

A critic-facing account cannot yet claim that pre-blocking resolver timing is fully grounded. The latest audit shows that generic support/stability/field mass can dominate burden/resolver structure and that the carrier-pressure gate has a borderline calibration watchpoint. This is useful evidence of self-audit, but the paper must not claim mature collapse/readout law until the generic calibration is either justified or corrected and ablated across families.

## 2026-05-22 generic carrier-gate calibration

A small generic readout calibration was applied after the dominance/readout-swamping audit: `preblocking_carrier_shape_urgency_weight` moved from `0.34` to `0.37` in `CommitmentSurface`. This is not maintenance tuning. It makes public shape urgency slightly more able to lower the pre-blocking carrier-pressure gate before resolver comparison.

See `research_reports/2026-05-22/GENERIC_CARRIER_GATE_CALIBRATION_REPORT_2026-05-22.md`. The cross-family pre-blocking microcases now report `cases=6`, `passed=5`, `observed=1`, `watchpoints=0`, while low-urgency, weak-resolver, and large-carrier-advantage negative controls remain protected. Current-family diagnostic map still runs `40/40` successfully. Maintenance action-prefix insensitivity remains unresolved (`insensitive_comparison_count=8`, `sensitive_comparison_count=0`).

Next step: freeze the Pass-1 kernel closure candidate, rerun mechanism/evaluation diagnostics, and decide whether remaining readout swamping is legitimate non-decisiveness, weak sequence-readout consumption, or a generic readout-design failure. Do not add robot/sim or family-specific rules yet.

## 2026-05-22 — Publication relevance: sequence/readout trace audit

The sequence/readout audit sharpens a critic-facing gap. The repo can now say that continuation memory is no longer purely native-action-keyed, because public burden-domain keys group multiple expressions. It still cannot claim mature branch identity across ordered action phases. The trace now has explicit generic sequence-composition carriers, but claims such as `INSPECT -> REPAIR -> RUN` as one higher continuation remain unproven behavior, not mature evidence.

Publication consequence: a paper can discuss ordered continuation composition as a required CO operational concept, but cannot claim the current runtime implements it. Before robot/simulation evidence becomes meaningful, the project needs sequence on/off ablations and audits showing when generic public sequence-phase evidence changes behavior for structural reasons and when it remains non-decisive.


## 2026-05-22 kernel Pass-1 closure candidate

Generic sequence-level continuation composition has been implemented and wired. See `research_reports/2026-05-22/KERNEL_PASS1_CLOSURE_CANDIDATE_REPORT_2026-05-22.md`, `research_reports/2026-05-22/SEQUENCE_COMPOSITION_MICROCASE_PROBE_REPORT_2026-05-22.md`, and the updated sequence/readout audits.

Current status: the known rough kernel mechanism set is now present as a Pass-1 closure candidate, not a final kernel. Next work should freeze/evaluate rather than add mechanisms: sequence on/off diagnostics, adapter-boundary tests, coefficient sensitivity, quotient false/missed quotient audit, and a current-family failure map. Robot/sim expansion remains premature until this evaluation is complete.


## Update — 2026-05-25

Publication-facing evidence remains insufficient. The causal investigation found a generic shape-path vocabulary defect and fixed it, but did not justify a new mechanism or performance tuning. The paper claim must still say that performance deficits are multi-causal and unresolved.


## Relation-field concentration / function-like collapse update (2026-05-25)

The repo now includes a bounded first-pass treatment of function-like mappings as earned collapses of public relation-fields under shape/gauge. Theory anchors: `TheoryOfChange_main/01_Statements/02_Outer_Formation/022B_S-DR-relation-field-function-like-collapse-from-shape.md` and `TheoryOfChange_main/02_Concepts/C-relation-field-function-like-collapse.md`. Kernel contract: `ChangeOntCode/docs/kernel_spec/106_RELATION_FIELD_FUNCTION_LIKE_COLLAPSE.md`. Runtime carrier: `ChangeOntCode/agents/co/runtime/surfaces/relation_field_concentration.py`, consumed by RelationSurface/DynamicShapeField. This is telemetry and shape evidence, not a full probabilistic relation algebra and not an action policy.


## Domain-relative coarseness update (2026-05-25)

Added `research_reports/2026-05-25/DOMAIN_RELATIVE_COARSENESS_FIELD_UPDATE_2026-05-25.md` plus theory/doc/code support for bounded domain-relative coarseness: `coarseness_radius` remains the global fallback, while `coarseness_by_domain` records active public relation/burden-domain resolution. This is telemetry/control-gauge support, not a new action policy.
