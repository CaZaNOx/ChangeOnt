"""Invariant/diagnostic module for canonical manifest invariants.

Run with: python -m agents.co.tests.canonical_manifest_invariants
"""
from __future__ import annotations

from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    build_validated_co_core,
    load_co_manifest_params,
)


def main() -> None:
    params = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
    core = build_validated_co_core(
        params,
        study_name="canonical_manifest_invariants",
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    names = [e.__class__.__name__ for e in core.elements]
    assert names, "canonical manifest built an empty CO core"
    assert any(name.lower().endswith("commitmentsurface") for name in names), f"CommitmentSurface missing from canonical core: {names}"
    assert any(name.lower().endswith("candidateevidencesurface") for name in names), f"CandidateEvidenceSurface missing from canonical core: {names}"
    print("OK canonical manifest invariant")


if __name__ == "__main__":
    main()
