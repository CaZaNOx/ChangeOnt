# J4b_counterfactual_bend.py
from typing import Any, Callable

def counterfactual_cost(edge_cost: Callable[[Any, Any], float],
                        old_edge: tuple,
                        new_edge: tuple) -> float:
    """
    Marginal cost difference if edge u->v is swapped to u'->v'.
    """
    (u, v) = old_edge
    (u2, v2) = new_edge
    try:
        return float(edge_cost(u2, v2)) - float(edge_cost(u, v))
    except Exception:
        return float("inf")
