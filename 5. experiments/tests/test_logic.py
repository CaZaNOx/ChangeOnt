# tests/test_logic.py
from __future__ import annotations

def kleene_neg(x: str) -> str:
    return {"T": "F", "F": "T", "?": "?"}[x]

def kleene_and(a: str, b: str) -> str:
    # strong Kleene
    if a == "F" or b == "F":
        return "F"
    if a == "T" and b == "T":
        return "T"
    return "?"  # otherwise unknown

def kleene_or(a: str, b: str) -> str:
    if a == "T" or b == "T":
        return "T"
    if a == "F" and b == "F":
        return "F"
    return "?"

def test_tables():
    assert kleene_neg("T") == "F" and kleene_neg("F") == "T" and kleene_neg("?") == "?"
    assert kleene_and("T", "T") == "T"
    assert kleene_and("?", "T") == "?"
    assert kleene_and("F", "?") == "F"
    assert kleene_or("F", "F") == "F"
    assert kleene_or("T", "?") == "T"
    assert kleene_or("?", "?") == "?"
