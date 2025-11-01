# J2_haq_quotient.py

from typing import Iterable, Any, Callable, Dict, Set


def build_quotient_classes(
    items: Iterable[Any],
    dist: Callable[[Any, Any], float],
    epsilon: float
) -> Dict[Any, Set[Any]]:
    """
    Group items by epsilon-tolerant equivalence. Non-throwing.
    """
    xs = list(items)
    eps = max(0.0, float(epsilon))

    classes: Dict[Any, Set[Any]] = {}
    seen: Set[Any] = set()

    for x in xs:
        if x in seen:
            continue

        rep = x
        cls: Set[Any] = {x}

        for y in xs:
            if y in seen:
                continue
            try:
                if dist(x, y) <= eps:
                    cls.add(y)
            except Exception:
                # ignore distance failures
                continue

        for y in cls:
            seen.add(y)

        classes[rep] = cls

    return classes