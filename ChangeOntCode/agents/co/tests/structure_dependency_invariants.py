"""Invariant/diagnostic module for structure dependency invariants.

Run with: python -m agents.co.tests.structure_dependency_invariants
"""
from __future__ import annotations

import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "agents" / "co"

RULES = {
    "boundary": [
        "agents.co.runtime.surfaces",
        "agents.co.runtime.support",
        "agents.co.core.elements",
        "agents.co.core.primitives",
        "agents.co.integration.translators",
    ],
    "placement": [
        "agents.co.adapters",
        "agents.co.boundary",
        "agents.co.runtime.surfaces",
        "agents.co.integration.translators",
        "environments",
    ],
    "runtime/surfaces": [
        "agents.co.adapters",
        "agents.co.boundary",
        "agents.co.integration.translators",
        "environments",
    ],
    "runtime/support": [
        "agents.co.adapters",
        "agents.co.boundary",
        "agents.co.integration.translators",
        "environments",
    ],
    "core/primitives": [
        "agents.co.boundary",
        "agents.co.adapters",
        "agents.co.integration.translators",
    ],
    "core/elements": [
        "agents.co.boundary",
        "agents.co.adapters",
        "agents.co.integration.translators",
    ],
}


def _imports_for(path: Path) -> list[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    found: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                found.append(alias.name)
        elif isinstance(node, ast.ImportFrom):
            mod = node.module or ""
            if node.level:
                continue
            found.append(mod)
    return found


def _iter_py(rel: str):
    base = ROOT / rel
    for p in base.rglob("*.py"):
        if "__pycache__" not in p.parts:
            yield p


def main() -> None:
    violations: list[str] = []
    for rel, banned in RULES.items():
        for path in _iter_py(rel):
            imports = _imports_for(path)
            for imp in imports:
                for bad in banned:
                    if imp == bad or imp.startswith(bad + "."):
                        violations.append(f"{path.relative_to(ROOT)} imports forbidden {imp}")
    assert not violations, "\n".join(violations)
    print("OK structure dependency invariants")


if __name__ == "__main__":
    main()
