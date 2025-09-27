# experiments/io/writers.py
from __future__ import annotations
import json, shutil, time, csv
from pathlib import Path
from typing import Tuple, List, Dict, Any

# Optional kernel writer
try:
    from kernel.logging import JSONLWriter as KernelWriter  # type: ignore
except Exception:
    KernelWriter = None  # type: ignore

def open_jsonl_writer(path: Path, header: Dict[str, Any]) -> Tuple[object, str]:
    """
    Returns (writer, writer_mode_tag). Writer has .write(dict) and .close().
    Header is always written (as first record or via write_header).
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    if KernelWriter is not None:
        try:
            w = KernelWriter(path)  # type: ignore[call-arg]
            try:
                w.write_header(header)  # type: ignore[attr-defined]
            except Exception:
                w.write({"record_type": "header", **header})
            return w, "kernel_jsonl"
        except Exception:
            pass

    class _Local:
        def __init__(self, p: Path, hdr: Dict[str, Any]):
            self._f = open(p, "w", encoding="utf-8")
            self._f.write(json.dumps({"record_type": "header", **hdr}) + "\n")
            self._f.flush()
        def write(self, rec: Dict[str, Any]) -> None:
            self._f.write(json.dumps(rec) + "\n")
        def close(self) -> None:
            try:
                self._f.flush()
            finally:
                self._f.close()

    return _Local(path, header), "local_jsonl"


def write_budget_csv(path: Path, rows: List[Dict[str, Any]]) -> None:
    """
    Always writes at least one DATA row (never header-only).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    rows = rows or [{"params_bits": 0, "flops_per_step": 0, "memory_bytes": 0}]
    cols = list(rows[0].keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)


def safe_copy(src: Path, dst: Path, retries: int = 12, delay: float = 0.12) -> None:
    """
    Windows-safe copy that retries when files are momentarily locked.
    """
    if not src.exists():
        return
    dst.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(retries):
        try:
            shutil.copy2(src, dst)
            return
        except PermissionError:
            time.sleep(delay)
    shutil.copy2(src, dst)
