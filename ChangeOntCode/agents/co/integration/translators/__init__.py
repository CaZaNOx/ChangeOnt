# agents/co/integration/translators/__init__.py
from __future__ import annotations
from typing import Any, Dict, Tuple, Callable

TranslatorFn = Callable[[Dict[str, Any], Any, Dict[str, Any], Dict[str, Any], Dict[str, Any]], Tuple[Dict[Any, float], set, Dict[str, Any]]]

def get_translator_for_family(family: str):
    fam = (family or "").lower()
    if fam == "maze":
        from .maze_translator import translate as fn
        return fn
    if fam == "bandit":
        from .bandit_translator import translate as fn
        return fn
    if fam == "renewal":
        from .renewal_translator import translate as fn
        return fn
    return None