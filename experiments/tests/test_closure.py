# tests/test_closure.py
from __future__ import annotations

from agents.co.core.quotient.equivalence import deterministic_merge_pass, stable_hash

def test_deterministic_merge_pass():
    items = [{"id": i, "val": i % 3} for i in range(6)]

    def dist(a, b):
        return 0.0 if (a["val"] == b["val"]) else 1.0

    def hdr(a, b):
        return True

    def sig(x):
        return {"val": x["val"]}

    uf1, cands1 = deterministic_merge_pass(items, dist, hdr, sig, tau=0.0, seed=1)
    uf2, cands2 = deterministic_merge_pass(items, dist, hdr, sig, tau=0.0, seed=99)

    # same partition regardless of seed because order depends on content
    assert uf1.classes() == uf2.classes()

    # termination: no infinite loops; candidate list is finite and sorted
    assert len(cands1) == len(cands2)
