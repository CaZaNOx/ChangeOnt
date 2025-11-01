# agents/co/core/combinators/C_transform_chain.py
from __future__ import annotations
from typing import Callable, Dict, Any, List

ActionScores = Dict[Any, float]
Transform = Callable[[ActionScores, Any, Dict[str, Any], Dict[str, Any]], ActionScores]

class C_TransformChain:
    """
    Applies a list of transforms in ORDER to an action->cost map.
    This is where ab ≠ ba lives: order matters (gauge -> bend -> closure -> residuation -> mdl -> loopiness).
    """

    def __init__(self, transforms: List[Transform] | None = None):
        self.transforms: List[Transform] = list(transforms or [])

    def add(self, T: Transform) -> "C_TransformChain":
        self.transforms.append(T)
        return self

    def apply(self, scores: ActionScores, header: Any, primitives: Dict[str, Any], signals: Dict[str, Any]) -> ActionScores:
        out = dict(scores or {})
        for T in self.transforms:
            try:
                out = T(out, header, primitives, signals) or {}
            except Exception:
                # fail-safe: keep previous out if a transform errors
                continue
        return out