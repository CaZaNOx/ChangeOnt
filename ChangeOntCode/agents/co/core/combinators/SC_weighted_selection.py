from __future__ import annotations
from typing import Dict, Any, Optional


class SC_WeightedSelection:
    """
    Semantic combinator: weighted competition/selection among candidates.
    Modes:
      - argmax (default): return max weighted score
      - blend: weighted average of candidate values
    """
    @staticmethod
    def select(
        candidates: Dict[Any, float],
        weights: Optional[Dict[Any, float]] = None,
        mode: str = "argmax",
    ) -> Dict[str, Any]:
        if not candidates:
            return {"choice": None, "score": 0.0}
        if weights is None:
            weights = {k: 1.0 for k in candidates.keys()}

        # compute weighted scores
        weighted = {k: float(candidates[k]) * float(weights.get(k, 1.0)) for k in candidates.keys()}

        if mode == "blend":
            total_w = sum(float(weights.get(k, 1.0)) for k in candidates.keys())
            if total_w <= 0.0:
                return {"choice": None, "score": 0.0}
            blended = sum(float(candidates[k]) * float(weights.get(k, 1.0)) for k in candidates.keys()) / total_w
            choice = max(weighted, key=weighted.get)
            return {"choice": choice, "score": float(blended), "weighted": weighted}

        # argmax by weighted score
        choice = max(weighted, key=weighted.get)
        return {"choice": choice, "score": float(weighted.get(choice, 0.0)), "weighted": weighted}
