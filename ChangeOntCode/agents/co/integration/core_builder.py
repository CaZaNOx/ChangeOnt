# agents/co/integration/core_builder.py
from __future__ import annotations
from typing import Any, Dict, List
from pathlib import Path

# Core & combinators
from agents.co.core.pipeline import COAgentCore

# Registry loader (already used by suite hooks)
from agents.co.integration.loader import load_registry, resolve_classes

# Default registry & combos locations
DEFAULT_REG_PATH = Path("agents/co/registries/registry.yaml")

# Safe import of pipeline combinator with fallback
try:
    from agents.co.core.combinators.C_pipeline import C_Pipeline
except Exception:
    class C_Pipeline:  # type: ignore
        def __init__(self, order: List[str] | None = None): self.order = order or []
        def run(self, elements, primitives, header, observation, feedback) -> Dict[str, Any]:
            out: Dict[str, Any] = {}
            for e in elements:
                for fn in ("update", "step", "metrics"):
                    if hasattr(e, fn):
                        try:
                            res = getattr(e, fn)(
                                observation, primitives, header, feedback
                            ) if fn in ("update", "step") else getattr(e, fn)()
                            if isinstance(res, dict): out.update(res)
                        except Exception:
                            out[e.__class__.__name__] = "failed"
            return out


# ... (keep your current imports and C_Pipeline fallback)

def _instantiate_components(params: Dict[str, Any], classes: Dict[str, Dict[str, Any]]) -> tuple[Any, Dict[str, Any], List[Any], Dict[str, Any]]:
    # -------- Header (unchanged) --------
    hcfg  = dict(params.get("header", {}))
    htype = str(hcfg.pop("type", hcfg.pop("mode", "SSI")))
    header_cls = classes.get("headers", {}).get(htype)
    if header_cls is None:
        class _Header:
            def __init__(self, mode: str = "SSI", **kwargs: Any) -> None:
                self.mode = str(mode)
                self.state: Dict[str, Any] = {}
            def update(self, observation: Dict[str, Any]) -> Dict[str, Any]:
                fam = observation.get("family")
                t = (observation.get("t", None) if "t" in observation else observation.get("step", None))
                if fam is not None: self.state["family"] = fam
                if t is not None:
                    try: self.state["t"] = int(t)
                    except Exception: pass
                return {"header_mode": self.mode, "t": self.state.get("t", None), "family": fam}
        header = _Header(mode=htype, **hcfg)
    else:
        header = header_cls(**hcfg)

    # -------- Primitives (unchanged) --------
    prim_cfg = dict(params.get("primitives", {}))
    prim_classes = classes.get("primitives", {})
    primitives: Dict[str, Any] = {}
    if prim_cfg:
        for name, cfg in prim_cfg.items():
            cls = prim_classes.get(name)
            if cls is None: continue
            kwargs = dict(cfg) if isinstance(cfg, dict) else {}
            kwargs.pop("enabled", None)
            primitives[name] = cls(**kwargs)
    else:
        for name in ("visit_tracker", "bandit_stats", "ngram_model"):
            cls = prim_classes.get(name)
            if cls:
                primitives[name] = cls()

    # -------- Elements (now with explicit reordering) --------
    el_cfg_map = dict(params.get("elements", {}))   # preserves insertion order from YAML loader
    element_classes = classes.get("elements", {})

    # Enabled names in insertion order
    names = [k for k, v in el_cfg_map.items() if not isinstance(v, dict) or v.get("enabled", True)]

    # Apply explicit order if provided:
    desired = list(params.get("combinator", {}).get("order", []))
    if desired:
        seen = set()
        # keep desired names in the given order if present/enabled
        ordered = [n for n in desired if n in names and not (n in seen or seen.add(n))]
        # append any remaining enabled names not in desired
        ordered.extend([n for n in names if n not in set(ordered)])
        names = ordered

    # Ensure action_head is last
    if "action_head" in names:
        names = [n for n in names if n != "action_head"] + ["action_head"]
    elif "action_head" in el_cfg_map:
        names.append("action_head")

    elements: List[Any] = []
    for name in names:
        cls = element_classes.get(name)
        if cls is None:
            continue
        kwargs = {}
        raw = el_cfg_map.get(name, {})
        if isinstance(raw, dict):
            kwargs = dict(raw); kwargs.pop("enabled", None)

        import inspect
        valid_kwargs = dict(kwargs)
        try:
            sig = inspect.signature(cls.__init__)
            accepted = set(sig.parameters.keys()) - {"self"}
            valid_kwargs = {k: v for k, v in kwargs.items() if k in accepted}
        except Exception:
            valid_kwargs = kwargs

        try:
            inst = cls(**valid_kwargs)
        except TypeError as e:
            raise TypeError(f"Element '{name}' could not be constructed with kwargs={valid_kwargs} (raw={kwargs}): {e}") from e

        elements.append(inst)

    # -------- Combinators (unchanged; we still pass order to pipeline if it supports it) --------
    comb_classes = classes.get("combinators", {})
    pipeline_cls = comb_classes.get("pipeline", C_Pipeline)
    order = list(params.get("combinator", {}).get("order", []))
    pipeline = pipeline_cls(order=order) if "order" in getattr(pipeline_cls.__init__, "__code__", type("x", (), {"co_varnames": ()})) .co_varnames else pipeline_cls()
    combinators: Dict[str, Any] = {"pipeline": pipeline}

    gate_cls = comb_classes.get("gate")
    if gate_cls:
        try:
            combinators["gate"] = gate_cls()
        except Exception:
            pass

    return header, primitives, elements, combinators


def build_co_core(params: Dict[str, Any] | None = None) -> COAgentCore:
    """
    Construct a CO core from params + registry.

    Params shape (examples):
      math_policy: "co" | "classical" | "auto"
      header:      { type: "SSI" }         # or { mode: "SSI" }
      elements:
        haq:        { enabled: true, history_len: 64, ema_alpha: 0.2 }
        ghvc:       { enabled: true, mdl_lambda: 1.0, cooldown: 5, birth_threshold: 2.0 }
        density:    { enabled: true, rounding: 2 }
        change_ops: { enabled: true, k: 4, mdL_select: true }
        # You can also specify: elements: { order: ["vote_bridge","haq","change_ops","action_head"] }
        action_head:{ enabled: true, visit_horizon: 256, c_explore: 1.0, ngram_order: 2 }  # <- last
      primitives:
        visit_tracker: {}
        bandit_stats: {}
        ngram_model: {}
        co_bus: {}             # optional; guaranteed even if omitted
      combinator:
        order: []    # optional explicit element order for the pipeline combinator
      name: "CO_core"
    """
    cfg = dict(params or {})
    math_policy = str(cfg.get("math_policy", "co"))

    # Load registry & resolve classes
    reg = load_registry(DEFAULT_REG_PATH)
    classes = resolve_classes(reg)

    # Build components
    header, primitives, elements, combinators = _instantiate_components(cfg, classes)

    # Return core
    return COAgentCore(
        header=header,
        elements=elements,
        primitives=primitives,
        combinators=combinators,
        math_policy=math_policy,
        name=str(cfg.get("name", "CO_core")),
    )