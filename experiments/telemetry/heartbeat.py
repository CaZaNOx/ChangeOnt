# experiments/telemetry/heartbeat.py
from __future__ import annotations
import json, time
from pathlib import Path
from typing import Dict, Any

def write_progress(path: Path, payload: Dict[str, Any], min_interval_s: float = 0.25) -> None:
    """
    Lightweight heartbeat file. Throttles writes by min_interval_s.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    now = time.time()
    stamp = path.with_suffix(path.suffix + ".ts")
    last = 0.0
    if stamp.exists():
        try:
            last = float(stamp.read_text(encoding="utf-8").strip() or "0")
        except Exception:
            last = 0.0
    if now - last < min_interval_s:
        return
    path.write_text(json.dumps(payload), encoding="utf-8")
    stamp.write_text(str(now), encoding="utf-8")
