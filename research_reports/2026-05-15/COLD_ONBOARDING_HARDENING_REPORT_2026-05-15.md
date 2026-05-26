# Cold Onboarding Hardening Report — 2026-05-15

## Source artifact verified

Input artifact:

```text
ChangeOnt_structural_formula_checks_fixes_2026-05-06.zip
```

The repo was unpacked and inspected before edits. The handover was treated as untrusted until files were checked.

## Verification before edits

Found:

```text
research_reports/2026-05-06/STRUCTURAL_TRACE_AND_FORMULA_HOTSPOT_REVIEW_2026-05-06.md
research_reports/2026-05-06/CODE_DOC_FULL_ALIGNMENT_2026-05-06.md
research_reports/2026-05-06/VALIDATION_PACK_REPORT_2026-05-06.md
research_reports/2026-05-06/DOCS_CERTIFICATION_PASS_2026-05-06.md
ChangeOntCode/docs/kernel_spec/00_INDEX.md
ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py
ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
ChangeOntCode/agents/co/runtime/surfaces/continuation_field.py
ChangeOntCode/agents/co/runtime/surfaces/collapse_certificate.py
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
```

Not found under the exact handover name:

```text
KERNEL_STRUCTURE_CARRIER_ALIGNMENT_FIXES_2026-05-06.md
```

Carrier-alignment material does exist in the current docs/tests, especially:

```text
ChangeOntCode/docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
ChangeOntCode/agents/co/tests/kernel_structure_carrier_alignment_invariants.py
```

## Changes made

Cold-onboarding entrypoints:

```text
README.md
ChangeOntCode/README.md
NEXT_AI_START_HERE.md
CANONICAL_STRUCTURE_MAP.md
OPEN_POINTS_AND_FUTURE_WORK.md
```

Legacy/exploratory marking:

```text
ChangeOntCode/experiments/legacy/README.md
ChangeOntCode/tools/legacy/README.md
ChangeOntCode/outputs/legacy/README.md
ChangeOntCode/docs/kernel_spec/19_PATH_ALGEBRA_AND_SEMIRING_DIRECTION.md
ChangeOntCode/docs/kernel_spec/23_CO_MATH_ALIGNMENT_AND_CRITIQUE.md
ChangeOntCode/docs/kernel_spec/04_PRIMITIVES/P3_MDL.md
ChangeOntCode/docs/kernel_spec/04_PRIMITIVES/P8_Loopiness.md
```

Code traceability/comments were improved in prioritized active files:

```text
ChangeOntCode/agents/co/runtime/surfaces/*.py
ChangeOntCode/agents/co/adapters/*.py
ChangeOntCode/agents/co/core/combinators/C_pipeline.py
ChangeOntCode/agents/co/core/pipeline.py
ChangeOntCode/agents/co/core/contracts/problem_contract.py
ChangeOntCode/agents/co/core/contracts/placement_contract.py
ChangeOntCode/agents/co/integration/core_assembly.py
ChangeOntCode/agents/co/integration/core_builder.py
```

Generated Python cache files were removed from the final package.

## Checks run after edits

Compile:

```bash
cd ChangeOntCode
python -m compileall -q agents environments experiments tools
```

Core invariants / diagnostics run successfully:

```text
agents.co.tests.certified_runtime_alignment_invariants
agents.co.tests.no_classical_fallback_fail_closed_invariants
agents.co.tests.candidate_surface_publication_invariants
agents.co.tests.relation_surface_public_effect_invariants
agents.co.tests.kernel_structure_carrier_alignment_invariants
agents.co.tests.collapse_certificate_readout_invariants
agents.co.tests.structural_trace_validation_invariants
agents.co.tests.relation_path_trace_diagnostics
agents.co.tests.code_vs_docs_pipeline_compliance_invariants
agents.co.tests.canonical_structure_docs_invariants
agents.co.tests.structure_dependency_invariants
agents.co.tests.shape_prior6_contract_invariants
```

Study/trace modules run successfully:

```text
experiments.studies.architecture_acceptance_audit_v1
experiments.studies.structural_trace_validation_v1
experiments.studies.relation_path_trace_v1
```

Observed study statuses:

```text
architecture_acceptance_audit_v1: ACCEPTANCE_WATCHPOINTS_REMAIN
structural_trace_validation_v1: PASS_WITH_WATCHPOINTS, cases_with_watchpoints = 0
relation_path_trace_v1: relations_total = 80, non_rival_relations = 16, commitment_mode_changed_cases = 1
```

Markdown inline-link audit after edits:

```text
inline_markdown_missing_count = 0
```

Obsolete active-surface grep after cleanup found only test references checking that retired surface docs do not reappear:

```text
ChangeOntCode/agents/co/tests/canonical_structure_docs_invariants.py
```

## Remaining limitations

Cold onboarding is materially safer, but not perfect:

```text
- This pass did not add docstrings to every function in the entire repo.
  It prioritized active runtime surfaces, adapters, contracts, pipeline, and integration files.
- Formula grounding remains incomplete.
- Architecture acceptance still reports watchpoints.
- Structural validation is not empirical proof.
- Broad benchmarks were not run.
- RCF novelty and usefulness remain unproven.
- Consciousness/proto-consciousness claims remain out of scope.
```

## Current status statement

A new AI can now start at `README.md` → `NEXT_AI_START_HERE.md` and reach the current canonical theory/docs/code/test chain without needing the chat handover. It should still verify the repo state before making claims.
