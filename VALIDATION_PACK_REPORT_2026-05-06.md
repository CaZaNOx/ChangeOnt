# ChangeOnt Validation Pack — 2026-05-06

## Scope

This pass validates the latest code/docs-aligned repo as an architecture implementation target. It is **not** a broad reward benchmark and does **not** claim CO works generally.

Validated chain:

```text
certified docs target
→ code/docs alignment
→ compile/runtime invariants
→ structural traces
→ relation-path traces
→ architecture-acceptance audit
```

## Direct fixes during validation

Two validation-target mismatches were found and fixed:

1. `canonical_structure_docs_invariants.py` still required pre-certification docs (`30_*`, `31_*`, `32_*`, `33_*`). It now checks the certified canonical doc target and verifies removed legacy docs do not reappear.
2. `commitment_relation_readout_trace_v1.py` imported stale helper names from the relation-awareness test. It now uses the current `_base_rows` helper and reports the post-certificate readout status.

These are validation/study alignment fixes, not runtime mechanism changes.

## Compile check

```text
python3 -m compileall -q agents experiments
exit: 0
```

## Invariant/test results

Modules run: 29
Failures after reruns/fixes: 0

All tracked invariant modules passed after the two validation-target fixes.

Key covered areas:

```text
canonical docs structure
certified runtime alignment
code-vs-doc pipeline compliance
no-classical-fallback fail-closed behavior
candidate / relation / carrier / certificate invariants
RCF invariants
shape / runtime / problem contracts
maintenance family and baseline invariants
smoke runner
```

Full machine-readable test summary: `validation_outputs/test_summary_final.json`.

## Study/diagnostic results

Studies run: 5
Failures after fixes: 0

### Adapter public-effect relation coverage

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "rows_with_public_effects": 20
}
```

Interpretation: adapters emit public effects in all sampled rows; relation derivation is active. This is coverage/wiring evidence, not performance evidence.

### Architecture acceptance audit

```json
{
  "status": "ACCEPTANCE_WATCHPOINTS_REMAIN",
  "summary": {
    "adapter_public_effect_leakage": "PASS_WITH_WATCHPOINTS",
    "branch_identity_trace_quality": "PASS_WITH_WATCHPOINTS",
    "collapse_certificate_reason_quality": "PASS_WITH_WATCHPOINTS",
    "formula_grounding": "PASS_WITH_WATCHPOINTS",
    "relation_noise": "PASS_WITH_WATCHPOINTS"
  },
  "formula_coefficient_lines": null
}
```

Interpretation: no hard blockers, but watchpoints remain. Formula coefficient lines remain a major documentation/validation debt.

### Relation-path trace

```json
{
  "cases": [
    {
      "branch_internal_hiddenness_pressure_total": 3.0,
      "branch_internal_operation_rows": 3,
      "branch_internal_resolver_support_total": 3.0,
      "branch_internal_unresolved_pressure_total": 1.8599999999999999,
      "candidate_rows": 3,
      "commitment_action_changed": false,
      "commitment_mode_changed": false,
      "commitment_off_action": 0,
      "commitment_off_mode": "reopen_or_sample",
      "commitment_on_action": 0,
      "commitment_on_mode": "reopen_or_sample",
      "family": "bandit_initial",
      "field_delta_by_action": {
        "0": {
          "collapse_certificate_blocker_pressure": 0.19793377855816,
          "collapse_certificate_recursion_demand": 0.3667507080858968,
          "collapse_certificate_score": 0.006316849546507686,
          "field_collapse_readiness": 0.03685401750159685,
          "field_debt": 0.19583611598849998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.3667507080858968,
          "field_viability": 0.06707418376434636,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "1": {
          "collapse_certificate_blocker_pressure": 0.19793377855816,
          "collapse_certificate_recursion_demand": 0.3667507080858968,
          "collapse_certificate_score": 0.006316849546507686,
          "field_collapse_readiness": 0.03685401750159685,
          "field_debt": 0.19583611598849998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.3667507080858968,
          "field_viability": 0.06707418376434636,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "2": {
          "collapse_certificate_blocker_pressure": 0.19793377855816,
          "collapse_certificate_recursion_demand": 0.3667507080858968,
          "collapse_certificate_score": 0.006316849546507686,
          "field_collapse_readiness": 0.03685401750159685,
          "field_debt": 0.19583611598849998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.3667507080858968,
          "field_viability": 0.06707418376434636,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        }
      },
      "field_delta_l1": 4.972549084592714,
      "field_delta_max": 0.42,
      "identity_source_counts": {
        "public_effects": 3
      },
      "non_rival_relations": 0,
      "relations_by_type": {
        "decision_slot_competition": 6
      },
      "relations_total": 6,
      "rows_with_public_effects": 3,
      "rows_with_relations": 3,
      "structural_relations": 0,
      "weak_decision_competition_relations": 6
    },
    {
      "branch_internal_hiddenness_pressure_total": 0.22000000000000003,
      "branch_internal_operation_rows": 5,
      "branch_internal_resolver_support_total": 1.13,
      "branch_internal_unresolved_pressure_total": 0.426085,
      "candidate_rows": 5,
      "commitment_action_changed": false,
      "commitment_mode_changed": false,
      "commitment_off_action": "INSPECT",
      "commitment_off_mode": "stable_continuation",
      "commitment_on_action": "INSPECT",
      "commitment_on_mode": "stable_continuation",
      "family": "maintenance_partial_midhealth",
      "field_delta_by_action": {
        "INSPECT": {
          "collapse_certificate_blocker_pressure": 0.0036645899034907607,
          "collapse_certificate_recursion_demand": 0.004632891269454771,
          "collapse_certificate_score": 0.007475889761806076,
          "field_collapse_readiness": 0.004854179574722867,
          "field_debt": 0.0,
          "field_grey_pressure": 0.020358832797170896,
          "field_recursion_budget": 0.004632891269454771,
          "field_viability": 0.001042323220403485,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "REPAIR": {
          "collapse_certificate_blocker_pressure": 0.0017667644761688228,
          "collapse_certificate_recursion_demand": 0.007361434708993329,
          "collapse_certificate_score": 0.08322050602887676,
          "field_collapse_readiness": 0.012673793786976001,
          "field_debt": 0.011042277976055143,
          "field_grey_pressure": 0.0,
          "field_recursion_budget": 0.007361434708993329,
          "field_viability": 0.027582743638684182,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "REPLACE": {
          "collapse_certificate_blocker_pressure": 0.0023965835573325524,
          "collapse_certificate_recursion_demand": 0.016456592700377776,
          "collapse_certificate_score": 0.08401849191275929,
          "field_collapse_readiness": 0.0233529039705275,
          "field_debt": 0.014978647233328451,
          "field_grey_pressure": 0.0,
          "field_recursion_budget": 0.016456592700377776,
          "field_viability": 0.054529750369570584,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "RUN": {
          "collapse_certificate_blocker_pressure": 0.06304346820352702,
          "collapse_certificate_recursion_demand": 0.11635562137492891,
          "collapse_certificate_score": 0.036080093243131384,
          "field_collapse_readiness": 0.053098223482922396,
          "field_debt": 0.06409647103225441,
          "field_grey_pressure": 0.12215573799092386,
          "field_recursion_budget": 0.11635562137492891,
          "field_viability": 0.028599966870566595,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "WAIT": {
          "collapse_certificate_blocker_pressure": 0.0008439505187935112,
          "collapse_certificate_recursion_demand": 0.0010445757025041996,
          "collapse_certificate_score": 0.0013632922745826503,
          "field_collapse_readiness": 0.0021825464630944036,
          "field_debt": 0.009617879942070987,
          "field_grey_pressure": 0.003860612621876925,
          "field_recursion_budget": 0.0010445757025041996,
          "field_viability": 0.0017828835397296627,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        }
      },
      "field_delta_l1": 1.0313856359038653,
      "field_delta_max": 0.12215573799092386,
      "identity_source_counts": {
        "public_effects": 5
      },
      "non_rival_relations": 6,
      "relations_by_type": {
        "cancellation": 3,
        "decision_slot_competition": 20,
        "relief": 2,
        "shared_evidence": 1
      },
      "relations_total": 26,
      "rows_with_public_effects": 5,
      "rows_with_relations": 5,
      "structural_relations": 6,
      "weak_decision_competition_relations": 20
    },
    {
      "branch_internal_hiddenness_pressure_total": 0.0,
      "branch_internal_operation_rows": 4,
      "branch_internal_resolver_support_total": 1.0,
      "branch_internal_unresolved_pressure_total": 1.3800000000000001,
      "candidate_rows": 4,
      "commitment_action_changed": false,
      "commitment_mode_changed": false,
      "commitment_off_action": "RIGHT",
      "commitment_off_mode": "dominance",
      "commitment_on_action": "RIGHT",
      "commitment_on_mode": "dominance",
      "family": "maze_visible_local",
      "field_delta_by_action": {
        "DOWN": {
          "collapse_certificate_blocker_pressure": 0.010673954594512945,
          "collapse_certificate_recursion_demand": 0.012535824895232417,
          "collapse_certificate_score": 0.02423496107552009,
          "field_collapse_readiness": 0.002763401415871225,
          "field_debt": 0.04719700716359998,
          "field_grey_pressure": 0.01734685249076079,
          "field_recursion_budget": 0.012535824895232417,
          "field_viability": 5.177107708120854e-05,
          "quotient_resolved_rival_count": 4.0,
          "quotient_share_count": 2.0,
          "unresolved_rival_count": 0.0
        },
        "LEFT": {
          "collapse_certificate_blocker_pressure": 0.010673954594512945,
          "collapse_certificate_recursion_demand": 0.012535824895232417,
          "collapse_certificate_score": 0.02423496107552009,
          "field_collapse_readiness": 0.002763401415871225,
          "field_debt": 0.04719700716359998,
          "field_grey_pressure": 0.01734685249076079,
          "field_recursion_budget": 0.012535824895232417,
          "field_viability": 5.177107708120854e-05,
          "quotient_resolved_rival_count": 4.0,
          "quotient_share_count": 2.0,
          "unresolved_rival_count": 0.0
        },
        "RIGHT": {
          "collapse_certificate_blocker_pressure": 0.0,
          "collapse_certificate_recursion_demand": 0.0177877846977988,
          "collapse_certificate_score": 0.11943873708097308,
          "field_collapse_readiness": 0.040589584235568354,
          "field_debt": 0.0,
          "field_grey_pressure": 0.0,
          "field_recursion_budget": 0.042630588884845756,
          "field_viability": 0.1127488450988009,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "UP": {
          "collapse_certificate_blocker_pressure": 0.010673954594512945,
          "collapse_certificate_recursion_demand": 0.012535824895232417,
          "collapse_certificate_score": 0.02423496107552009,
          "field_collapse_readiness": 0.002763401415871225,
          "field_debt": 0.04719700716359998,
          "field_grey_pressure": 0.01734685249076079,
          "field_recursion_budget": 0.012535824895232417,
          "field_viability": 5.177107708120854e-05,
          "quotient_resolved_rival_count": 4.0,
          "quotient_share_count": 2.0,
          "unresolved_rival_count": 0.0
        }
      },
      "field_delta_l1": 18.715214332821418,
      "field_delta_max": 4.0,
      "identity_source_counts": {
        "public_effects": 4
      },
      "non_rival_relations": 6,
      "relations_by_type": {
        "decision_slot_competition": 12,
        "equivalence": 3,
        "relief": 3
      },
      "relations_total": 18,
      "rows_with_public_effects": 4,
      "rows_with_relations": 4,
      "structural_relations": 6,
      "weak_decision_competition_relations": 12
    },
    {
      "branch_internal_hiddenness_pressure_total": 3.0,
      "branch_internal_operation_rows": 5,
      "branch_internal_resolver_support_total": 1.0,
      "branch_internal_unresolved_pressure_total": 2.412,
      "candidate_rows": 5,
      "commitment_action_changed": false,
      "commitment_mode_changed": false,
      "commitment_off_action": "RIGHT",
      "commitment_off_mode": "dominance",
      "commitment_on_action": "RIGHT",
      "commitment_on_mode": "dominance",
      "family": "latent_mechanism_visible",
      "field_delta_by_action": {
        "DOWN": {
          "collapse_certificate_blocker_pressure": 0.17604139073205122,
          "collapse_certificate_recursion_demand": 0.32275978949416156,
          "collapse_certificate_score": 0.10742855983948418,
          "field_collapse_readiness": 0.15923353487949837,
          "field_debt": 0.259698991328514,
          "field_grey_pressure": 0.28049751177493876,
          "field_recursion_budget": 0.32275978949416156,
          "field_viability": 0.09163578595521146,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "INTERACT": {
          "collapse_certificate_blocker_pressure": 0.1443008643124915,
          "collapse_certificate_recursion_demand": 0.2852470484951922,
          "collapse_certificate_score": 0.06844926394031348,
          "field_collapse_readiness": 0.09665803587558008,
          "field_debt": 0.09338040195307201,
          "field_grey_pressure": 0.252,
          "field_recursion_budget": 0.2852470484951922,
          "field_viability": 0.050036127750671344,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "LEFT": {
          "collapse_certificate_blocker_pressure": 0.16643925063965634,
          "collapse_certificate_recursion_demand": 0.31185529634104614,
          "collapse_certificate_score": 0.06591689446844018,
          "field_collapse_readiness": 0.13648257677210807,
          "field_debt": 0.258297074146584,
          "field_grey_pressure": 0.22839843764557158,
          "field_recursion_budget": 0.31185529634104614,
          "field_viability": 0.07902249323515609,
          "quotient_resolved_rival_count": 2.0,
          "quotient_share_count": 1.0,
          "unresolved_rival_count": 0.0
        },
        "RIGHT": {
          "collapse_certificate_blocker_pressure": 0.15149330944608,
          "collapse_certificate_recursion_demand": 0.34562916705287056,
          "collapse_certificate_score": 0.04571556325627846,
          "field_collapse_readiness": 0.06222803033983948,
          "field_debt": 0.138333184038,
          "field_grey_pressure": 0.252,
          "field_recursion_budget": 0.34562916705287056,
          "field_viability": 0.07663268303778747,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "UP": {
          "collapse_certificate_blocker_pressure": 0.16643925063965634,
          "collapse_certificate_recursion_demand": 0.31185529634104614,
          "collapse_certificate_score": 0.06591689446844018,
          "field_collapse_readiness": 0.13648257677210807,
          "field_debt": 0.258297074146584,
          "field_grey_pressure": 0.22839843764557158,
          "field_recursion_budget": 0.31185529634104614,
          "field_viability": 0.07902249323515609,
          "quotient_resolved_rival_count": 2.0,
          "quotient_share_count": 1.0,
          "unresolved_rival_count": 0.0
        }
      },
      "field_delta_l1": 13.529569887723476,
      "field_delta_max": 2.0,
      "identity_source_counts": {
        "public_effects": 5
      },
      "non_rival_relations": 4,
      "relations_by_type": {
        "decision_slot_competition": 20,
        "equivalence": 1,
        "relief": 3
      },
      "relations_total": 24,
      "rows_with_public_effects": 5,
      "rows_with_relations": 5,
      "structural_relations": 4,
      "weak_decision_competition_relations": 20
    },
    {
      "branch_internal_hiddenness_pressure_total": 3.0,
      "branch_internal_operation_rows": 3,
      "branch_internal_resolver_support_total": 2.8,
      "branch_internal_unresolved_pressure_total": 1.8599999999999999,
      "candidate_rows": 3,
      "commitment_action_changed": false,
      "commitment_mode_changed": false,
      "commitment_off_action": 0,
      "commitment_off_mode": "reopen_or_sample",
      "commitment_on_action": 0,
      "commitment_on_mode": "reopen_or_sample",
      "family": "renewal_initial",
      "field_delta_by_action": {
        "0": {
          "collapse_certificate_blocker_pressure": 0.1938013037020171,
          "collapse_certificate_recursion_demand": 0.36569297411911716,
          "collapse_certificate_score": 0.008034010954209636,
          "field_collapse_readiness": 0.038391915713248764,
          "field_debt": 0.14959148147093998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.36569297411911716,
          "field_viability": 0.0581096343494194,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "1": {
          "collapse_certificate_blocker_pressure": 0.1938013037020171,
          "collapse_certificate_recursion_demand": 0.36569297411911716,
          "collapse_certificate_score": 0.008034010954209636,
          "field_collapse_readiness": 0.038391915713248764,
          "field_debt": 0.14959148147093998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.36569297411911716,
          "field_viability": 0.0581096343494194,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        },
        "2": {
          "collapse_certificate_blocker_pressure": 0.1938013037020171,
          "collapse_certificate_recursion_demand": 0.36569297411911716,
          "collapse_certificate_score": 0.008034010954209636,
          "field_collapse_readiness": 0.038391915713248764,
          "field_debt": 0.14959148147093998,
          "field_grey_pressure": 0.42,
          "field_recursion_budget": 0.36569297411911716,
          "field_viability": 0.0581096343494194,
          "quotient_resolved_rival_count": 0.0,
          "quotient_share_count": 0.0,
          "unresolved_rival_count": 0.0
        }
      },
      "field_delta_l1": 4.7979428832842075,
      "field_delta_max": 0.42,
      "identity_source_counts": {
        "public_effects": 3
      },
      "non_rival_relations": 0,
      "relations_by_type": {
        "decision_slot_competition": 6
      },
      "relations_total": 6,
      "rows_with_public_effects": 3,
      "rows_with_relations": 3,
      "structural_relations": 0,
      "weak_decision_competition_relations": 6
    }
  ]
}
```

Interpretation: public effects and relation/branch-internal carriers produce RCF/certificate field deltas in all sampled cases. Final commitment did not change in this trace; that is not automatically failure, but it means this pass remains structural validation rather than behavior/performance evidence.

### Structural trace validation

```json
{
  "status": "PASS_WITH_WATCHPOINTS",
  "summary": {
    "branch_internal_operation_rows": 20,
    "candidate_rows": 20,
    "cases": 5,
    "cases_with_watchpoints": 5,
    "commitment_changed_cases": 0,
    "field_delta_positive_cases": 5,
    "relations_total": 80,
    "structural_relations": 16,
    "weak_decision_competition_relations": 64
  },
  "formula_lines": null
}
```

Interpretation: all sampled cases remain inspectable and architecture-consistent but still `PASS_WITH_WATCHPOINTS`. The system is structurally wired; it is not yet paper-grade validated.

### Commitment relation/readout trace

```json
{
  "status": "diagnostic_not_benchmark",
  "real_adapter_cases": 5,
  "relation_positive_cases": 5,
  "field_delta_positive_cases": 5,
  "commitment_changed_cases": 0,
  "verdict": {
    "commitment_surface_first_class_relation_certificate": true,
    "current_readout_status": "certificate_aware_with_watchpoints",
    "next_needed": "continue certificate reason-quality and formula-ledger validation before paper-grade relation-aware readout claim",
    "relation_path_reaches_rcf": true
  }
}
```

Interpretation: CommitmentSurface is certificate-aware after the earned-collapse patch. Raw relation metadata alone remains non-policy telemetry; first-class certificate fields are the intended readout input. Further certificate reason-quality and formula-ledger validation remain required.

## Current validation verdict

```text
VALIDATION_PACK_PASS_WITH_WATCHPOINTS
```

What this supports:

```text
- The cleaned docs target and code alignment do not have obvious runtime-contract breakage.
- No-classical-fallback / fail-closed invariants pass.
- RelationSurface, branch-internal carriers, RCF, CollapseCertificate, and CommitmentSurface are wired and traceable.
- Structural traces are available for manual review across representative families.
```

What this does **not** support yet:

```text
- CO performance claims.
- RCF novelty claims against known algorithms.
- Final formula/coefficient grounding.
- Final quotient/equivalence tolerance calibration.
- Final recursion scheduler validation.
- Consciousness/meaning claims.
```

## Remaining watchpoints before broad benchmarks

```text
1. Formula ledger/coefficient grounding remains incomplete.
2. Structural traces still pass with watchpoints, not clean final acceptance.
3. Commitment action did not change in the sampled relation-path trace; manual review should decide whether stability is correct or readout is too insensitive.
4. Quotient/equivalence tolerance is still target-specified rather than calibrated.
5. Recursion scheduler/budget is still target-specified rather than deeply validated.
6. Multi-step continuation identity remains under-audited.
```

## Recommended next move

Do a focused manual review of the structural trace cases and formula-ledger hot spots before broad reward benchmarks. If that review finds no architecture issue, the next phase can be controlled family studies against fair baselines.
