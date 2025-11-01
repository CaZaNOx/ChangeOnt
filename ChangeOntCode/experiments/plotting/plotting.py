from __future__ import annotations
from pathlib import Path
from experiments.logging import quick_plot

def save_quick_plot(metrics_path: Path, out_png: Path, title: str | None = None) -> None:
    quick_plot(Path(metrics_path), Path(out_png), title=title)
