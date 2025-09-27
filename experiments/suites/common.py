# experiments/suites/common.py
from __future__ import annotations
import subprocess, sys, yaml, json
from pathlib import Path
from typing import Dict, Any, List

def run_module(mod: str, *args: str) -> None:
    """
    Subprocess runner using the current interpreter.
    """
    exe = sys.executable or "python"
    cmd = [exe, "-m", mod, *args]
    subprocess.run(cmd, check=True)

def tmp_yaml(obj: Dict[str, Any], path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = yaml.safe_dump(obj, sort_keys=False)
    path.write_text(text, encoding="utf-8")
    return path

def ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)
