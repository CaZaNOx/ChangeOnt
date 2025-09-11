from __future__ import annotations
from typing import Any, Callable, Iterable, Dict, List, Tuple

def R_tau(
    u: Dict[str, Any],
    v: Dict[str, Any],
    *,
    tau: float,
    distance: Callable[[list[int], list[int]], float],
    header_ok: Callable[[dict, dict], bool],
) -> bool:
    """
    Bend-equivalence predicate before closure:
    - Compare recent token traces via distance; check header agreement.
    - Not necessarily transitive -> we will take equivalence closure elsewhere.
    """
    if not header_ok(u.get("header", {}), v.get("header", {})):
        return False
    d = distance(u.get("trace", []), v.get("trace", []))
    return d <= tau
