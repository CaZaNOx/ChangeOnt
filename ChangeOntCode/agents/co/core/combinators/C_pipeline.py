# agents/co/core/combinators/C_pipeline.py
from typing import List, Dict, Any

class Pipeline:
    """
    Simple element pipeline: feeds outputs back into inputs incrementally.
    """
    def __init__(self, elements: List[Any]):
        self.elements = elements

    def run(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        state = dict(inputs)
        for e in self.elements:
            out = e.step(state)
            if out:
                state.update(out)
        return state
