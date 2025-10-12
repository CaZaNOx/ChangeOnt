# agents/co/integration/loader.py
from __future__ import annotations
import importlib
from pathlib import Path
from typing import Any, Dict, Iterator, List, Tuple

try:
    import yaml  # type: ignore
except Exception as e:
    raise SystemExit("PyYAML is required: pip install pyyaml") from e


def _resolve(symbol: Any) -> Any:
    """
    Resolve a symbol into a Python object.

    Accepts:
      - "pkg.mod:Class"
      - "pkg.mod.Class"
      - "pkg.mod" (module only)
      - {"path": "..."}
      - already-imported objects
    """
    if symbol is None:
        raise ValueError("Empty symbol")

    # Already a Python object?
    if not isinstance(symbol, str):
        if isinstance(symbol, dict) and "path" in symbol:
            symbol = symbol["path"]
        else:
            return symbol  # class/function/module already provided

    s = str(symbol).strip()
    if not s:
        raise ValueError("Empty string symbol")

    # Preferred explicit form: "pkg.mod:Name"
    if ":" in s:
        mod, name = s.rsplit(":", 1)
        return getattr(importlib.import_module(mod), name)

    # Try module import first (supports pure 'pkg.mod')
    try:
        return importlib.import_module(s)
    except Exception:
        pass

    # Then try dotted object path: "pkg.mod.Name"
    if "." in s:
        mod, name = s.rsplit(".", 1)
        return getattr(importlib.import_module(mod), name)

    raise ValueError(
        f"Unqualified symbol '{symbol}'. Use 'pkg.mod:Name', 'pkg.mod.Name', or a module path."
    )


def load_registry(path: str | Path) -> Dict[str, Any]:
    p = Path(path)
    data = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Registry YAML root must be a mapping: {p}")
    return data


def resolve_classes(registry: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    """
    Resolve every entry under each section to a Python object.
    """
    out: Dict[str, Dict[str, Any]] = {}
    for section, mapping in registry.items():
        if not isinstance(mapping, dict):
            continue
        resolved: Dict[str, Any] = {}
        for key, sym in mapping.items():
            try:
                resolved[key] = _resolve(sym)
            except Exception as e:
                raise RuntimeError(
                    f"Failed to resolve {section}.{key} -> {sym!r}: {e}"
                ) from e
        out[section] = resolved
    return out


def load_combos(glob_or_path: str | Path) -> Iterator[Tuple[str, Dict[str, Any]]]:
    p = Path(glob_or_path)
    if any(ch in str(p) for ch in "*?[]"):
        files = sorted(p.parent.glob(p.name))
    elif p.is_dir():
        files = sorted(p.glob("*.yaml"))
    else:
        files = [p]
    for fp in files:
        if not fp.exists():
            continue
        data = yaml.safe_load(fp.read_text(encoding="utf-8")) or {}
        if isinstance(data, dict):
            name = data.get("name") or fp.stem
            yield (str(name), data)