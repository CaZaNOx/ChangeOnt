# Full Repo Audit Report — 2026-05-15

Status: full-repo coherence audit and hardening pass.  
Claim boundary: repository coherence, validation hygiene, and structural contract checks. This is not empirical proof of CO, not RCF novelty proof, and not a consciousness result.

## 1. Scope actually audited

The audit started from the repo package produced by the prior live traversal pass and treated repo files as truth. The pass covered:

```text
- full file inventory;
- root onboarding files;
- TheoryOfChange_main active meta/onboarding route;
- TheoryOfChange_main statement/link/frontmatter validator;
- ChangeOntCode kernel_spec active docs and catalogs;
- active CO runtime code path under agents/co;
- adapters, boundary, placement, runtime surfaces, integration, and tests;
- markdown inline links;
- invariant suite and structural study modules;
- generated-file/package hygiene.
```

Inventory after fixes:

```text
markdown files: 807
python files: 285
machine ledger: FULL_REPO_AUDIT_LEDGER_2026-05-15.json
```

The audit used direct reading of active entry/architecture files plus repository-wide scans and executable validators. It did not convert every historical or exploratory theory file into a freshly line-by-line philosophical proof. The remaining theory-level semantic audit is listed as an open item below.

## 2. Defects fixed

### 2.1 Adapter-side fallback defect

File:

```text
ChangeOntCode/agents/co/adapters/maintenance_replacement_adapter.py
```

Finding:

```text
If the kernel returned an invalid maintenance action, the adapter coerced it to RUN.
```

Why this was wrong:

```text
This is adapter-side rescue behavior. It violates the no-classical/no-first-legal/fail-closed rule because an invalid kernel readout was silently turned into a valid native action.
```

Fix:

```text
The adapter now raises RuntimeError instead of coercing to RUN.
```

Protection added:

```text
ChangeOntCode/agents/co/tests/no_classical_fallback_fail_closed_invariants.py
```

New invariant:

```text
test_adapter_rejects_invalid_kernel_action_without_rescue
```

### 2.2 Maze unused shortest-path helper removed

File:

```text
ChangeOntCode/agents/co/adapters/maze_adapter.py
```

Finding:

```text
An unused `_maze_shortest_dist` helper remained in the adapter. It was not used in the active path, but its presence created avoidable confusion because the adapter doctrine forbids shortest-path policy leakage.
```

Fix:

```text
Removed the unused helper and the now-unneeded deque import.
```

### 2.3 Theory validator false negatives and real theory hygiene failures

Files:

```text
tools/validate_toc_main.py
TheoryOfChange_main/02_Concepts/C-kernel.md
TheoryOfChange_main/02_Concepts/C-boundary.md
TheoryOfChange_main/02_Concepts/C-collapse.md
TheoryOfChange_main/02_Concepts/C-change-space-metric.md
TheoryOfChange_main/01_Statements/Clarification/S-CL-environment-vector-local-progress-reliability.md
multiple statement frontmatter files
TheoryOfChange_main/03_Derivation/graph.yaml
```

Findings:

```text
- validate_toc_main.py treated repo-root links to ChangeOntCode docs as missing.
- Several concept links used by current statements had no concept page.
- Several newer clarification/definition/derivation files lacked required frontmatter fields.
- graph.yaml contained orphan nodes for statement IDs that no longer existed.
```

Fixes:

```text
- Updated the validator to resolve links both inside TheoryOfChange_main and from repo root.
- Added minimal concept index pages for kernel, boundary, collapse, and change-space metric/comparability.
- Added the missing environment-vector local-progress bridge file because existing files pointed to it.
- Added/fixed frontmatter for the affected newer statement files.
- Removed orphan graph nodes and incident edges for missing/deleted statement IDs:
  - stmt.cl-godel-hole-legacy
  - stmt.elm-action-head
  - stmt.elm-e0-vote-bridge
  - stmt.localreach-topology
  - stmt.pointer-structural
  - stmt.proto-conceptual-same-type-guidance
```

Result:

```text
python tools/validate_toc_main.py
→ All checks passed for TheoryOfChange_main.
```

### 2.4 Stale execution map / surface classification wording

Files:

```text
TheoryOfChange_main/00_Meta/EXECUTION_REALIZATION_MAP.md
TheoryOfChange_main/00_Meta/CANONICAL_CORE_AND_INVESTIGATION_PERIPHERY.md
```

Findings:

```text
- Remaining transformation burden was still described as weak/mostly implicit.
- Candidate/readout surfaces were grouped too loosely with investigation periphery.
```

Fixes:

```text
- Updated burden execution locus to branch-internal burden carriers, RelationSurface, RCF, and CollapseCertificate.
- Clarified that CandidateSurface and CommitmentSurface are active runtime carriers, but not philosophical primitives/elements.
```

### 2.5 Generated Python caches removed from package

Finding:

```text
The prior zip still contained __pycache__ files.
```

Fix:

```text
Removed generated __pycache__ directories before packaging.
```

## 3. Validation run after fixes

Commands run from repo root / ChangeOntCode:

```bash
python tools/validate_toc_main.py
cd ChangeOntCode
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.candidate_surface_publication_invariants
python -m agents.co.tests.canonical_manifest_invariants
python -m agents.co.tests.canonical_structure_docs_invariants
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.commitment_surface_readout_invariants
python -m agents.co.tests.continuation_state_invariants
python -m agents.co.tests.family_packet_alignment_invariants
python -m agents.co.tests.forbidden_shared_family_branching_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.maintenance_replacement_family_invariants
python -m agents.co.tests.maintenance_replacement_runtime_wiring_invariants
python -m agents.co.tests.maintenance_replacement_stoa_baseline_invariants
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.problem_contract_invariants
python -m agents.co.tests.recursive_continuation_field_invariants
python -m agents.co.tests.recursive_continuation_field_relation_support_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.runtime_contract_invariants
python -m agents.co.tests.shape_prior6_active_path_invariants
python -m agents.co.tests.shape_prior6_contract_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.structure_dependency_invariants
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
python -m experiments.studies.architecture_acceptance_audit_v1
```

Observed key study outputs after fixes:

```text
structural_trace_validation_v1:
  status: PASS_WITH_WATCHPOINTS
  cases: 5
  candidate_rows: 20
  relations_total: 80
  structural_relations: 16
  weak_decision_competition_relations: 64
  branch_internal_operation_rows: 20
  field_delta_positive_cases: 5
  commitment_changed_cases: 1
  cases_with_watchpoints: 0

relation_path_trace_v1:
  relations_total: 80
  non_rival_relations: 16
  commitment_action_changed_cases: 0
  commitment_mode_changed_cases: 1

architecture_acceptance_audit_v1:
  status: ACCEPTANCE_WATCHPOINTS_REMAIN
  adapter_public_effect_leakage: PASS_WITH_WATCHPOINTS
  branch_identity_trace_quality: PASS_WITH_WATCHPOINTS
  collapse_certificate_reason_quality: PASS_WITH_WATCHPOINTS
  formula_grounding: PASS_WITH_WATCHPOINTS
  relation_noise: PASS_WITH_WATCHPOINTS
```

Markdown inline-link audit:

```text
missing inline markdown links: 0
```

## 4. Current coherent architecture after audit

The active route remains:

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

The no-fallback rule is stronger after this audit because the maintenance adapter no longer rescues invalid kernel output with `RUN`.

## 5. Remaining gaps / not solved

The following remain open and must not be hidden:

```text
- architecture_acceptance_audit_v1 still returns ACCEPTANCE_WATCHPOINTS_REMAIN;
- formula/coefficient grounding remains incomplete;
- quotient/equivalence tolerance is not fully operationally calibrated;
- recursion scheduler/budget is not complete;
- multi-step continuation identity is not complete;
- RCF is not proven novel against known algorithms;
- empirical usefulness is not proven;
- broad benchmark evidence is not established;
- consciousness/meaning theory is not established;
- function-level docstrings are still incomplete across many files;
- historical/exploratory theory files are not all semantically re-audited line by line.
```

## 6. Next recommended work

Do not jump to broad benchmarks yet. Recommended next order:

```text
1. Expand the no-fallback invariant pattern to every adapter, not only maintenance.
2. Add an adapter action-validation helper so every adapter validates kernel output against its native action space consistently.
3. Add a docstring/comment pass for active boundary/adapters/placement/runtime/integration functions.
4. Complete formula-ledger coverage for every readout-affecting scalar.
5. Run targeted ablations:
   - RelationSurface on/off
   - public_effects present/stripped
   - branch-internal operations present/stripped
   - CollapseCertificate on/off
   - same scalar rows with different relation topology
6. Only then run controlled family studies with frozen constants and honest baselines.
```

## 7. Claim boundary

This audit supports the following statement only:

```text
The repo is more coherent and more self-validating than before. The active onboarding, theory validator, kernel docs, runtime path, and invariant/study checks are aligned enough to proceed to controlled structural diagnostics.
```

It does not support:

```text
CO is proven;
RCF is novel;
CO beats baselines;
the formulas are fully grounded;
consciousness follows from the kernel.
```
