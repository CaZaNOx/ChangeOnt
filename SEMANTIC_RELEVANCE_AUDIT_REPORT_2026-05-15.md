# Semantic Relevance Audit Report — 2026-05-15

This report records the stricter audit requested after the cold-onboarding and full-repo hardening passes. It should be read as a repo-coherence audit, not as evidence that ChangeOnt is empirically useful or philosophically complete.

## 1. Scope

The audit classified the repo's markdown/code/config artifacts by current semantic role and then focused deep reading/checking on the files that the repo itself presents as active for onboarding, theory-to-kernel mapping, implementation, and structural validation.

Classification target:

```text
active / support / test / legacy / exploratory / generated / obsolete-like residue
```

The machine-readable ledger classifies 1206 tracked markdown/code/config artifacts in this package. The ledger is:

```text
SEMANTIC_RELEVANCE_AUDIT_LEDGER_2026-05-15.json
```

Important boundary:

```text
This was not a line-by-line philosophical rederivation of every historical,
exploratory, generated, or support statement file. Active onboarding and active
runtime/kernel paths were read and corrected. Broad theory/support material was
classified, scanned, graph-validated, and checked for route coherence, but not
all re-proven semantically line by line.
```

## 2. Active route audited

The audited current route includes:

```text
README.md
NEXT_AI_START_HERE.md
CANONICAL_STRUCTURE_MAP.md
OPEN_POINTS_AND_FUTURE_WORK.md
TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md
TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md
TheoryOfChange_main/00_Meta/TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md
ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md
ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
ChangeOntCode/docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
ChangeOntCode/docs/kernel_spec/03C_IMPLEMENTATION_FIDELITY_STATUS.md
ChangeOntCode/docs/kernel_spec/00_INDEX.md
```

The active implementation route was also checked, including boundary packet contracts, adapters, six-question placement controls, runtime surfaces, integration assembly, and the minimum structural diagnostics named in `NEXT_AI_START_HERE.md`.

## 3. Defects found and fixed

### 3.1 Derivation graph snapshots were stale

The Mermaid graph snapshots still referenced deleted or renamed statement IDs, including old active-route residue such as `stmt.elm-action-head` and `stmt.elm-e0-vote-bridge`. The YAML graph also had edge endpoints that were not declared as nodes.

Fixes:

```text
- added graph.yaml nodes for stmt.continuation-admissibility and stmt.localreach-zone;
- regenerated TheoryOfChange_main/03_Derivation/graph.mmd;
- regenerated TheoryOfChange_main/03_Derivation/graph_first_layer.mmd;
- strengthened tools/validate_toc_main.py so future validation checks graph edge endpoints and Mermaid snapshot references.
```

Current validator status:

```text
python tools/validate_toc_main.py
→ All checks passed for TheoryOfChange_main.
```

### 3.2 Adapter invalid-action validation was not shared across all active adapters

The prior no-fallback fix protected the maintenance adapter, but the common boundary guard did not yet validate every active adapter's native action domain. That left room for future adapter-specific rescue or coercion patterns.

Fixes:

```text
- extended agents/co/boundary/problem_packet.py::require_kernel_action with legal_actions and family parameters;
- added public native-domain rejection without fallback/coercion;
- updated bandit, renewal, maze, latent_mechanism, and maintenance adapters to pass their public native action domains;
- added invariants that invalid native actions fail closed and every active adapter calls the shared guard with legal_actions.
```

### 3.3 UTF-8 BOM residue existed in source/support files

Several Python support files still contained a UTF-8 BOM that could trip AST/source checks. They were rewritten as plain UTF-8, including files under `ChangeOntCode/environments/`, `ChangeOntCode/experiments/`, and `ChangeOntCode/agents/stoa/`.

### 3.4 Active onboarding-listed code lacked module-level orientation in places

Targeted module docstrings were added to active onboarding-listed boundary, placement, runtime surface, integration, and diagnostic files where missing; active diagnostic modules in `agents/co/tests` were also given module-level orientation strings where absent. This improves cold onboarding but does not complete function-level docstring coverage for the whole repo.

### 3.5 Open-points file was updated

The now-implemented shared adapter action-validation guard was removed as an unresolved task and replaced with a maintenance instruction to keep the guard and source invariant extended for future adapters.

## 4. Checks run after fixes

The following checks were run successfully after the semantic relevance fixes:

```text
python tools/validate_toc_main.py
cd ChangeOntCode
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.canonical_structure_docs_invariants
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.candidate_surface_publication_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.relation_path_trace_diagnostics
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
python -m agents.co.tests.problem_contract_invariants
python -m agents.co.tests.runtime_contract_invariants
python -m agents.co.tests.shape_prior6_contract_invariants
python -m agents.co.tests.shape_prior6_active_path_invariants
python -m agents.co.tests.structure_dependency_invariants
python -m agents.co.tests.family_packet_alignment_invariants
python -m agents.co.tests.maintenance_replacement_family_invariants
python -m agents.co.tests.maintenance_replacement_runtime_wiring_invariants
python -m agents.co.tests.maintenance_replacement_stoa_baseline_invariants
python -m agents.co.tests.recursive_continuation_field_invariants
python -m agents.co.tests.recursive_continuation_field_relation_support_invariants
python -m agents.co.tests.continuation_state_invariants
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
python -m experiments.studies.architecture_acceptance_audit_v1
```

Trace status remained:

```text
structural_trace_validation_v1:
  status = PASS_WITH_WATCHPOINTS
  cases_with_watchpoints = 0
  relations_total = 80
  structural_relations = 16
  weak_decision_competition_relations = 64
  branch_internal_operation_rows = 20
  commitment_changed_cases = 1

relation_path_trace_v1:
  relations_total = 80
  non_rival_relations = 16
  commitment_action_changed_cases = 0
  commitment_mode_changed_cases = 1

architecture_acceptance_audit_v1:
  status = ACCEPTANCE_WATCHPOINTS_REMAIN
```

## 5. Current status after this audit

Cleaner:

```text
- the active onboarding route is more explicit;
- derivation graph snapshots now match current statement IDs;
- graph validation now guards against stale graph endpoints and Mermaid references;
- active adapters share a no-fallback native-action guard;
- the active route has better code orientation comments/docstrings;
- no generated __pycache__ files should be packaged in the release zip.
```

Still not claimed:

```text
- CO is proven;
- RCF novelty is proven;
- empirical usefulness is proven;
- broad benchmark superiority exists;
- consciousness follows from this runtime;
- all formulas and coefficients are fully grounded;
- quotient/equivalence tolerance is complete;
- recursion scheduling is complete;
- multi-step continuation identity is complete.
```

## 6. Remaining audit limits

The stricter classification found and corrected active-route issues, but the following limits remain:

```text
- historical/exploratory files were classified and scanned but not all semantically rederived line by line;
- support theory statements outside the current first-layer route remain support material unless promoted by the active route;
- function-level docstrings are still incomplete outside the active onboarding-listed files;
- generated prior-run artifacts remain historical evidence records, not current fresh runs;
- architecture_acceptance_audit_v1 still reports ACCEPTANCE_WATCHPOINTS_REMAIN.
```

## 7. Maintenance rule from this audit

When adding new adapters or runtime surfaces:

```text
- update the docs first if the target changes;
- pass public native action domains through require_kernel_action;
- add/extend no-fallback invariants;
- regenerate/validate theory graphs if statement IDs or edges change;
- update README, NEXT_AI_START_HERE, CANONICAL_STRUCTURE_MAP, OPEN_POINTS_AND_FUTURE_WORK, and this audit lineage when the active route changes.
```
