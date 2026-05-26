"""Compatibility export for canonical component instantiation.

The implementation lives in core_builder; this module preserves the import
surface without adding an alternate assembly path.
"""
from __future__ import annotations
from typing import Any, Dict, List, Tuple

from agents.co.integration.core_builder import _instantiate_components

__all__ = ["_instantiate_components"]
