"""Build and validate assembled CO runtime components from manifests/configs."""

from __future__ import annotations
from typing import Any, Dict

from agents.co.integration.core_builder import build_co_core

__all__ = ["build_co_core"]
