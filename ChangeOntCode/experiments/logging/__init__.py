# experiments/logging/__init__.py
from __future__ import annotations
from pathlib import Path

# Re-export existing utilities so imports work project-wide.
try:
    from .plots import quick_plot
except Exception:
    def quick_plot(*args, **kwargs):  # type: ignore
        raise NotImplementedError("plots.quick_plot not available")

__all__ = ["Path", "quick_plot"]
