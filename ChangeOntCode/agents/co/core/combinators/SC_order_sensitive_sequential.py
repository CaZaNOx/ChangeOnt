from __future__ import annotations
from typing import Dict, Any, Iterable, Tuple


class SC_OrderSensitiveSequential:
    """
    Semantic combinator for order-sensitive sequential accumulation.
    Later surfaces can amplify or attenuate earlier ones without becoming
    a purely symmetric additive blend.
    """

    @staticmethod
    def combine_sequence(parts: Iterable[Tuple[Dict[Any, float], float]], decay: float = 0.85) -> Dict[Any, float]:
        out: Dict[Any, float] = {}
        cur_decay = 1.0
        for surf, weight in parts:
            if not isinstance(surf, dict):
                continue
            w = float(weight)
            for key, val in surf.items():
                out[key] = out.get(key, 0.0) + cur_decay * w * float(val)
            cur_decay *= float(decay)
        return out
