from __future__ import annotations
from typing import Any, Dict, List, Optional


class KernelSignalBus:
    """Generic signal and candidate-evidence bus keyed by decision scope.

    Canonical rules:
    - keyed by caller-provided scope, not benchmark family
    - stores typed candidate-evidence publications and scalar signals
    - shared runtime surfaces may depend on this bus; environment families may not
      extend its schema ad hoc
    """
    def __init__(self) -> None:
        self._store: Dict[str, List[Dict[str, Any]]] = {}
        self._signals: Dict[str, float] = {}

    def _key(self, scope_key: Optional[str] = None) -> str:
        return str(scope_key or "default")

    def publish(self, *, scope_key: Optional[str] = None, action: Any = None, weight: float = 1.0, channel: Optional[str] = None, support: Optional[Any] = None, rationale: Optional[str] = None, source: Optional[str] = None) -> None:
        key = self._key(scope_key=scope_key)
        self._store.setdefault(key, []).append({
            "action": action,
            "weight": float(weight),
            "scope": channel,
            "support": support,
            "rationale": rationale,
            "source": source,
        })

    def drain(self, *, scope_key: Optional[str] = None) -> List[Dict[str, Any]]:
        key = self._key(scope_key=scope_key)
        lst = self._store.get(key, [])
        self._store[key] = []
        return lst

    def peek(self, *, scope_key: Optional[str] = None) -> List[Dict[str, Any]]:
        return list(self._store.get(self._key(scope_key=scope_key), []))

    def size(self, *, scope_key: Optional[str] = None) -> int:
        return len(self._store.get(self._key(scope_key=scope_key), []))

    def set(self, key: str, value: float) -> None:
        self._signals[str(key)] = float(value)

    def get(self, key: str, default: Optional[float] = None) -> Optional[float]:
        return self._signals.get(str(key), default)

    def signals(self) -> Dict[str, float]:
        return dict(self._signals)

    def __setitem__(self, key: str, value: float) -> None:
        self.set(key, value)

    def __getitem__(self, key: str) -> float:
        return self._signals[str(key)]
