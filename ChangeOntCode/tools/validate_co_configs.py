#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import sys, yaml

ROOT = Path(__file__).resolve().parents[1]
CO_DIR = ROOT / 'experiments' / 'configs' / 'co_agents'

ALLOWED_AGENT_TOP = {"type", "name", "params"}
ALLOWED_PARAMS_TOP = {"name", "family", "math_policy", "allow_experimental", "meta_header", "header", "elements", "primitives", "groups", "final_fusion", "combinator", "semantic_overrides", "semantic_combinators", "translator", "logging", "run", "params", "meta"}
ALLOWED_GROUP_OPS = {"add", "gated", "order_sensitive"}


def die(msg: str) -> None:
    print(f"FAIL: {msg}")
    raise SystemExit(1)


def load_yaml(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def validate_manifest(path: Path) -> None:
    data = load_yaml(path)
    if not isinstance(data, dict):
        die(f"{path}: manifest root must be a mapping")
    agents = data.get('co_agents')
    if not isinstance(agents, list) or not agents:
        die(f"{path}: co_agents must be a non-empty list")
    for i, agent in enumerate(agents):
        if not isinstance(agent, dict):
            die(f"{path}: co_agents[{i}] must be a mapping")
        bad = sorted(k for k in agent.keys() if k not in ALLOWED_AGENT_TOP)
        if bad:
            die(f"{path}: co_agents[{i}] has unknown top-level keys {bad}")
        if agent.get('type') != 'co':
            die(f"{path}: co_agents[{i}] type must be 'co'")
        if not agent.get('name'):
            die(f"{path}: co_agents[{i}] missing name")
        params = agent.get('params') or {}
        if not isinstance(params, dict):
            die(f"{path}: co_agents[{i}].params must be a mapping")
        badp = sorted(k for k in params.keys() if k not in ALLOWED_PARAMS_TOP)
        if badp:
            die(f"{path}: co_agents[{i}].params has unknown keys {badp}")
        hdr = params.get('header', {})
        if hdr and (not isinstance(hdr, dict) or not (hdr.get('mode') or hdr.get('type'))):
            die(f"{path}: co_agents[{i}].params.header must provide mode/type")
        groups = params.get('groups', params.get('combinator', {}).get('groups') if isinstance(params.get('combinator'), dict) else None)
        if groups is not None:
            if not isinstance(groups, list):
                die(f"{path}: co_agents[{i}].params.groups must be a list")
            enabled = {k for k,v in (params.get('elements') or {}).items() if not isinstance(v, dict) or v.get('enabled', True)}
            for j,g in enumerate(groups):
                if not isinstance(g, dict):
                    die(f"{path}: group {j} must be a mapping")
                members = g.get('members') or []
                if not members:
                    die(f"{path}: group {j} must declare members")
                badm = sorted(m for m in members if m not in enabled)
                if badm:
                    die(f"{path}: group {j} references disabled/unknown members {badm}")
                op = str(g.get('operator', g.get('fusion', 'add')))
                if op not in ALLOWED_GROUP_OPS:
                    die(f"{path}: group {j} has unsupported operator {op}")
        ff = params.get('final_fusion')
        if ff is not None and not isinstance(ff, dict):
            die(f"{path}: co_agents[{i}].params.final_fusion must be a mapping")


def main() -> None:
    files = sorted(CO_DIR.glob('*.yaml'))
    if not files:
        die(f"No co manifest yaml files found in {CO_DIR}")
    for p in files:
        validate_manifest(p)
        print(f"PASS: {p.relative_to(ROOT)}")
    print('PASS: all CO manifests validated')


if __name__ == '__main__':
    main()
