# experiments/plotting/util.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
import csv

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def write_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    keys = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def safe_import_plt():
    try:
        import matplotlib.pyplot as plt  # type: ignore
        return plt
    except Exception:
        return None
