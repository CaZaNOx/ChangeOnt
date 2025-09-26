# PATH: agents/co/__init__.py
"""
CO package init.

- Keeps backward compatibility: `from agents.co import HAQCfg, HAQAgent`.
- Avoids eager imports that can fail if other CO submodules have issues.
- Lazily loads symbols on first access via module __getattr__ (PEP 562).
"""

__all__ = ["HAQCfg", "HAQAgent"]

def __getattr__(name: str):
    # Only expose the two public symbols you already export.
    if name in ("HAQCfg", "HAQAgent"):
        from importlib import import_module
        m = import_module("agents.co.agent_haq")
        return getattr(m, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
# PATH: agents/co/__init__.py
"""
CO package init.

- Keeps backward compatibility: `from agents.co import HAQCfg, HAQAgent`.
- Avoids eager imports that can fail if other CO submodules have issues.
- Lazily loads symbols on first access via module __getattr__ (PEP 562).
"""

__all__ = ["HAQCfg", "HAQAgent"]

def __getattr__(name: str):
    # Only expose the two public symbols you already export.
    if name in ("HAQCfg", "HAQAgent"):
        from importlib import import_module
        m = import_module("agents.co.agent_haq")
        return getattr(m, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
