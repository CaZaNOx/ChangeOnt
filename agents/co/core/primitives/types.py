# agents/co/core/primitives/types.py
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, List, Optional, Union, Tuple

Number = Union[int, float]

@dataclass
class Sequence:
    """A generic numeric sequence used by several primitives."""
    values: List[Number]

@dataclass
class NominalLoop:
    """A discovered loop: period L, representative code, and a confidence score."""
    period: int
    code: List[int]
    confidence: float = 1.0

@dataclass
class QuotientMapping:
    """
    Maps raw observations to quotient labels (e.g., partition classes).
    `classes[i]` is the class label assigned to observation i.
    """
    classes: List[int]

@dataclass
class LiftedSequence:
    """Sequence lifted to a quotient space via a mapping."""
    values: List[int]
    mapping: QuotientMapping

def identity_similarity(a: Union[Number, Iterable[Number]],
                        b: Union[Number, Iterable[Number]]) -> float:
    """
    A simple similarity measure in [0, 1] where 1.0 means identical.
    - Scalars: 1 / (1 + (a-b)^2)
    - Vectors: 1 / (1 + sum_i (a_i - b_i)^2)
    """
    def as_tuple(x: Union[Number, Iterable[Number]]) -> Tuple[float, ...]:
        if isinstance(x, (int, float)):
            return (float(x),)
        return tuple(float(v) for v in x)

    va, vb = as_tuple(a), as_tuple(b)
    if len(va) != len(vb):
        # If shapes mismatch, define similarity as 0.
        return 0.0
    sqdist = sum((xa - xb) ** 2 for xa, xb in zip(va, vb))
    return 1.0 / (1.0 + sqdist)
