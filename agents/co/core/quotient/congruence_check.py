from future import annotations
from typing import Callable, Dict, Hashable, Iterable, Tuple

def tau_congruence_ok(
    classes: Iterable[Hashable],
    edge_cost_lookup: Callable[[Hashable, Hashable], float | None],
    rep_of: Dict[Hashable, Hashable],
    tau: float,
    ) -> bool:
    """
    Empirical congruence test: for any action available from a representative,
    the class-lifted cost deviates ≤ tau compared to any other member's action.
    This checks representativeness is not artifact-dependent.
    Implementation:
    - for each class C, pick its rep r
    - gather outgoing edges from any member u∈C
    - compare costs c(r->v) vs c(u->v) when v is in same target class
    - allow None edges (unobserved) to skip that comparison
    """
    # build reverse: class -> members
    members_by_class: Dict[Hashable, list] = {}
    for u, r in rep_of.items():
        members_by_class.setdefault(r, []).append(u)

    for C in classes:
        mems = members_by_class.get(C, [])
        if not mems:
            continue
        r = mems[0]  # canonical rep for this test
        # collect targets seen from any member
        targets: set[Hashable] = set()
        for u in mems:
            # edges out of u: we don't have adjacency; probe known targets via rep_of keys
            # caller should ensure edge_cost_lookup returns None for unknown (u,v)
            for v in rep_of.keys():
                if edge_cost_lookup(u, v) is not None:
                    targets.add(v)
        for v in targets:
            cr = edge_cost_lookup(r, v)
            for u in mems:
                cu = edge_cost_lookup(u, v)
                if cr is None or cu is None:
                    continue
                if abs(float(cr) - float(cu)) > float(tau):
                    return False
    return True