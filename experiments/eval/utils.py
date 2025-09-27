# experiments/eval/utils.py
from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Dict, Iterable, List, Optional

def read_jsonl(path: Path) -> List[dict]:
    recs: List[dict] = []
    if not path.exists():
        return recs
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                recs.append(json.loads(line))
            except Exception:
                pass
    return recs

def list_agent_dirs(family_dir: Path) -> List[Path]:
    if not family_dir.exists():
        return []
    return [p for p in family_dir.iterdir() if p.is_dir() and (p / "metrics.jsonl").exists()]

def read_budget_row(path: Path) -> Optional[dict]:
    if not path.exists():
        return None
    try:
        with open(path, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
            return rows[0] if rows else None
    except Exception:
        return None

def safe_get(d: dict, key: str, default=None):
    try:
        return d.get(key, default)
    except Exception:
        return default
