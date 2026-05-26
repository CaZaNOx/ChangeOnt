"""Verify the certified canonical docs/readme structure remains present and legacy active docs stay removed.

Run with: python -m agents.co.tests.canonical_structure_docs_invariants
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
KERNEL = ROOT / "docs" / "kernel_spec"

# This invariant tracks the certified canonical documentation target, not older
# pre-certification/provenance docs that were removed from the active tree.
REQUIRED = [
    KERNEL / "00_INDEX.md",
    KERNEL / "00A_DOCS_READING_GUIDE.md",
    KERNEL / "01B_TARGET_ARCHITECTURE_CONTRACT.md",
    KERNEL / "03C_IMPLEMENTATION_FIDELITY_STATUS.md",
    KERNEL / "03_WIRING_MAP.md",
    KERNEL / "04_GOAL_STATE_CO_ALIGNED_KERNEL.md",
    KERNEL / "05_SURFACES" / "README.md",
    KERNEL / "05_SURFACES" / "CandidateSurface.md",
    KERNEL / "05_SURFACES" / "RelationSurface.md",
    KERNEL / "05_SURFACES" / "CollapseCertificate.md",
    KERNEL / "05_SURFACES" / "CommitmentSurface.md",
    KERNEL / "08_TRANSLATORS" / "README.md",
    KERNEL / "09_ACCEPTANCE" / "README.md",
    KERNEL / "74_SIX_QUESTION_SHAPE_PRIOR.md",
    KERNEL / "76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md",
    KERNEL / "77_PUBLIC_BURDEN_EFFECT_SCHEMA.md",
    KERNEL / "78_RUNTIME_SAFETY_AND_FALLBACK_CONTRACT.md",
    KERNEL / "79_CANDIDATE_AND_COMMITMENT_FORMULA_GROUNDING_PROTOCOL.md",
    KERNEL / "84_BURDEN_OPERATION_ALGEBRA.md",
    KERNEL / "87_RELATION_SURFACE_PUBLIC_EFFECT_IMPLEMENTATION.md",
    KERNEL / "91_EARNED_COLLAPSE_CERTIFICATE_IMPLEMENTATION.md",
    KERNEL / "95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md",
    KERNEL / "96_CONCEPTUAL_CLOSURE_LEDGER.md",
    KERNEL / "97_QUOTIENT_EQUIVALENCE_TARGET_STATE.md",
    KERNEL / "98_RECURSION_DEMAND_TARGET_STATE.md",
    KERNEL / "99_RELATION_ALGEBRA_TARGET_STATE.md",
    KERNEL / "100_SHAPE_PRIOR_FORMULA_AND_EVIDENCE_STATUS.md",
    KERNEL / "101_RCF_ALGORITHM_COMPARISON_AND_CONSCIOUSNESS_SCOPE.md",
    KERNEL / "102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md",
    KERNEL / "103_DYNAMIC_SHAPE_FIELD_CONTRACT.md",
    KERNEL / "104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md",
    ROOT / "agents" / "co" / "boundary" / "README.md",
    ROOT / "agents" / "co" / "placement" / "README.md",
    ROOT / "agents" / "co" / "runtime" / "surfaces" / "README.md",
    ROOT / "agents" / "co" / "runtime" / "support" / "README.md",
    ROOT / "agents" / "co" / "core" / "primitives" / "README.md",
    ROOT / "agents" / "co" / "core" / "elements" / "README.md",
    ROOT / "agents" / "co" / "adapters" / "README.md",
]

FORBIDDEN_ACTIVE_DOCS = [
    KERNEL / "30_CANONICAL_ARCHITECTURE_AND_LAYER_RULES.md",
    KERNEL / "31_HOW_TO_ADD_A_NEW_PROBLEM_FAMILY.md",
    KERNEL / "32_DEPENDENCY_AND_IMPORT_RULES.md",
    KERNEL / "33_NAMING_AND_DEPRECATED_PATHS.md",
    KERNEL / "05_SURFACES" / "ActionHead.md",
    KERNEL / "05_SURFACES" / "VoteBridge.md",
]


def main() -> None:
    missing = [str(p.relative_to(ROOT)) for p in REQUIRED if not p.exists()]
    assert not missing, "missing required certified structure docs/readmes: " + ", ".join(missing)
    present_forbidden = [str(p.relative_to(ROOT)) for p in FORBIDDEN_ACTIVE_DOCS if p.exists()]
    assert not present_forbidden, "removed legacy docs reappeared in active tree: " + ", ".join(present_forbidden)
    print("OK canonical certified structure docs invariants")


if __name__ == "__main__":
    main()
