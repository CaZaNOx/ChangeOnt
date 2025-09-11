# tests/test_lift.py
from __future__ import annotations

from agents.co.core.quotient.infimum_lift import LiftedGraph, BaseEdge

def test_witness_consistent_cycle():
    # classes: A={a1,a2}, B={b1}, C={c1}
    part = {"A": ["a1", "a2"], "B": ["b1"], "C": ["c1"]}
    edges = [
        BaseEdge("a1", "b1", 1.0),
        BaseEdge("a2", "b1", 0.5),   # cheaper A->B but via a2
        BaseEdge("b1", "c1", 1.0),
        BaseEdge("c1", "a1", 1.0),
    ]
    lg = LiftedGraph(part, edges)
    # Naive per-edge minima would pick a2->b1 (0.5), b1->c1 (1.0), c1->a1 (1.0) -> but witnesses don't chain (a2->b1 then b1->c1 then c1->a1 -> OK chain only if last returns to a2).
    # Our guard requires chaining (v_i == u_{i+1}); this cycle fails because c1->a1 returns to a1, not a2.
    cost = lg.witness_consistent_cycle_cost(["A", "B", "C"])
    assert cost is None  # guard rejects Frankenstein stitching

    # If we add c1->a2, the chain can close
    edges2 = edges + [BaseEdge("c1", "a2", 1.0)]
    lg2 = LiftedGraph(part, edges2)
    cost2 = lg2.witness_consistent_cycle_cost(["A", "B", "C"])
    assert cost2 is not None
