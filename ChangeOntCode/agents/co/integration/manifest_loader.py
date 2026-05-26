"""Load and normalize runtime manifests for the canonical CO assembly path.

Manifest loading is configuration plumbing only; it must not introduce alternate
policy routes or non-CO rescue components.
"""
from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, Iterator, Tuple

from agents.co.integration.loader import load_registry, resolve_classes, load_combos

__all__ = ["load_registry", "resolve_classes", "load_combos"]
