#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys
import yaml

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT
EL_DIR = CODE / "agents" / "co" / "core" / "elements"
CO_DIR = CODE / "experiments" / "configs" / "co_agents"

ELEMENT_CLASS_FILES = [
    "EA_haq.py", "EB_ghvc.py", "EC_identity.py", "EG_density_precision.py",
    "EI_change_operators.py", "E0_vote_bridge.py", "action_head.py",
    "ED_gauge_warp.py", "EE_compressibility.py", "EF_router_gil.py",
    "EH_breadth_depth.py", "EJ_order_asymmetry.py",
]

ALLOWED_PARAMS_TOP = {
    "name", "family", "math_policy", "allow_experimental",
    "meta_header", "header", "elements", "primitives", "groups",
    "final_fusion", "combinator", "semantic_overrides", "semantic_combinators",
    "translator", "logging", "run", "params", "meta",
}

def fail(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)

def main() -> None:
    # element declaration completeness
    for fn in ELEMENT_CLASS_FILES:
        text = (EL_DIR / fn).read_text(encoding="utf-8")
        if "WEIGHT_ROLE" not in text:
            fail(f"{fn} missing WEIGHT_ROLE")
        if "COMPOSITION_ROLE" not in text:
            fail(f"{fn} missing COMPOSITION_ROLE")
        if "PRIMITIVE_DEPS" not in text:
            fail(f"{fn} missing PRIMITIVE_DEPS")
    # config grammar check
    for p in sorted(CO_DIR.glob("*.yaml")):
        data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        agents = data.get("co_agents") or []
        if not isinstance(agents, list) or not agents:
            fail(f"{p.name}: co_agents missing")
        for i, agent in enumerate(agents):
            params = agent.get("params") or {}
            bad = sorted(k for k in params if k not in ALLOWED_PARAMS_TOP)
            if bad:
                fail(f"{p.name}: co_agents[{i}] unknown params keys {bad}")
            if "action_head" in (params.get("elements") or {}):
                ah = params["elements"]["action_head"] or {}
                if ah.get("enabled", True) and "groups" not in params and "groups" not in (params.get("combinator") or {}):
                    fail(f"{p.name}: co_agents[{i}] enabled action_head without explicit groups")
    # runtime path honesty markers
    for rel in [
        "archive/legacy_runtime/co_core_engine_legacy.py",
        "archive/legacy_runtime/co_suite_hooks_legacy.py",
        "archive/legacy_runtime/co_registry_factories_legacy.py",
    ]:
        txt = (CODE / rel).read_text(encoding="utf-8")
        if "inactive" not in txt.lower() and "legacy" not in txt.lower():
            fail(f"{rel} missing inactive/legacy marker")
    print("DONE_STATE_OK")

if __name__ == "__main__":
    main()
