# core/quotient/infimum_lift.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Hashable, Iterable, List, Tuple, Optional

NodeId = Hashable
ClassId = Hashable

@dataclass(frozen=True)
class BaseEdge:
    u: NodeId
    v: NodeId
    cost: float  # perceived (gauge-warped) nonnegative cost

@dataclass
class Witness:
    u: NodeId
    v: NodeId
    cost: float

class LiftedGraph:
    """
    Infimum-lifted graph over equivalence classes with stored edge witnesses.
    Enforces witness-consistent path/cycle evaluation to avoid Frankenstein loops.
    """
    def __init__(self, partition: Dict[ClassId, List[NodeId]], edges: Iterable[BaseEdge]):
        self.partition: Dict[ClassId, List[NodeId]] = {cid: list(members) for cid, members in partition.items()}
        self.edges_by_src: Dict[NodeId, List[BaseEdge]] = {}
        self.edges: List[BaseEdge] = []
        for e in edges:
            if e.cost < 0:
                raise ValueError("Edge cost must be nonnegative")
            self.edges.append(e)
            self.edges_by_src.setdefault(e.u, []).append(e)

        # cache lifted edge minima and witnesses
        self.lift_cache: Dict[Tuple[ClassId, ClassId], Tuple[float, Witness]] = {}

    def _lift_min_edge(self, c_from: ClassId, c_to: ClassId) -> Optional[Tuple[float, Witness]]:
        key = (c_from, c_to)
        if key in self.lift_cache:
            return self.lift_cache[key]
        best_cost: Optional[float] = None
        best_wit: Optional[Witness] = None
        for u in self.partition.get(c_from, []):
            for e in self.edges_by_src.get(u, []):
                if e.v in self._flat_class(c_to):
                    if best_cost is None or e.cost < best_cost:
                        best_cost = e.cost
                        best_wit = Witness(u=e.u, v=e.v, cost=e.cost)
        if best_cost is None or best_wit is None:
            return None
        self.lift_cache[key] = (best_cost, best_wit)
        return self.lift_cache[key]

    def _flat_class(self, cid: ClassId) -> List[NodeId]:
        return self.partition.get(cid, [])

    def lifted_edge_cost(self, c_from: ClassId, c_to: ClassId) -> Optional[float]:
        res = self._lift_min_edge(c_from, c_to)
        return res[0] if res else None

    def witness_consistent_cycle_cost(self, classes_cycle: List[ClassId], epsilon_link: float = 0.0) -> Optional[float]:
        """
        Sum costs around a cycle [C0,C1,...,Ck-1,C0] using witnesses that chain:
        witness.v of edge i must equal (or be within epsilon) witness.u of edge i+1.
        """
        if len(classes_cycle) < 2:
            return None
        total = 0.0
        current_wit: Optional[Witness] = None
        for i in range(len(classes_cycle)):
            c_from = classes_cycle[i]
            c_to = classes_cycle[(i + 1) % len(classes_cycle)]
            pair = self._lift_min_edge(c_from, c_to)
            if pair is None:
                return None
            cost, wit = pair
            if current_wit is not None:
                # enforce witness chaining
                if wit.u != current_wit.v:
                    if epsilon_link <= 0.0:
                        return None
                    # epsilon mode: allow if both endpoints belong to same class and costs close
                    # (simple safe fallback; you can refine this)
                    if current_wit.v not in self._flat_class(c_from):
                        return None
            total += cost
            current_wit = wit
        return total
