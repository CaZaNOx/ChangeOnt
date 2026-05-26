"""Invariants for certified docs -> code runtime alignment.

These checks reject inactive runtime residues that could reintroduce a non-CO
route or make the certified docs ambiguous.

Run:
    python -m agents.co.tests.certified_runtime_alignment_invariants
"""
from __future__ import annotations

from pathlib import Path

from agents.co.core.contracts.placement_contract import build_runtime_contract
from agents.co.core.combinators.C_gate import C_Gate
from agents.co.core.combinators.C_math_policy import C_MathPolicy
from agents.co.core.combinators.C_fuse import C_Fuse
from agents.co.headers.H_CS import HeaderCS
from agents.co.headers.H_ID import HeaderID


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def _raises(fn, msg: str) -> None:
    try:
        fn()
    except Exception:
        return
    raise AssertionError(msg)


def main() -> None:
    root = Path(__file__).resolve().parents[3]
    forbidden_dirs = [
        root / "agents/co/combos/legacy",
        root / "agents/co/placement/legacy",
        root / "agents/co/integration/legacy",
        root / "agents/co/tests/legacy",
    ]
    for p in forbidden_dirs:
        _assert(not p.exists(), f"retired runtime/test directory still present: {p}")

    combo = (root / "agents/co/combos/CO_canonical_core.yaml").read_text(encoding="utf-8")
    _assert("combinators:" not in combo, "canonical combo must not configure route/fusion/math combinators")
    _assert("math_policy: co" in combo, "canonical combo must declare CO-only math policy")

    registry = (root / "agents/co/registries/registry.yaml").read_text(encoding="utf-8")
    _assert("C_ClassicOps" not in registry, "registry must not expose retired non-CO operations")
    _assert("C_MathPolicy" not in registry, "registry must not expose math-policy router")
    _assert("C_Gate" not in registry, "registry must not expose route gate")
    _assert("CS:" not in registry and "ID:" not in registry, "registry must not expose retired headers")

    contract = build_runtime_contract({"problem_contract": {"actions": {"count": 2}, "decision_scope": "anchor"}})
    _assert("legacy_placement" not in contract, "runtime contract must not expose retired placement payloads")
    _assert(contract["problem_contract"]["decision_scope"] == "anchor", "explicit public problem scope must be retained")

    _assert(C_Gate().route(None, {}) == "co", "route guard must report only co")
    _raises(lambda: C_Gate(prefer="non_co"), "route guard must reject non-CO route requests")
    _assert(C_MathPolicy().selected() == "co", "math policy guard must report only co")
    _raises(lambda: C_MathPolicy(policy="non_co"), "math policy guard must reject non-CO policies")
    _raises(lambda: C_Fuse(method="softmax"), "C_Fuse must reject unsupported score-only softmax method")
    _raises(lambda: HeaderCS(), "retired H_CS must not instantiate")
    _raises(lambda: HeaderID(), "retired H_ID must not instantiate")


if __name__ == "__main__":
    main()
