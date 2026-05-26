"""Invariant/diagnostic module for forbidden shared family branching invariants.

Run with: python -m agents.co.tests.forbidden_shared_family_branching_invariants
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3] / "agents" / "co"
CHECK_DIRS = [
    ROOT / "placement",
    ROOT / "runtime" / "surfaces",
    ROOT / "runtime" / "support",
]
PATTERNS = [
    re.compile(r"['\"](?:bandit|renewal|maze|latent|langton|collatz|arw)['\"]"),
    re.compile(r"\bfamily\s*=="),
    re.compile(r"\bif\s+[^\n]*\bfamily\b"),
]


def main() -> None:
    violations: list[str] = []
    for base in CHECK_DIRS:
        for path in base.rglob("*.py"):
            text = path.read_text()
            for pat in PATTERNS:
                if pat.search(text):
                    violations.append(f"{path.relative_to(ROOT)} matched {pat.pattern}")
    assert not violations, "\n".join(violations)
    print("OK forbidden shared family branching invariants")


if __name__ == "__main__":
    main()
