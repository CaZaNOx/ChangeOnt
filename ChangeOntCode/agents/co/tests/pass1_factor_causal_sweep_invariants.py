"""Invariants for pass1_factor_causal_sweep_v1 output."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "outputs" / "pass1_factor_causal_sweep_v1" / "summary.json"


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> None:
    _assert(OUT.exists(), f"missing summary: {OUT}")
    data = json.loads(OUT.read_text(encoding="utf-8"))
    _assert(data.get("study") == "pass1_factor_causal_sweep_v1", "wrong study")
    comps = data.get("comparisons", {})
    required = {
        "bandit/easy_public_bandit",
        "renewal/noisy_renewal",
        "maze/static_visible_5x5",
        "latent_mechanism/easy_visible",
        "latent_mechanism/hidden_depth2",
        "maintenance_replacement/bandit_like",
        "maintenance_replacement/middle",
        "maintenance_replacement/renewal_like",
    }
    _assert(required.issubset(set(comps)), f"missing comparisons: {sorted(required - set(comps))}")
    for key, val in comps.items():
        _assert("best_baseline_agent" in val, f"{key}: no baseline")
        _assert("best_co_variant_agent" in val, f"{key}: no co variant")
        groups = val.get("factor_group_effects", {})
        _assert("shape_counterfactual" in groups, f"{key}: no shape factor group")
        _assert("mechanism_ablation" in groups, f"{key}: no mechanism ablation group")
    non_claims = " ".join(data.get("non_claims", []))
    _assert("Counterfactual" in non_claims and "not canonical" in non_claims, "claim boundary missing")
    print("pass1_factor_causal_sweep_invariants: PASS")

if __name__ == "__main__":
    main()
