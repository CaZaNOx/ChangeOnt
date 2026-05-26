# Pass-1 Kernel Closure Audit v1 — 2026-05-22

## Claim boundary

Freeze/evaluation audit only. It does not add a kernel mechanism, does not tune performance, does not constitute benchmark evidence, and does not prove CO's usefulness or novelty.

## Verdict

- Known rough mechanism files present: `True`.
- Pass-1 kernel closure candidate: `True`.
- Release-ready: `False`.
- Publication-ready: `False`.

Interpretation: the rough mechanism set is present, but this is not a clean release state. The correct state is to freeze the rough kernel for evaluation and treat the remaining findings as blockers/watchpoints, not as justification for hidden benchmark rescue patches.

## Mechanism presence

| mechanism file | present |
|---|---:|
| `candidate_surface` | True |
| `collapse_certificate` | True |
| `commitment_surface` | True |
| `dynamic_shape_field` | True |
| `quotient_equivalence` | True |
| `recursion_scheduler` | True |
| `relation_surface` | True |
| `sequence_composition` | True |

## Diagnostic map scope

Runs attempted: `48`; succeeded: `48`; failed: `0`.

Variants: `full_current`, `minimal_recent_core`, `no_quotient`, `no_scheduler`, `no_sequence`, `static_shape`.

## Mechanism visibility in full-current runs

- Full-current runs: `8`.
- Avg dynamic-shape-applied steps: `15.500`.
- Avg sequence-active steps: `9.250`.
- Avg sequence rows: `1.317`.
- Avg quotient rows: `0.768`.
- Avg recursion scheduler demand: `0.135`.

## Ablation sensitivity

### By ablation

| ablation | comparisons | families/modes with action diff | prefix action diffs | metric abs delta sum | sequence step delta | dynamic step delta |
|---|---:|---:|---:|---:|---:|---:|
| `minimal_recent_core` | 8 | 4 | 32 | 29.600 | -74 | -124 |
| `no_quotient` | 8 | 2 | 22 | 23.000 | 0 | 2 |
| `no_scheduler` | 8 | 2 | 17 | 5.600 | -2 | 0 |
| `no_sequence` | 8 | 1 | 5 | 2.000 | -74 | 2 |
| `static_shape` | 8 | 4 | 28 | 9.600 | -4 | -124 |

### By family/mode

| family/mode | ablation comparisons | comparisons with action diff | prefix action diffs |
|---|---:|---:|---:|
| `bandit::easy_public_bandit` | 5 | 3 | 21 |
| `latent_mechanism::easy_visible` | 5 | 3 | 32 |
| `latent_mechanism::hidden_depth2` | 5 | 4 | 39 |
| `maintenance_replacement::bandit_like` | 5 | 0 | 0 |
| `maintenance_replacement::middle` | 5 | 0 | 0 |
| `maintenance_replacement::renewal_like` | 5 | 0 | 0 |
| `maze::static_visible_5x5` | 5 | 2 | 10 |
| `renewal::noisy_renewal` | 5 | 1 | 2 |

## Blocking watchpoints

### P1A_RELEASE_NOT_READY_ARCHITECTURE_WATCHPOINTS — blocking-for-release

Evidence: architecture_acceptance_audit_v1 status=ACCEPTANCE_WATCHPOINTS_REMAIN

Interpretation: The closure candidate is not architecture-accepted; Pass-1 can proceed only as a diagnostic/research state.

### P1A_STRUCTURAL_TRACE_WATCHPOINTS_REMAIN — blocking-for-release

Evidence: structural_trace_validation_v1 status=PASS_WITH_WATCHPOINTS; cases_with_watchpoints=1

Interpretation: Structural trace validation is not clean enough for public strong claims.

### P1A_SEQUENCE_PRESENT_EFFECT_UNPROVEN — major-pass1-watchpoint

Evidence: sequence_field_rows=511; sequence_active_rows=176; no_sequence action-diff cases=1

Interpretation: Sequence composition exists and is telemetry-visible, but current capped diagnostics show limited action-level causal effect.

### P1A_MAINTENANCE_INSENSITIVITY_UNRESOLVED — major-pass1-watchpoint

Evidence: maintenance insensitive=10; sensitive=0

Interpretation: Maintenance middle/renewal-like remain insensitive under recent-mechanism ablations; do not patch maintenance specifically.

### P1A_READOUT_SWAMPING_REMAINS — major-pass1-watchpoint

Evidence: carrier_with_resolver_alt_steps=104; carrier_with_resolver_no_shape_trigger_steps=98; support/stability share=0.949325684325217

Interpretation: Support/stability/field dominance still risks collapsing CO structure into ordinary scoring-like readout.

### P1A_QUOTIENT_CONSERVATIVE_CALIBRATION_OPEN — medium-watchpoint

Evidence: duplicate_signature_bug_count=0; possible_calibration_site_count=82; accepted_singletons=495

Interpretation: No obvious duplicate-signature bug found, but quotienting is mostly conservative/singleton and needs false/missed quotient calibration.

### P1A_ADAPTER_BOUNDARY_AND_FORMULA_GROUNDING_STILL_REQUIRED — major-pass1-watchpoint

Evidence: adapter structural ablations are behavior-causal, but formulas and translator richness remain possible hidden-shaping risks.

Interpretation: Before public release, adapter-boundary adversarial tests and formula/coefficient grounding must be strengthened.

## Required next actions

1. Do not add robot/sim yet as evidence. First resolve/characterize sequence-readout consumption and maintenance/readout insensitivity.
2. Run broader multi-seed/current-family diagnostics after freezing mechanism set, including no_sequence, no_scheduler, no_quotient, static_shape and minimal_recent_core.
3. Add adapter-boundary adversarial tests: thin translator, remove public effects, perturb irrelevant labels, and compare rich vs minimal public effects.
4. Add coefficient sensitivity around readout/sequence consumption, not just resolver thresholds; classify coefficients as derived/provisional/empirical.
5. Decide whether remaining readout swamping is a bug, an expected limitation, or evidence that CO currently degenerates into scoring in some regimes.
6. Only after that, design small robot/sim tasks as stress tests for dynamic admissibility, exposure, affordance, and sequence continuation.

## Release statement

This repo state may be called a Pass-1 kernel closure candidate, not a finished kernel, not a public empirical result, and not a publication-ready CO system. The next work should evaluate and simplify/harden this frozen candidate rather than automatically adding mechanisms.
