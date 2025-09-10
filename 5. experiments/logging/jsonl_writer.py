from __future__ import annotations
import os, json
from typing import Any, Dict, Iterable, Optional, TextIO

class JSONLWriter:
    """Simple JSONL writer with directory creation and context manager support."""
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        self._f: TextIO = open(path, "w", encoding="utf-8")

    def write(self, row: Dict[str, Any]) -> None:
        self._f.write(json.dumps(row) + "\n")

    def writemany(self, rows: Iterable[Dict[str, Any]]) -> None:
        for r in rows:
            self.write(r)

    def close(self) -> None:
        try:
            self._f.close()
        except Exception:
            pass

    def __enter__(self) -> "JSONLWriter":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
