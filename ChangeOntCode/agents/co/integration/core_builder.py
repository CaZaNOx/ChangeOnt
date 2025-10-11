# agents/co/integration/core_builder.py
from __future__ import annotations
from typing import Any, Dict

def build_co_core(params: Dict[str, Any] | None = None) -> Any:
    """
    Tries to construct your COAgentCore from agents.co.core.pipeline.
    Falls back to a minimal shim that just returns {} on .step(...).
    """
    params = dict(params or {})
    try:
        from agents.co.core.pipeline import COAgentCore  # type: ignore
        # Try a few ctor shapes, in order of richness
        for attempt in (
            lambda: COAgentCore(**params),
            lambda: COAgentCore(params),
            lambda: COAgentCore(),
        ):
            try:
                return attempt()
            except Exception:
                pass
    except Exception:
        pass

    # Last-resort shim that won't crash the runners
    class _ShimCore:
        def step(self, observation: Dict[str, Any] | None = None, feedback: Dict[str, Any] | None = None) -> Dict[str, Any]:
            return {}
    return _ShimCore()