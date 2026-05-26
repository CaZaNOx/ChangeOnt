# Live Onboarding Traversal Report — 2026-05-15

Claim boundary: this report records a live traversal of the current onboarding path and the corrections made during that traversal. It is not empirical evidence for CO performance.

## Starting point

I started from the repo root `README.md`, followed its pointer to `NEXT_AI_START_HERE.md`, then followed the repo's stated reading path into:

```text
TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md
TheoryOfChange_main/00_Meta/FIRST_LAYER_CANONICAL_PATH.md
TheoryOfChange_main/00_Meta/TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md
ChangeOntCode/docs/kernel_spec/00_INDEX.md
ChangeOntCode/docs/kernel_spec/00A_DOCS_READING_GUIDE.md
ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md
ChangeOntCode/docs/kernel_spec/96_CONCEPTUAL_CLOSURE_LEDGER.md
ChangeOntCode/docs/kernel_spec/95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
ChangeOntCode/docs/kernel_spec/03C_IMPLEMENTATION_FIDELITY_STATUS.md
CANONICAL_STRUCTURE_MAP.md
OPEN_POINTS_AND_FUTURE_WORK.md
ChangeOntCode/README.md
ChangeOntCode/agents/co/runtime/surfaces/README.md
```

I also inspected the current runtime path around:

```text
ChangeOntCode/agents/co/runtime/surfaces/candidate_surface.py
ChangeOntCode/agents/co/runtime/surfaces/relation_surface.py
ChangeOntCode/agents/co/runtime/surfaces/commitment_surface.py
ChangeOntCode/agents/co/core/combinators/C_pipeline.py
ChangeOntCode/agents/co/combos/README.md
ChangeOntCode/agents/co/combos/CO_canonical_core.yaml
ChangeOntCode/agents/co/registries/registry.yaml
```

## Problems found and corrected

### 1. Competing onboarding reading orders

Problem: `NEXT_AI_START_HERE.md`, `CANONICAL_REFERENCE_STACK.md`, `00_INDEX.md`, `00A_DOCS_READING_GUIDE.md`, and `102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md` each gave a slightly different ordering. This made the repo less cold-onboarding safe.

Correction:

- `NEXT_AI_START_HERE.md` now gives one expanded route.
- `CANONICAL_REFERENCE_STACK.md` is explicitly the authoritative route.
- `00_INDEX.md` is explicitly a catalog, not a competing entrypoint.
- `00A_DOCS_READING_GUIDE.md` is explicitly the kernel-doc order after the top-level route.
- `102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md` now points to the same route and lists only the implementation-audit stack inside `kernel_spec`.

### 2. `_main` target architecture still carried an older chain

Problem: `TheoryOfChange_main/00_Meta/TARGET_KERNEL_ARCHITECTURE_DOCTRINE.md` still presented an older operational chain centered on descriptor position, rival objects, and descriptor-conditioned stabilization geometry. That conflicted with the current RelationSurface / RCF / CollapseCertificate / CommitmentSurface loop.

Correction: the file was rewritten as the current bridge doctrine:

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

It now preserves the boundary/adaptor anti-smuggling doctrine, branch-is-not-action rule, burden/relation/certificate structure, and current open debts without presenting the older chain as active.

### 3. CandidateSurface doc still used a pre-relation chain

Problem: `44_CANONICAL_CANDIDATE_SURFACE.md` still showed a clean chain ending at `CandidateEvidenceSurface → CommitmentSurface → action`, missing RelationSurface, RCF, and CollapseCertificate.

Correction: the chain now matches the active loop and clarifies that CandidateSurface is intake, not final readout.

### 4. RCF docs still described a pre-certificate path

Problem: `47_RECURSIVE_CONTINUATION_FIELD.md` and `49_RECURSIVE_CONTINUATION_FIELD_RUNTIME_CONTRACT.md` still described the RCF path as sitting directly between candidate/ContinuationState and CommitmentSurface.

Correction: both now include branch-internal burden operations, RelationSurface, CollapseCertificate, and CommitmentSurface in the correct order. `49` now distinguishes first-pass relation/certificate-aware implementation from a fully proven CO-native field.

### 5. RCF readiness doc still sounded pre-implementation

Problem: `50_RECURSIVE_CONTINUATION_FIELD_IMPLEMENTATION_READINESS.md` still said it was a gate before implementation.

Correction: its status now says it is a retained readiness/maintenance gate for future behavior-affecting RCF changes, because first-pass RCF v1 has already been implemented.

### 6. Continuation identity / relation contract status was stale

Problem: `76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md` still described implementation as pending and claimed RCF could only be called executable scaffold until implementation and telemetry existed.

Correction: it now states the current first-pass carrier status while preserving the stricter claim boundary: not full CO-native RCF, not algorithmic novelty, not empirical superiority.

### 7. Runtime surfaces README was incomplete

Problem: `ChangeOntCode/agents/co/runtime/surfaces/README.md` listed only candidate publication, commitment/finalization, and telemetry. It omitted RelationSurface, RCF, CollapseCertificate, and branch-internal operation carriers.

Correction: it now lists the full active surface chain and forbids hidden policy leakage, baseline-policy selection, and default action-label branch identity.

### 8. Maintenance family non-claims had stale robot/simulation wording

Problem: `75_MAINTENANCE_REPLACEMENT_MDP_PROBLEM_SPEC.md` still included a non-claim about not replacing robot/simulation hard-domain work and phrasing about strong results before executed logs exist, despite the file itself documenting a first negative comparison.

Correction: non-claims now focus on current maintenance truth: no DP win, no six-question proof, no empirical competitiveness claim, and no explaining away negative first-run evidence without structural audit.

### 9. Active onboarding path had one missing Obsidian link

Problem: `FIRST_LAYER_CANONICAL_PATH.md` linked to `OUTER_INNER_ROUTE_REUSE_DISCIPLINE`, which is not present in this snapshot.

Correction: the missing link was replaced with an explicit note that the file is absent and must not be relied on for current onboarding.

## Checks run after corrections

From `ChangeOntCode/`:

```text
python -m compileall -q agents environments experiments tools
python -m agents.co.tests.canonical_structure_docs_invariants
python -m agents.co.tests.code_vs_docs_pipeline_compliance_invariants
python -m agents.co.tests.certified_runtime_alignment_invariants
python -m agents.co.tests.no_classical_fallback_fail_closed_invariants
python -m agents.co.tests.candidate_surface_publication_invariants
python -m agents.co.tests.relation_surface_public_effect_invariants
python -m agents.co.tests.kernel_structure_carrier_alignment_invariants
python -m agents.co.tests.collapse_certificate_readout_invariants
python -m agents.co.tests.structural_trace_validation_invariants
python -m agents.co.tests.relation_path_trace_diagnostics
python -m agents.co.tests.canonical_manifest_invariants
python -m agents.co.tests.commitment_surface_readout_invariants
python -m agents.co.tests.continuation_state_invariants
python -m agents.co.tests.family_packet_alignment_invariants
python -m agents.co.tests.forbidden_shared_family_branching_invariants
python -m agents.co.tests.maintenance_replacement_family_invariants
python -m agents.co.tests.maintenance_replacement_runtime_wiring_invariants
python -m agents.co.tests.maintenance_replacement_stoa_baseline_invariants
python -m agents.co.tests.problem_contract_invariants
python -m agents.co.tests.recursive_continuation_field_invariants
python -m agents.co.tests.recursive_continuation_field_relation_support_invariants
python -m agents.co.tests.runtime_contract_invariants
python -m agents.co.tests.shape_prior6_active_path_invariants
python -m agents.co.tests.shape_prior6_contract_invariants
python -m agents.co.tests.structure_dependency_invariants
```

Study modules run:

```text
python -m experiments.studies.structural_trace_validation_v1
python -m experiments.studies.relation_path_trace_v1
python -m experiments.studies.architecture_acceptance_audit_v1
```

Observed status:

```text
structural_trace_validation_v1: PASS_WITH_WATCHPOINTS, cases_with_watchpoints = 0
relation_path_trace_v1: relations_total = 80, non_rival_relations = 16
architecture_acceptance_audit_v1: ACCEPTANCE_WATCHPOINTS_REMAIN
```

## Link audit boundary

The active onboarding path listed above now has zero unresolved markdown/wiki links under a repo-local resolver.

A broader repo-wide Obsidian link audit still finds unresolved shortlinks in older/non-onboarding theory graph material. Those were not fixed in this pass because doing so would require a separate graph-maintenance pass and could accidentally rewrite noncanonical or exploratory theory material.

## Remaining limits

This traversal did not prove:

```text
CO works empirically;
RCF is novel;
the formula ledger is complete;
quotient/recursion are solved;
multi-step continuation identity is solved;
consciousness follows from the runtime.
```

It also did not perform a line-by-line audit of every `_main` statement file or every Python function. It exercised and corrected the live onboarding path and the active architecture path it points to.
