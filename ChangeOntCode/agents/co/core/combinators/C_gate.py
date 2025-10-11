# agents/co/core/combinators/C_gate.py
from typing import Any, Dict

class Gate:
    """
    Conditional execution based on header guards or a callable predicate.
    """
    def __init__(self, predicate, element: Any):
        self.predicate = predicate  # callable(state)->bool OR guard key str
        self.element = element

    def run(self, state: Dict) -> Dict:
        ok = True
        if callable(self.predicate):
            ok = bool(self.predicate(state))
        elif isinstance(self.predicate, str):
            guards = state.get("guards", {})
            ok = not bool(guards.get(self.predicate, False))
        if not ok:
            return state
        out = self.element.step(state)
        if out:
            state.update(out)
        return state
