"""Instantiate the canonical CO core from config while preserving fail-closed runtime contracts."""

# agents/co/integration/core_builder.py
from __future__ import annotations
from typing import Any, Dict, List
from pathlib import Path

# Core & combinators
from agents.co.core.pipeline import COAgentCore
from agents.co.placement.meta_prior import MetaHeader
from agents.co.core.combinators import (
    SC_AdditiveBlend,
    SC_MultiplicativeCoupling,
    SC_GatedThreshold,
)

# Registry loader (already used by suite hooks)
from agents.co.integration.loader import load_registry, resolve_classes
from agents.co.core.contracts.placement_contract import build_runtime_contract

# Default registry & combos locations
DEFAULT_REG_PATH = Path("agents/co/registries/registry.yaml")


def _apply_configure(inst: Any, params: Dict[str, Any], context: Dict[str, Any]) -> Any:
    if inst is None:
        return inst
    if hasattr(inst, "configure") and callable(getattr(inst, "configure")):
        try:
            configured = inst.configure(dict(params or {}), dict(context or {}))
            if configured is not None:
                return configured
        except TypeError:
            try:
                configured = inst.configure(dict(params or {}))
                if configured is not None:
                    return configured
            except Exception:
                return inst
        except Exception:
            return inst
    return inst

from agents.co.core.combinators.C_pipeline import C_Pipeline

def _instantiate_components(params: Dict[str, Any], classes: Dict[str, Dict[str, Any]]) -> tuple[Any, Dict[str, Any], List[Any], Dict[str, Any], Any]:
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
    def _init_primitive(cls: Any, params: Dict[str, Any]) -> Any:
        if cls is None:
            return None
        if callable(cls):
            try:
                return cls(**params)
            except Exception:
                try:
                    return cls()
                except Exception:
                    return cls
        return cls

    if prim_cfg:
        for name, cfg in prim_cfg.items():
            cls = prim_classes.get(name)
            if cls is None: continue
            kwargs = dict(cfg) if isinstance(cfg, dict) else {}
            kwargs.pop("enabled", None)
            primitives[name] = _apply_configure(_init_primitive(cls, kwargs), kwargs, {"component": name, "kind": "primitive"})
    else:
        for name in ("visit_tracker", "bandit_stats", "ngram_model"):
            cls = prim_classes.get(name)
            if cls:
                primitives[name] = cls()

    # Ensure canonical primitives exist when classes are available
    if "signal_bus" not in primitives:
        cls = prim_classes.get("signal_bus")
        if cls:
            primitives["signal_bus"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "signal_bus", "kind": "primitive"})
    if "kernel_substrate" not in primitives:
        cls = prim_classes.get("kernel_substrate")
        if cls:
            primitives["kernel_substrate"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "kernel_substrate", "kind": "substrate"})
    if "operative_relevance" not in primitives:
        cls = prim_classes.get("operative_relevance")
        if cls:
            primitives["operative_relevance"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "operative_relevance", "kind": "primitive"})
    if "P1" not in primitives:
        cls = prim_classes.get("P1")
        if cls:
            primitives["P1"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "P1", "kind": "primitive"})
    if "P2" not in primitives:
        cls = prim_classes.get("P2")
        if cls:
            primitives["P2"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "P2", "kind": "primitive"})
    if "P4" not in primitives:
        cls = prim_classes.get("P4")
        if cls:
            primitives["P4"] = _apply_configure(_init_primitive(cls, {"epsilon": 0.2, "window": 5}), {"epsilon": 0.2, "window": 5}, {"component": "P4", "kind": "primitive"})
    if "P16" not in primitives:
        cls = prim_classes.get("P16")
        if cls:
            primitives["P16"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "P16", "kind": "primitive"})
    if "p10" not in primitives:
        cls = prim_classes.get("p10")
        if cls:
            primitives["p10"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "p10", "kind": "primitive"})
    if "p12" not in primitives:
        cls = prim_classes.get("p12")
        if cls:
            primitives["p12"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "p12", "kind": "primitive"})
    if "id_mem" not in primitives:
        cls = prim_classes.get("id_mem")
        if cls:
            primitives["id_mem"] = _apply_configure(_init_primitive(cls, {}), {}, {"component": "id_mem", "kind": "primitive"})
    if "birth_count" not in primitives:
        primitives["birth_count"] = 0

    # Keep exploratory primitives opt-in. Canonical configs should enumerate
    # only what they actually mean to use rather than silently widening the
    # kernel.
    # NOTE: P9 (VariableBirth) remains optional and should only be enabled explicitly.

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

    # Ensure commitment_surface is last
    if "commitment_surface" in names:
        names = [n for n in names if n != "commitment_surface"] + ["commitment_surface"]
    elif "commitment_surface" in el_cfg_map:
        names.append("commitment_surface")

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

        inst = _apply_configure(inst, kwargs, {"component": name, "kind": "element"})
        elements.append(inst)

    # -------- Combinators (runtime + semantic) --------
    comb_classes = classes.get("combinators", {})
    pipeline_cls = comb_classes.get("pipeline", C_Pipeline)
    order = list(params.get("combinator", {}).get("order", []))
    pipeline = pipeline_cls(order=order) if "order" in getattr(pipeline_cls.__init__, "__code__", type("x", (), {"co_varnames": ()})) .co_varnames else pipeline_cls()
    # Semantic combinators (law-forms)
    semantic = {
        "SC_AdditiveBlend": SC_AdditiveBlend,
        "SC_MultiplicativeCoupling": SC_MultiplicativeCoupling,
        "SC_GatedThreshold": SC_GatedThreshold,
    }
    # Optional semantic combinator remapping for experiment doctrine
    overrides = params.get("semantic_overrides", params.get("semantic_combinators", {})) or {}
    if isinstance(overrides, dict):
        for name, target in overrides.items():
            if name in semantic and target in semantic:
                semantic[name] = semantic[target]
    # expose to elements without conflating primitives
    primitives["_semantic"] = semantic

    combinators: Dict[str, Any] = {"pipeline": pipeline, "semantic": semantic}

    return header, primitives, elements, combinators, semantic


def _build_meta_header(params: Dict[str, Any]) -> MetaHeader:
    meta_cfg = params.get("meta_header", params.get("meta", {})) or {}
    if not isinstance(meta_cfg, dict):
        meta_cfg = {}
    priors = dict(meta_cfg.get("priors", meta_cfg))
    family = meta_cfg.get("family")
    return MetaHeader(priors=priors, family=family)




def _normalize_combo(cfg: Dict[str, Any]) -> Dict[str, Any]:
    """Translate the canonical combo YAML shape into build_co_core params.

    Supported canonical YAML keys:
      - header: {type, params}
      - elements: list[{class,key,params}]
      - primitives: mapping{name: {class, params}}
      - combinators: {pipeline:{params}, ...}
    """
    out: Dict[str, Any] = {}
    if not isinstance(cfg, dict):
        return out
    if 'math_policy' in cfg:
        out['math_policy'] = cfg.get('math_policy')
    if 'name' in cfg:
        out['name'] = cfg.get('name')
    h = cfg.get('header', {}) or {}
    if isinstance(h, dict):
        hp = dict(h.get('params', {}) or {})
        htype = h.get('type', h.get('mode'))
        if htype is not None:
            hp['type'] = htype
        out['header'] = hp
    elems = cfg.get('elements', []) or []
    if isinstance(elems, list):
        emap: Dict[str, Any] = {}
        order: List[str] = []
        alias = {
            'A':'haq','B':'ghvc','C':'EC_Identity','D':'ED_GaugeWarp','E':'EE_Compressibility',
            'F':'EF_Router','G':'density','H':'EH_BreadthDepth','I':'change_ops',
            'HEAD':'commitment_surface','candidate_surface':'candidate_surface','candidate_surface':'candidate_surface','commitment_surface':'commitment_surface'
        }
        for item in elems:
            if not isinstance(item, dict):
                continue
            key = str(item.get('key') or item.get('name') or '').strip()
            norm = alias.get(key, key)
            if not norm:
                cls = str(item.get('class') or '')
                tail = cls.split(':')[0].split('.')[-1]
                norm = alias.get(tail, tail)
            params = dict(item.get('params', {}) or {})
            params.setdefault('enabled', True)
            emap[norm] = params
            order.append(norm)
        out['elements'] = emap
        out.setdefault('combinator', {})['order'] = order
    prims = cfg.get('primitives', {}) or {}
    if isinstance(prims, dict):
        pmap: Dict[str, Any] = {}
        for name, item in prims.items():
            if isinstance(item, dict):
                pmap[name] = dict(item.get('params', {}) or {})
            else:
                pmap[name] = {}
        out['primitives'] = pmap
    comb = cfg.get('combinators', {}) or {}
    if isinstance(comb, dict):
        c = out.setdefault('combinator', {})
        pipe = comb.get('pipeline', {}) or {}
        if isinstance(pipe, dict):
            params = pipe.get('params', {}) or {}
            if isinstance(params, dict) and 'order' in params:
                c['order'] = list(params.get('order', []) or [])
    return out

def build_co_core(params: Dict[str, Any] | None = None) -> COAgentCore:
    """
    Construct a CO core from params + registry.

    Params shape (examples):
      math_policy: "co"
      header:      { type: "SSI" }         # or { mode: "SSI" }
      elements:
        haq:        { enabled: true, history_len: 64, ema_alpha: 0.2 }
        ghvc:       { enabled: true, mdl_lambda: 1.0, cooldown: 5, birth_threshold: 2.0 }
        density:    { enabled: true, rounding: 2 }
        change_ops: { enabled: true, k: 4, mdL_select: true }
        # Optional canonical order still keeps CommitmentSurface final.
        commitment_surface:{ enabled: true }  # readout surface; pipeline enforces final execution
      primitives:
        visit_tracker: {}
        bandit_stats: {}
        ngram_model: {}
        signal_bus: {}             # optional; guaranteed even if omitted
      combinator:
        order: []    # optional explicit element order for the pipeline combinator
      name: "CO_core"
    """
    cfg = dict(params or {})
    combo_path = cfg.get("combo_path") or cfg.get("combo")
    if combo_path:
        cp = Path(str(combo_path))
        if cp.exists():
            import yaml  # type: ignore
            raw = yaml.safe_load(cp.read_text(encoding="utf-8")) or {}
            cfg = {**_normalize_combo(raw), **{k: v for k, v in cfg.items() if k not in {"combo_path", "combo"}}}
    math_policy = str(cfg.get("math_policy", "co"))
    runtime_contract = build_runtime_contract(cfg)

    # Load registry & resolve classes
    reg = load_registry(DEFAULT_REG_PATH)
    classes = resolve_classes(reg)

    # Build components
    header, primitives, elements, combinators, semantic = _instantiate_components(cfg, classes)

    # Return core
    core = COAgentCore(
        header=header,
        elements=elements,
        primitives=primitives,
        combinators=combinators,
        math_policy=math_policy,
        name=str(cfg.get("name", "CO_core")),
        meta_header=_build_meta_header(cfg),
        runtime_contract=runtime_contract,
    )
    # expose meta header for telemetry without conflating with internal header
    primitives["_meta_header"] = core.meta_header
    primitives["_runtime_contract"] = core.export_runtime_contract()
    return core
