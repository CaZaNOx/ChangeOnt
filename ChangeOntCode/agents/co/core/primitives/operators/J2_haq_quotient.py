# J2_haq_quotient.py
from typing import Iterable, Any, Callable, Dict, set as _set

def build_quotient_classes(items: Iterable[Any],
                           dist: Callable[[Any, Any], float],
                           epsilon: float) -> Dict[Any, set]:
    """
    Group items by epsilon-tolerant equivalence. Non-throwing.
    """
    items = list(items)
    eps = max(0.0, float(epsilon))
    classes: Dict[Any, set] = {}
    seen: set = _set()
    for x in items:
        if x in seen:
            continue
        rep = x
        cls = {x}
        for y in items:
            if y in seen:
                continue
            try:
                if dist(x, y) <= eps:
                    cls.add(y)
            except Exception:
                continue
        for y in cls:
            seen.add(y)
        classes[rep] = cls
    return classes
