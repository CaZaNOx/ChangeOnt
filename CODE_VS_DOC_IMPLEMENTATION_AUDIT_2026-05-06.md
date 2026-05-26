# Code-vs-Docs Implementation Audit — 2026-05-06

Status: first implementation-compliance patch against the certified canonical docs target.  
Claim boundary: implementation alignment and invariants only; not benchmark or performance evidence.

## Certified docs target used

`ChangeOnt_docs_certified_canonical_target_2026-05-06.zip`

The relevant target loop is:

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

## Main mismatch found

The active `C_Pipeline` still routed the final readout using an old class-name pattern rather than explicitly enforcing `CommitmentSurface` as the canonical final readout surface.

Consequence: `CommitmentSurface` would only be final if the config order happened to place it last. This violated the certified docs target, which requires the readout to run exactly once after all non-readout kernel surfaces.

## Fixes applied

### 1. Canonical pipeline readout enforcement

Updated:

```text
ChangeOntCode/agents/co/core/combinators/C_pipeline.py
```

Now:

```text
- identifies CommitmentSurface by its canonical class/MRO;
- partitions non-readout surfaces from the readout surface;
- runs all non-readout surfaces first;
- invokes CommitmentSurface exactly once, last;
- skips CommitmentSurface during update/learning pass;
- marks surface errors as non-evidential safety events instead of silent rescue.
```

### 2. CommitmentSurface orchestration residue removed

Updated:

```text
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
```

Now:

```text
- CommitmentSurface.run_update fails closed if called directly;
- CommitmentSurface is no longer an orchestration layer;
- old collapse-controller readout path was removed from the active surface;
- old telemetry keys tied to prior readout naming were removed;
- backward constructor aliases are accepted only as ignored compatibility aliases.
```

### 3. Canonical config cleanup

Updated:

```text
ChangeOntCode/agents/co/combos/CO_canonical_core.yaml
```

Now the canonical config names the surface as `commitment_surface` and does not pass old exploratory/readout parameters.

### 4. Core-level fail-closed telemetry

Updated:

```text
ChangeOntCode/agents/co/core/pipeline.py
```

Pipeline/substrate errors now set:

```text
engineering_safety_triggered = true
co_evidence_valid_for_step = false
safety_kind = pipeline_error / surface_error
```

rather than only recording a vague failure string.

### 5. New invariants

Added:

```text
ChangeOntCode/agents/co/tests/code_vs_docs_pipeline_compliance_invariants.py
```

These verify:

```text
- CommitmentSurface runs exactly once and last even if config order is wrong;
- update pass skips CommitmentSurface;
- surface errors mark the step non-evidential and do not rescue an action;
- direct old-style CommitmentSurface.run_update invocation fails closed.
```

## Active scan result

The active runtime/docs/config scan found no remaining hits for:

```text
ActionHead
VoteBridge
actionhead
collapse_controller
collapse_enabled
collapse_scores
head_eps
head_ngram
```

The scan excludes explicitly named legacy directories. Those are not part of the certified active path.

## Tests run

Verified passing:

```text
agents.co.tests.code_vs_docs_pipeline_compliance_invariants
agents.co.tests.no_classical_fallback_fail_closed_invariants
agents.co.tests.candidate_surface_publication_invariants
agents.co.tests.commitment_surface_readout_invariants
agents.co.tests.collapse_certificate_readout_invariants
agents.co.tests.relation_surface_public_effect_invariants
agents.co.tests.kernel_structure_carrier_alignment_invariants
agents.co.tests.structural_trace_validation_invariants
agents.co.tests.relation_path_trace_diagnostics
agents.co.tests.recursive_continuation_field_invariants
agents.co.tests.recursive_continuation_field_relation_support_invariants
agents.co.tests.continuation_state_invariants
agents.co.tests.shape_prior6_contract_invariants
agents.co.tests.shape_prior6_active_path_invariants
agents.co.tests.runtime_contract_invariants
agents.co.tests.problem_contract_invariants
agents.co.tests.family_packet_alignment_invariants
agents.co.tests.adapter_public_effect_relation_coverage
agents.co.tests.maintenance_replacement_family_invariants
agents.co.tests.maintenance_replacement_runtime_wiring_invariants
agents.co.tests.maintenance_replacement_stoa_baseline_invariants
agents.co.tests.smoke_co_runner
```

A long batched run reached the end but hit the notebook command timeout around the final smoke check; the smoke runner and heavier maintenance baseline invariant both passed when rerun separately with longer timeouts.

## Structural trace after patch

`structural_trace_validation_v1.py` still reports:

```json
{
  "status": "PASS_WITH_WATCHPOINTS",
  "summary": {
    "cases": 5,
    "candidate_rows": 20,
    "relations_total": 80,
    "structural_relations": 16,
    "weak_decision_competition_relations": 64,
    "branch_internal_operation_rows": 20,
    "field_delta_positive_cases": 5,
    "commitment_changed_cases": 0,
    "cases_with_watchpoints": 5
  },
  "formula_lines": 280
}
```

## Remaining watchpoints

This pass closes the pipeline/readout compliance mismatch. It does not close:

```text
- full formula ledger and coefficient calibration;
- quotient/equivalence tolerance calibration;
- recursion scheduler and budget;
- deeper multi-step branch identity;
- broader performance or benchmark evidence;
- RCF comparison against known algorithms.
```

## Verdict

The first active code-vs-doc mismatch was patched. The runtime now more faithfully enforces the certified execution loop: non-readout kernel surfaces first, `CommitmentSurface` exactly once and last, no readout rescue path, and fail-closed telemetry on active path errors.
