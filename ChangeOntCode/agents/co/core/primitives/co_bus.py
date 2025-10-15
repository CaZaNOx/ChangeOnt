#ChangeOntCode\agents\co\core\primitives\co_bus.py
from __future__ import annotations
from typing import Any, Dict, List, Optional

class CoVoteBus:
    """
    Very small pub/sub bus for CO element 'votes'.
    Elements call push(family, action, weight, ...) each step.
    Aggregators (e.g., ActionHead) drain() the family-specific list once per step.
    """
    def __init__(self) -> None:
        self._store: Dict[str, List[Dict[str, Any]]] = {}

    def push(
        self,
        family: str,
        action: Any,
        weight: float = 1.0,
        scope: Optional[str] = None,
        support: Optional[Any] = None,
        rationale: Optional[str] = None,
        source: Optional[str] = None,
    ) -> None:
        if family not in self._store:
            self._store[family] = []
        self._store[family].append({
            "action": action,
            "weight": float(weight),
            "scope": scope,
            "support": support,
            "rationale": rationale,
            "source": source,
        })

    def drain(self, family: str) -> List[Dict[str, Any]]:
        lst = self._store.get(family, [])
        self._store[family] = []
        return lst

    def peek(self, family: str) -> List[Dict[str, Any]]:
        return list(self._store.get(family, []))

    def size(self, family: str) -> int:
        return len(self._store.get(family, []))