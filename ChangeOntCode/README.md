# ChangeOntCode

`ChangeOntCode/` contains the current experimental CO runtime, problem environments, diagnostics, and comparison baselines. It implements the active kernel-doc target under `docs/kernel_spec/`.

The current code should be evaluated first for structural fidelity to the docs, then for empirical behavior. Do not treat reward performance as evidence unless the translator boundary, runtime path, logs, baselines, and oracle exclusions have been checked.

## Active runtime path

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

Key locations:

```text
docs/kernel_spec/00_INDEX.md
docs/kernel_spec/00A_DOCS_READING_GUIDE.md
docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md

agents/co/boundary/
agents/co/adapters/
agents/co/placement/
agents/co/runtime/surfaces/
agents/co/integration/
agents/co/tests/

environments/
experiments/
```

## Runtime responsibilities

Adapters and boundary code translate native observations into public facts, legal/admissible action expressions, and public burden-effect facts. They must not publish optimality, hidden state conclusions, baseline values, or route-level policy answers.

CandidateSurface creates candidate rows and public candidate telemetry. Actions are interface expressions; they are not automatically continuation branches.

RelationSurface derives kernel-side relations from public burden/effect facts. It distinguishes structural relations from weak procedural decision-slot competition.

RecursiveContinuationField updates relation-aware continuation state, including debt, relief support, grey pressure, recursion demand, collapse readiness, quotient markers, and viability.

CollapseCertificate checks whether collapse into a branch is earned and preserves reasons such as unresolved rivalry, quotient resolution, burden relief/cancellation, hiddenness, grey structure, and recursion demand.

CommitmentSurface is the final readout. It must respect certificate gates and fail closed rather than rescue missing CO evidence with a non-CO selection path.

## Verification commands

Run from this directory:

```bash
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
```

For broader work, add family-specific invariants and study modules only after the structural checks remain clean.

## Baselines

Baseline algorithms live outside the CO runtime path and are used for comparison. If a baseline has privileged information, label it as an oracle or upper bound. Do not use baseline behavior as a fallback inside evidence-bearing CO runtime.

## Current limitations

The code is architecture-aligned enough for controlled diagnostics, but formula grounding, quotient/equivalence tolerance, recursion scheduling, multi-step continuation identity, and empirical validation remain open. See root `OPEN_POINTS_AND_FUTURE_WORK.md`.

## 2026-05-16 validation additions

New stage-gate diagnostics/live studies:

- `experiments/studies/real_family_manual_trace_review_v1.py`
- `experiments/studies/frozen_empirical_sanity_smoke_v1.py`
- `agents/co/tests/real_family_manual_trace_review_invariants.py`
- `agents/co/tests/frozen_empirical_sanity_smoke_invariants.py`
- `agents/co/tests/maintenance_runner_no_rescue_invariants.py`

These support structural/manual trace review and small frozen runtime sanity only. They are not broad reward benchmark evidence.
