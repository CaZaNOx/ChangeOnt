# experiments/plotting/common.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import json

try:
    from experiments.plotting.plotting import save_quick_plot
except Exception:
    save_quick_plot = None  # type: ignore

def quick_plot_if_available(metrics_path: Path, out_path: Path, title: str) -> None:
    if save_quick_plot is None:
        return
    try:
        save_quick_plot(metrics_path, out_path, title=title)
    except Exception:
        pass
