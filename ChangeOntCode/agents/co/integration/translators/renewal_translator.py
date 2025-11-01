# agents/co/integration/translators/renewal_translator.py
from __future__ import annotations
from typing import Any, Dict, Tuple, List
from agents.co.core.contracts.signals import normalize_scores

def translate(
    observation: Dict[str, Any],
    header: Any,
    primitives: Dict[str, Any],
    co_bus: Dict[str, Any],
    cfg: Dict[str, Any],
) -> Tuple[Dict[Any, float], set, Dict[str, Any]]:
    """
    Score symbols using n-gram model when available; fallback predict-last.
    """
    A = int(observation.get("A", 0))
    actions: List[int] = list(observation.get("action_space") or list(range(A)))
    mask: set = set()
    if A <= 0:
        return ({}, mask, {"reason":"no_alphabet"})

    obs_sym = int(observation.get("obs", 0))
    # Prefer primitive model
    ng = primitives.get("ngram_model")
    scores: Dict[int, float] = {}
    if ng is not None and all(hasattr(ng, k) for k in ("predict_proba","ensure")):
        try:
            ng.ensure(A)
            proba = ng.predict_proba()  # should return length-A probabilities or dict
            if isinstance(proba, dict):
                for a in actions:
                    scores[a] = float(proba.get(a, 0.0))
            else:
                for a in actions:
                    scores[a] = float(proba[a]) if a < len(proba) else 0.0
        except Exception:
            pass

    if not scores:
        # fallback: predict-last heuristic
        scores = {a: (1.0 if a == obs_sym else 0.0) for a in actions}

    return (normalize_scores(scores), mask, {"fallback": not bool(scores)})