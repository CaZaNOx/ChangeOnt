from __future__ import annotations
from typing import Any, Dict, Tuple, Callable, Optional

TranslatorFn = Callable[[Dict[str, Any], Any, Dict[str, Any], Dict[str, Any], Dict[str, Any]], Tuple[Dict[Any, float], set, Dict[str, Any]]]
FeedbackTranslatorFn = Callable[[Dict[str, Any], Dict[str, Any], Any, Dict[str, Any], Dict[str, Any], Dict[str, Any]], Dict[str, Any]]

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


def get_feedback_translator_for_family(family: str) -> Optional[FeedbackTranslatorFn]:
    fam = (family or "").lower()
    if fam == "maze":
        from .maze_translator import translate_feedback as fn
        return fn
    if fam == "bandit":
        from .bandit_translator import translate_feedback as fn
        return fn
    if fam == "renewal":
        from .renewal_translator import translate_feedback as fn
        return fn
    return None
