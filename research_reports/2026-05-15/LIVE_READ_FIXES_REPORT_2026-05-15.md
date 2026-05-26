# Live-Read Fixes Report — 2026-05-15

## Scope

This pass was triggered by a user challenge that the prior cold-onboarding hardening was too trust-based and not enough direct reading. The pass did not claim a full repo-wide line-by-line audit. It live-read and corrected the active onboarding path plus the currently relevant kernel docs around relation, certificate, readout, structural trace, and architecture acceptance status.

## Directly visited files

Root/onboarding:

```text
README.md
NEXT_AI_START_HERE.md
CANONICAL_STRUCTURE_MAP.md
OPEN_POINTS_AND_FUTURE_WORK.md
ChangeOntCode/README.md
```

Kernel docs:

```text
ChangeOntCode/docs/kernel_spec/00_INDEX.md
ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/03_WIRING_MAP.md
ChangeOntCode/docs/kernel_spec/04_GOAL_STATE_CO_ALIGNED_KERNEL.md
ChangeOntCode/docs/kernel_spec/05_ELEMENTS/02_V1_DEPENDENCY_DECLARATIONS.md
ChangeOntCode/docs/kernel_spec/05_SURFACES/README.md
ChangeOntCode/docs/kernel_spec/08_TRANSLATORS/README.md
ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md
ChangeOntCode/docs/kernel_spec/42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md
ChangeOntCode/docs/kernel_spec/43_CANONICAL_COMMITMENT_RULE.md
ChangeOntCode/docs/kernel_spec/80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md
ChangeOntCode/docs/kernel_spec/88_ADAPTER_PUBLIC_EFFECT_RELATION_COVERAGE.md
ChangeOntCode/docs/kernel_spec/91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md
ChangeOntCode/docs/kernel_spec/92_ARCHITECTURE_ACCEPTANCE_AUDITS.md
ChangeOntCode/docs/kernel_spec/94_REAL_TRACE_STRUCTURAL_VALIDATION_AND_FORMULA_GROUNDING.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
```

Code touched during this live-read correction:

```text
ChangeOntCode/agents/co/runtime/surfaces/fusion_support.py
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
ChangeOntCode/agents/co/core/primitives/operative_relevance.py
```

## Concrete mismatches fixed

1. `94_REAL_TRACE_STRUCTURAL_VALIDATION_AND_FORMULA_GROUNDING.md` still reported an older structural trace summary with `cases_with_watchpoints: 5`. The current executable trace reports `cases_with_watchpoints: 0`, `branch_internal_operation_rows: 20`, `field_delta_positive_cases: 5`, and `commitment_changed_cases: 1`. The document now reflects the current verified trace while keeping the limitation boundary explicit.

2. `91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md` still reported an older relation-path diagnostic with `relations_total: 82`, `non_rival_relations: 18`, and action/mode change counts that no longer match the executable current trace. It now reports the current verified relation-path trace: `relations_total: 80`, `non_rival_relations: 16`, `commitment_action_changed_cases: 0`, and `commitment_mode_changed_cases: 1`.

3. `88_ADAPTER_PUBLIC_EFFECT_RELATION_COVERAGE.md` still described an earlier adapter coverage count of `relations_total: 82`. The current verified run reports `relations_total: 80`; the doc now says so.

4. `92_ARCHITECTURE_ACCEPTANCE_AUDITS.md` had a current top-level status and body sections that still sounded like first-pass hard failure. It now reports the current `ACCEPTANCE_WATCHPOINTS_REMAIN` audit status directly and removes the old failure-count narrative from the active architecture-audit doc.

5. `80_KERNEL_SIDE_RELATION_SURFACE_CONTRACT.md` said the contract did not assert the code implements RelationSurface, even though the runtime implementation now exists. It also had duplicate section numbering and a rivalry example that blurred single-slot competition with strong rivalry. The doc now separates `decision_slot_competition` from strong rivalry and states that a first implementation exists but remains watchpoint-level.

6. Several active docs contained negative references to older architecture names or historical replacement language. Those were replaced with positive current-loop statements so active docs explain what the canonical architecture is, not what obsolete architecture should not be used.

7. `17_COMPONENT_CLASSIFICATION.md` listed absent surface names as if they were active-looking runtime surface entries. Those rows were replaced with current problem-contract and telemetry/support categories.

8. `42_CANONICAL_READOUT_AND_ACTION_SELECTION_RULE.md` and `43_CANONICAL_COMMITMENT_RULE.md` still described the readout path as if relation/certificate integration was only future work. They now state the current architecture-level implementation status and keep formula/reason-quality watchpoints open.

9. `102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md` contained duplicated purpose bullets. The duplicate was removed.

10. `fusion_support.py` lacked module/function documentation despite providing provisional readout formula helpers. It now has targeted docstrings clarifying that it is not an independent policy layer.

11. `operative_relevance.py` had a docstring phrase that could make a non-canonical candidate scoring helper sound like the active readout path. The docstring now marks the helper as non-canonical/investigatory for evidence purposes.

## Current verified command results

Executed successfully after the live-read corrections:

```text
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
python -m agents.co.tests.canonical_structure_docs_invariants
python -m agents.co.tests.shape_prior6_contract_invariants
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
python -m experiments.studies.architecture_acceptance_audit_v1
```

Current structural trace summary:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "structural_relations": 16,
  "weak_decision_competition_relations": 64,
  "branch_internal_operation_rows": 20,
  "field_delta_positive_cases": 5,
  "commitment_changed_cases": 1,
  "cases_with_watchpoints": 0
}
```

Current relation-path summary:

```json
{
  "cases": 5,
  "candidate_rows": 20,
  "relations_total": 80,
  "non_rival_relations": 16,
  "commitment_action_changed_cases": 0,
  "commitment_mode_changed_cases": 1,
  "field_delta_positive_cases": 5
}
```

Current architecture acceptance status:

```text
ACCEPTANCE_WATCHPOINTS_REMAIN
```

## Remaining caution

This pass improves the visited path. It is still not a full line-by-line audit of every file in the repo. Remaining exact legacy names appear in test guard lists that check removed active docs do not reappear; they are not active architecture docs.

The repo remains not empirical proof of CO. The next correct step is continued live-read traversal or controlled ablation/trace diagnostics, not broad reward claims.
