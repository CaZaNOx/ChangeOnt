# Code vs Certified Docs Full Alignment Pass — 2026-05-06

Status: **PASS WITH WATCHPOINTS** for the active implementation target.

## Scope

This pass aligned active code with the certified canonical docs target:

```text
Boundary / Adapter
→ CandidateSurface
→ Continuation Identity
→ Burden Operations
→ RelationSurface
→ RecursiveContinuationField
→ CollapseCertificate
→ CommitmentSurface
```

It was not a benchmark/performance pass and does not claim final formula calibration or final quotient/recursion theory.

## Main alignment fixes

1. Removed active retired runtime/test directories for old combos, placement axes, integration shims, and old tests.
2. Removed route/fusion/math combinators from the canonical combo.
3. Restricted the active registry to the canonical SSI header and removed constructible route-gate/math-policy/non-CO operation entries.
4. Replaced old route-gate/math-policy guards so accidental non-CO route requests fail closed.
5. Removed pipeline import fallback logic; canonical `C_Pipeline` must import or fail.
6. Removed gate routing from `COAgentCore.step`; certified runtime records `math_policy=co` and marks any non-CO request invalid.
7. Removed retired placement-payload exposure from runtime contract and updated tests accordingly.
8. Removed retired scope-projection paths from renewal/scope-key handling.
9. Retired `H_CS` and `H_ID` as guard headers and made `H_SSI` the only registry-exposed header.
10. Renamed active header/regime telemetry away from non-CO-route language toward thinness/thin-collapse terminology where it affects active runtime.
11. Added `certified_runtime_alignment_invariants.py` to enforce the active no-retired-route target.

## Automated alignment scan

```json
{
  "status": "CODE_DOC_ALIGNMENT_PASS_WITH_WATCHPOINTS",
  "hard_blockers": {},
  "checks": {
    "ChangeOntCode/agents/co/combos/legacy": false,
    "ChangeOntCode/agents/co/placement/legacy": false,
    "ChangeOntCode/agents/co/integration/legacy": false,
    "ChangeOntCode/agents/co/tests/legacy": false,
    "ChangeOntCode/agents/co/core/combinators/C_classic_ops.py": false,
    "ChangeOntCode/agents/co/core/combinators/SC_weighted_selection.py": false,
    "registry_exposes_retired_route_gate": false,
    "registry_exposes_retired_math_policy": false,
    "registry_exposes_retired_non_co_ops": false,
    "registry_exposes_retired_headers": false,
    "canonical_combo_has_combinators": false,
    "canonical_combo_math_policy_co": true
  },
  "old_architecture_hits": {
    "ActionHead": [],
    "VoteBridge": [],
    "allow_classical_fallback": [],
    "classic_planner": [],
    "C_ClassicOps": [
      "ChangeOntCode/agents/co/tests/certified_runtime_alignment_invariants.py"
    ],
    "SC_WeightedSelection": []
  }
}
```

## Verified tests

The following relevant modules passed after the patch:

```text
agents.co.tests.certified_runtime_alignment_invariants
agents.co.tests.code_vs_docs_pipeline_compliance_invariants
agents.co.tests.no_classical_fallback_fail_closed_invariants
agents.co.tests.runtime_contract_invariants
agents.co.tests.shape_prior6_contract_invariants
agents.co.tests.candidate_surface_publication_invariants
agents.co.tests.commitment_surface_readout_invariants
agents.co.tests.relation_surface_public_effect_invariants
agents.co.tests.adapter_public_effect_relation_coverage
agents.co.tests.burden_relation_microdiagnostics
agents.co.tests.collapse_certificate_readout_invariants
agents.co.tests.commitment_surface_relation_awareness_diagnostics
agents.co.tests.relation_path_trace_diagnostics
agents.co.tests.recursive_continuation_field_relation_support_invariants
agents.co.tests.recursive_continuation_field_invariants
agents.co.tests.continuation_state_invariants
agents.co.tests.kernel_structure_carrier_alignment_invariants
agents.co.tests.structural_trace_validation_invariants
agents.co.tests.problem_contract_invariants
agents.co.tests.family_packet_alignment_invariants
agents.co.tests.shape_prior6_active_path_invariants
agents.co.tests.maintenance_replacement_family_invariants
agents.co.tests.maintenance_replacement_runtime_wiring_invariants
agents.co.tests.maintenance_replacement_stoa_baseline_invariants
agents.co.tests.smoke_co_runner
```

The first long batched command timed out during the heavier maintenance section; the remaining maintenance modules passed when rerun separately with longer timeouts.

## Structural diagnostics

The structural trace remains `PASS_WITH_WATCHPOINTS`:

```json
{
  "branch_internal_operation_rows": 20,
  "candidate_rows": 20,
  "cases": 5,
  "cases_with_watchpoints": 5,
  "commitment_changed_cases": 0,
  "field_delta_positive_cases": 5,
  "relations_total": 80,
  "structural_relations": 16,
  "weak_decision_competition_relations": 64
}
```

Relation-path aggregate:

```json
{
  "candidate_rows": 20,
  "cases": 5,
  "commitment_action_changed_cases": 0,
  "commitment_mode_changed_cases": 0,
  "field_delta_positive_cases": 5,
  "non_rival_relations": 16,
  "relations_by_type": {
    "cancellation": 3,
    "decision_slot_competition": 64,
    "equivalence": 4,
    "relief": 8,
    "shared_evidence": 1
  },
  "relations_total": 80
}
```

## Remaining watchpoints

These are not active code-vs-doc contradictions, but they remain before paper-level claims:

```text
- full formula ledger / coefficient grounding;
- quotient/equivalence tolerance calibration;
- recursion scheduler and budget distinct from lookahead;
- deeper multi-step continuation identity audit;
- broader cross-family structural validation before performance claims.
```

## Claim boundary

This pass means the active implementation is aligned with the certified docs target far enough for continued structural validation. It does **not** mean CO is proven, formulas are final, or benchmark evidence is established.
