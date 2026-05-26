from __future__ import annotations

"""Bridge-signal trace across active problem families.

Diagnostic purpose only.  This study traces whether generic CO signals survive
across the bridge:

    public observation / problem contract
    -> shape_prior6 / direct controls
    -> raw adapter candidates
    -> CandidateSurface rows
    -> CommitmentSurface assessment
    -> action

It does not patch runtime behavior and does not use family/action-specific logic
inside the kernel.  The family-specific code here is only to instantiate public
environments for audit episodes.
"""

import json
import math
import os
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import importlib

from agents.co.core.pipeline import COAgentCore
from agents.co.headers.H_SSI import HeaderSSI
from agents.co.core.combinators.C_pipeline import C_Pipeline
from agents.co.core.combinators import SC_AdditiveBlend, SC_MultiplicativeCoupling, SC_GatedThreshold, SC_WeightedSelection
from agents.co.runtime.support.signal_bus import KernelSignalBus
from agents.co.runtime.support.bandit_stats import BanditStats
from agents.co.runtime.support.ngram_model import NGramModel
from agents.co.core.primitives.kernel_substrate import KernelSubstrate as BoundedLocalUnfoldingSubstrate
from agents.co.core.primitives.operative_relevance import OperativeRelevanceController
from agents.co.core.primitives.P4_reid_kernel import ReIDKernel
from agents.co.core.primitives.identity import TraceMemory
from agents.co.core.primitives.P10_change_ops_core import ChangeOpsCore
from agents.co.core.primitives.P12_closure_quotient import ClosureQuotient
from agents.co.core.primitives.P16_remaining_burden import RemainingTransformationBurden
from agents.co.core.elements.EA_haq import EA_HAQ
from agents.co.core.elements.EC_identity import EC_Identity
from agents.co.core.elements.EG_density_precision import EG_Density
from agents.co.core.elements.EI_change_operators import EI_ChangeOps
from agents.co.runtime.surfaces.candidate_surface import CandidateEvidenceSurface
from agents.co.runtime.surfaces.commitment_surface import CommitmentSurface
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement

from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from environments.maze1.env import GridMazeEnv, MazeSpec
from environments.latent_mechanism.env import LatentMechanismDoorWorld, MechanismSpec
from environments.maintenance_replacement.env import MaintenanceReplacementEnv, MaintenanceSpec, ACTIONS as MAINT_ACTIONS

OUT = Path("outputs/bridge_signal_trace_v1.json")
DEFAULT_SEEDS = (0, 1, 2)
TRACE_HORIZON = 32


def spec_from_name(name: str, seed: int) -> MaintenanceSpec:
    key = str(name or "middle").lower()
    if key in {"bandit_like", "maintenance_bandit_like", "bandit"}:
        return MaintenanceSpec.bandit_like(seed=int(seed))
    if key in {"renewal_like", "maintenance_renewal_like", "renewal"}:
        return MaintenanceSpec.renewal_like(seed=int(seed))
    return MaintenanceSpec.middle(seed=int(seed))


def _canonical_params() -> Dict[str, Any]:
    return {
        "header": {"mode": "SSI"},
        "elements": {
            "haq": {"enabled": True},
            "EC_Identity": {"enabled": True},
            "density": {"enabled": True},
            "change_ops": {"enabled": True},
            "candidate_surface": {"enabled": True},
            "commitment_surface": {"enabled": True},
        },
        "primitives": {
            "signal_bus": {},
            "kernel_substrate": {},
            "operative_relevance": {},
            "bandit_stats": {},
            "ngram_model": {},
        },
        "combinator": {"order": ["haq", "EC_Identity", "density", "change_ops", "candidate_surface", "commitment_surface"]},
    }


def _configure(inst: Any, params: Mapping[str, Any], component: str, kind: str) -> Any:
    if hasattr(inst, "configure"):
        try:
            configured = inst.configure(dict(params or {}), {"component": component, "kind": kind})
            return configured if configured is not None else inst
        except TypeError:
            try:
                configured = inst.configure(dict(params or {}))
                return configured if configured is not None else inst
            except Exception:
                return inst
        except Exception:
            return inst
    return inst


def _core() -> Any:
    # Manual canonical core builder for this study.  It avoids the PyYAML-backed
    # registry loader so the diagnostic remains runnable in minimal shells.  The
    # component set mirrors CO_canonical_core.
    p2 = importlib.import_module("agents.co.core.primitives.P2_gauge")
    p1 = importlib.import_module("agents.co.core.primitives.P1_bend_metric")
    primitives: Dict[str, Any] = {
        "signal_bus": KernelSignalBus(),
        "kernel_substrate": BoundedLocalUnfoldingSubstrate(),
        "operative_relevance": OperativeRelevanceController(),
        "bandit_stats": BanditStats(),
        "ngram_model": NGramModel(),
        "P1": p1,
        "P2": p2,
        "P4": ReIDKernel(epsilon=0.2, window=5),
        "P16": RemainingTransformationBurden(),
        "p10": ChangeOpsCore(),
        "p12": ClosureQuotient(),
        "id_mem": TraceMemory(),
        "birth_count": 0,
    }
    primitives["_semantic"] = {
        "SC_AdditiveBlend": SC_AdditiveBlend,
        "SC_MultiplicativeCoupling": SC_MultiplicativeCoupling,
        "SC_GatedThreshold": SC_GatedThreshold,
        "SC_WeightedSelection": SC_WeightedSelection,
    }
    header = HeaderSSI(family="audit")
    elements = [
        _configure(EA_HAQ(), {}, "haq", "element"),
        _configure(EC_Identity(), {}, "EC_Identity", "element"),
        _configure(EG_Density(), {}, "density", "element"),
        _configure(EI_ChangeOps(), {}, "change_ops", "element"),
        CandidateEvidenceSurface(),
        CommitmentSurface(),
    ]
    combinators = {"pipeline": C_Pipeline(order=["haq", "EC_Identity", "density", "change_ops", "candidate_surface", "commitment_surface"]), "semantic": primitives["_semantic"]}
    core = COAgentCore(header=header, elements=elements, primitives=primitives, combinators=combinators, math_policy="co", name="CO_core_bridge_trace")
    primitives["_runtime_contract"] = core.export_runtime_contract()
    return core


def _f(x: Any, default: Optional[float] = None) -> Optional[float]:
    try:
        if x is None:
            return default
        v = float(x)
        if math.isnan(v) or math.isinf(v):
            return default
        return v
    except Exception:
        return default


def _clamp01(x: Any, default: float = 0.0) -> float:
    v = _f(x, default)
    if v is None:
        v = default
    if v < 0.0:
        return 0.0
    if v > 1.0:
        return 1.0
    return float(v)


def _safe_mean(xs: Iterable[Any]) -> Optional[float]:
    vals = [_f(x) for x in xs]
    vals = [v for v in vals if v is not None]
    return float(mean(vals)) if vals else None


def _safe_action(sel: Any, default: Any) -> Any:
    if isinstance(sel, dict):
        return sel.get("action", default)
    return default if sel is None else sel


def _packet(agent: Any) -> Dict[str, Any]:
    p = getattr(agent, "_last_obs", {})
    return dict(p or {}) if isinstance(p, Mapping) else {}


def _prims(agent: Any) -> Dict[str, Any]:
    core = getattr(agent, "core", None)
    p = getattr(core, "primitives", {})
    return dict(p or {}) if isinstance(p, Mapping) else {}


def _shape_axes(packet: Mapping[str, Any]) -> Dict[str, float]:
    sp = packet.get("shape_prior6") or {}
    axes = sp.get("axes", {}) if isinstance(sp, Mapping) else {}
    return {str(k): _clamp01(v, 0.5) for k, v in dict(axes or {}).items()}


def _row_by_action(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Mapping[str, Any]]:
    return {str(r.get("action")): r for r in rows if r.get("action") is not None}


def _assessment_by_action(sel: Mapping[str, Any]) -> Dict[str, Mapping[str, Any]]:
    raw = sel.get("canonical_commitment_assessment", {}) if isinstance(sel, Mapping) else {}
    return {str(k): v for k, v in dict(raw or {}).items() if isinstance(v, Mapping)}


def _best_by(items: Mapping[str, Mapping[str, Any]], field: str, high: bool = True) -> Dict[str, Any]:
    best_a: Optional[str] = None
    best_v: Optional[float] = None
    for a, rec in items.items():
        v = _f(rec.get(field))
        if v is None:
            continue
        if best_v is None or (v > best_v if high else v < best_v):
            best_a, best_v = a, v
    return {"action": best_a, "value": best_v}


def _rank_of(action: Any, items: Mapping[str, Mapping[str, Any]], field: str, high: bool = True) -> Optional[int]:
    vals: List[Tuple[str, float]] = []
    for a, rec in items.items():
        v = _f(rec.get(field))
        if v is not None:
            vals.append((a, v))
    vals.sort(key=lambda x: x[1], reverse=high)
    target = str(action)
    for i, (a, _) in enumerate(vals, start=1):
        if a == target:
            return i
    return None


def _raw_candidate_features(candidates: Sequence[Mapping[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, Mapping[str, Any]]]:
    rows: List[Dict[str, Any]] = []
    for c in candidates:
        action = c.get("candidate_id", c.get("action"))
        if action is None:
            continue
        visible = _clamp01(c.get("visible_delta", 0.5), 0.5)
        uncertainty = _clamp01(c.get("uncertainty_hint", 0.0), 0.0)
        contradiction = _clamp01(c.get("contradiction_hint", 0.0), 0.0)
        obstruction = _clamp01(c.get("obstruction_hint", 0.0), 0.0)
        reversibility = _clamp01(c.get("reversibility_hint", 1.0), 1.0)
        coverage = _clamp01(c.get("coverage_adequacy", 0.0), 0.0)
        tested = _clamp01(c.get("tested_hint", coverage), coverage)
        raw_burden = _clamp01(0.42 * contradiction + 0.22 * obstruction + 0.18 * (1.0 - reversibility) + 0.10 * (1.0 - coverage) + 0.08 * uncertainty)
        rows.append({
            "action": str(action),
            "legal": bool(c.get("legal", True)),
            "visible_delta": visible,
            "uncertainty_hint": uncertainty,
            "contradiction_hint": contradiction,
            "obstruction_hint": obstruction,
            "reversibility_hint": reversibility,
            "coverage_adequacy": coverage,
            "tested_hint": tested,
            "raw_burden_proxy": raw_burden,
        })
    return rows, _row_by_action(rows)


def _trace_bridge_step(family: str, case: str, seed: int, t: int, obs: Mapping[str, Any], agent: Any, sel: Mapping[str, Any], action: Any, reward: Optional[float] = None, done: Optional[bool] = None, env_audit: Optional[Mapping[str, Any]] = None) -> Dict[str, Any]:
    packet = _packet(agent)
    prims = _prims(agent)
    raw_candidates = [dict(c) for c in packet.get("candidates", []) if isinstance(c, Mapping)]
    raw_rows, raw_map = _raw_candidate_features(raw_candidates)
    pub_rows = [dict(r) for r in prims.get("__candidate_publication_rows__", []) if isinstance(r, Mapping)]
    pub_map = _row_by_action(pub_rows)
    ass = _assessment_by_action(sel)
    final_scores = {str(k): _f(v, 0.0) for k, v in dict(sel.get("candidate_final_scores", {}) or {}).items()} if isinstance(sel, Mapping) else {}

    chosen = str(action)
    direct_controls = {str(k): _clamp01(v, 0.5) for k, v in dict(sel.get("direct_controls_used", {}) or {}).items()} if isinstance(sel, Mapping) else {}
    shape_axes = _shape_axes(packet)
    problem_contract = packet.get("problem_contract", {}) if isinstance(packet.get("problem_contract", {}), Mapping) else {}

    # Stage winners and ranks are the loss-map core: where did chosen action
    # become dominant, and did burden/preventive signals ever disagree with local cue?
    stage = {
        "raw_top_visible": _best_by(raw_map, "visible_delta"),
        "raw_top_burden": _best_by(raw_map, "raw_burden_proxy"),
        "published_top_local_support": _best_by(pub_map, "local_support"),
        "published_top_burden_pressure": _best_by(pub_map, "burden_pressure"),
        "published_top_burden_relief": _best_by(pub_map, "burden_relief"),
        "published_top_preventive_support": _best_by(pub_map, "preventive_support"),
        "published_top_sampling_demand": _best_by(pub_map, "sampling_demand"),
        "published_top_decision_state": _best_by(pub_map, "decision_state"),
        "commitment_top_dominance": _best_by(ass, "dominance_score"),
        "commitment_top_continuation": _best_by(ass, "continuation_score"),
        "commitment_top_sampling": _best_by(ass, "sampling_score"),
        "final_score_top": {"action": max(final_scores, key=final_scores.get) if final_scores else None, "value": max(final_scores.values()) if final_scores else None},
    }

    chosen_trace = {
        "raw_visible_rank": _rank_of(chosen, raw_map, "visible_delta"),
        "raw_burden_rank": _rank_of(chosen, raw_map, "raw_burden_proxy"),
        "published_local_rank": _rank_of(chosen, pub_map, "local_support"),
        "published_burden_rank": _rank_of(chosen, pub_map, "burden_pressure"),
        "published_preventive_rank": _rank_of(chosen, pub_map, "preventive_support"),
        "published_decision_rank": _rank_of(chosen, pub_map, "decision_state"),
        "commitment_dominance_rank": _rank_of(chosen, ass, "dominance_score"),
        "commitment_sampling_rank": _rank_of(chosen, ass, "sampling_score"),
    }

    # Small snapshots keep output readable while preserving enough for diagnosis.
    chosen_pub = dict(pub_map.get(chosen, {}) or {})
    chosen_ass = dict(ass.get(chosen, {}) or {})
    top_pub_actions = sorted(pub_rows, key=lambda r: _f(r.get("decision_state"), 0.0) or 0.0, reverse=True)[:4]

    return {
        "family": family,
        "case": case,
        "seed": int(seed),
        "t": int(t),
        "action": chosen,
        "reward": reward,
        "done": done,
        "env_audit": dict(env_audit or {}),
        "problem_contract": dict(problem_contract or {}),
        "shape_axes": shape_axes,
        "direct_controls_used": direct_controls,
        "raw_candidate_count": len(raw_rows),
        "published_candidate_count": len(pub_rows),
        "raw_candidate_stage_summary": {
            "mean_visible_delta": _safe_mean(r.get("visible_delta") for r in raw_rows),
            "mean_raw_burden_proxy": _safe_mean(r.get("raw_burden_proxy") for r in raw_rows),
            "mean_uncertainty_hint": _safe_mean(r.get("uncertainty_hint") for r in raw_rows),
            "mean_contradiction_hint": _safe_mean(r.get("contradiction_hint") for r in raw_rows),
            "max_raw_burden_proxy": max([r.get("raw_burden_proxy", 0.0) for r in raw_rows], default=0.0),
        },
        "published_stage_summary": {
            "mean_local_support": _safe_mean(r.get("local_support") for r in pub_rows),
            "mean_burden_pressure": _safe_mean(r.get("burden_pressure") for r in pub_rows),
            "mean_preventive_support": _safe_mean(r.get("preventive_support") for r in pub_rows),
            "mean_sampling_demand": _safe_mean(r.get("sampling_demand") for r in pub_rows),
            "mean_decision_state": _safe_mean(r.get("decision_state") for r in pub_rows),
            "max_burden_pressure": max([_f(r.get("burden_pressure"), 0.0) or 0.0 for r in pub_rows], default=0.0),
            "max_preventive_support": max([_f(r.get("preventive_support"), 0.0) or 0.0 for r in pub_rows], default=0.0),
        },
        "stage_winners": stage,
        "chosen_rank_trace": chosen_trace,
        "chosen_publication_snapshot": {k: chosen_pub.get(k) for k in (
            "local_support", "burden_pressure", "burden_relief", "preventive_support", "stability_under_change", "sampling_demand", "commitment_stability", "fracture_state", "decision_state"
        )},
        "chosen_commitment_snapshot": {k: chosen_ass.get(k) for k in (
            "local_support", "burden", "uncertainty", "sampling_score", "continuation_score", "dominance_score"
        )},
        "canonical_commitment_mode": str(sel.get("canonical_commitment_mode", "")) if isinstance(sel, Mapping) else "",
        "canonical_commitment_reason": str(sel.get("canonical_commitment_reason", "")) if isinstance(sel, Mapping) else "",
        "dominance_margin": _f(sel.get("dominance_margin")) if isinstance(sel, Mapping) else None,
        "unresolved_pressure": _f(sel.get("unresolved_pressure")) if isinstance(sel, Mapping) else None,
        "top_published_rows_by_decision": top_pub_actions,
    }


def _summarize_rows(rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    n = float(len(rows) or 1)
    action_counts = Counter(str(r.get("action")) for r in rows)
    mode_counts = Counter(str(r.get("canonical_commitment_mode")) for r in rows)
    chosen_local_rank1 = sum(1 for r in rows if (r.get("chosen_rank_trace") or {}).get("published_local_rank") == 1)
    chosen_decision_rank1 = sum(1 for r in rows if (r.get("chosen_rank_trace") or {}).get("published_decision_rank") == 1)
    chosen_dominance_rank1 = sum(1 for r in rows if (r.get("chosen_rank_trace") or {}).get("commitment_dominance_rank") == 1)
    chosen_preventive_rank1 = sum(1 for r in rows if (r.get("chosen_rank_trace") or {}).get("published_preventive_rank") == 1)

    disagreements = []
    for r in rows:
        sw = r.get("stage_winners") or {}
        local = ((sw.get("published_top_local_support") or {}).get("action"))
        preventive = ((sw.get("published_top_preventive_support") or {}).get("action"))
        decision = ((sw.get("published_top_decision_state") or {}).get("action"))
        chosen = r.get("action")
        if local is not None and preventive is not None and local != preventive:
            disagreements.append("local_vs_preventive")
        if local is not None and decision is not None and local != decision:
            disagreements.append("local_vs_decision")
        if preventive is not None and chosen is not None and preventive == chosen:
            disagreements.append("chosen_preventive")
    disagree_counts = Counter(disagreements)

    return {
        "n_steps": len(rows),
        "action_rates": {k: float(v) / n for k, v in sorted(action_counts.items())},
        "commitment_modes": {k: int(v) for k, v in sorted(mode_counts.items())},
        "chosen_rank1_rates": {
            "published_local_support": chosen_local_rank1 / n,
            "published_decision_state": chosen_decision_rank1 / n,
            "commitment_dominance_score": chosen_dominance_rank1 / n,
            "published_preventive_support": chosen_preventive_rank1 / n,
        },
        "stage_disagreement_counts": {k: int(v) for k, v in sorted(disagree_counts.items())},
        "mean_shape_axes": {k: _safe_mean((r.get("shape_axes") or {}).get(k) for r in rows) for k in sorted({kk for r in rows for kk in (r.get("shape_axes") or {}).keys()})},
        "mean_direct_controls": {k: _safe_mean((r.get("direct_controls_used") or {}).get(k) for r in rows) for k in sorted({kk for r in rows for kk in (r.get("direct_controls_used") or {}).keys()})},
        "mean_raw_burden_proxy": _safe_mean((r.get("raw_candidate_stage_summary") or {}).get("mean_raw_burden_proxy") for r in rows),
        "mean_published_burden_pressure": _safe_mean((r.get("published_stage_summary") or {}).get("mean_burden_pressure") for r in rows),
        "mean_published_preventive_support": _safe_mean((r.get("published_stage_summary") or {}).get("mean_preventive_support") for r in rows),
        "mean_published_sampling_demand": _safe_mean((r.get("published_stage_summary") or {}).get("mean_sampling_demand") for r in rows),
        "mean_chosen_decision_state": _safe_mean((r.get("chosen_publication_snapshot") or {}).get("decision_state") for r in rows),
        "mean_chosen_burden_pressure": _safe_mean((r.get("chosen_publication_snapshot") or {}).get("burden_pressure") for r in rows),
        "mean_chosen_preventive_support": _safe_mean((r.get("chosen_publication_snapshot") or {}).get("preventive_support") for r in rows),
    }


def trace_bandit(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    case = "bernoulli_gap_small"
    rows: List[Dict[str, Any]] = []
    for seed in seeds:
        env = BernoulliBanditEnv([0.46, 0.50, 0.54], horizon=TRACE_HORIZON)
        env.reset(seed=int(seed))
        agent = COAdapterBandit(core=_core(), n_arms=3)
        for t in range(TRACE_HORIZON):
            obs = {"family": "bandit", "t": t, "n_arms": 3}
            sel = dict(agent.select(obs) or {})
            a = int(_safe_action(sel, 0))
            if a < 0 or a >= 3:
                a = 0
            _, r, done, info = env.step(a)
            rows.append(_trace_bridge_step("bandit", case, int(seed), t, obs, agent, sel, a, float(r), bool(done), {"arm_means": [0.46, 0.50, 0.54]}))
            agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
            if done:
                break
    return {"status": "executed", "cases": {case: {"summary": _summarize_rows(rows), "rows": rows}}}


def trace_renewal(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    case = "codebook_moderate_renewal"
    rows: List[Dict[str, Any]] = []
    for seed in seeds:
        cfg = EnvCfg(A=4, L_win=4, p_ren=0.08, p_noise=0.02, T_max=TRACE_HORIZON)
        env = CodebookRenewalEnvW(cfg, seed=int(seed))
        obs_val, _, done, info = env.reset()
        agent = COAdapterRenewal(core=_core())
        t = 0
        while not done and t < TRACE_HORIZON:
            obs = {"family": "renewal", "t": t, "obs": int(obs_val), "x": int(obs_val), "A": cfg.A, "action_space": list(range(cfg.A))}
            sel = dict(agent.select(obs) or {})
            a = int(_safe_action(sel, 0))
            if a < 0 or a >= cfg.A:
                a = 0
            nxt, r, done, info = env.step(a)
            rows.append(_trace_bridge_step("renewal", case, int(seed), t, obs, agent, sel, a, float(r), bool(done), {"p_ren": cfg.p_ren, "p_noise": cfg.p_noise}))
            agent.update({"action": a, "reward": float(r), "done": bool(done), "observation": int(nxt), "info": dict(info)})
            obs_val = nxt
            t += 1
    return {"status": "executed", "cases": {case: {"summary": _summarize_rows(rows), "rows": rows}}}


def trace_maze(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for case, partial in [("static_visible", False), ("static_partial", True)]:
        rows: List[Dict[str, Any]] = []
        for seed in seeds:
            spec = MazeSpec(width=7, height=7, seed=int(seed), partial_observability=bool(partial))
            env = GridMazeEnv(spec=spec)
            agent = COAdapterMaze(core=_core())
            for t in range(TRACE_HORIZON):
                obs = env.get_observation()
                obs["t"] = t
                sel = dict(agent.select(obs) or {})
                a = str(_safe_action(sel, "RIGHT"))
                if a not in ("UP", "DOWN", "LEFT", "RIGHT"):
                    a = "RIGHT"
                _, r, done, info = env.step(a)
                rows.append(_trace_bridge_step("maze", case, int(seed), t, obs, agent, sel, a, float(r), bool(done), {"partial_observability": bool(partial)}))
                agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
                if done or tuple(env.pos) == tuple(env.goal):
                    break
        out[case] = {"summary": _summarize_rows(rows), "rows": rows}
    return {"status": "executed", "cases": out}


def trace_latent(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    makers = {"easy_visible": MechanismSpec.easy_visible}
    for case, maker in makers.items():
        rows: List[Dict[str, Any]] = []
        for seed in seeds:
            spec = maker(seed=int(seed))
            env = LatentMechanismDoorWorld(spec)
            obs, _, done, info = env.reset(seed=int(seed))
            agent = COAdapterLatentMechanism(core=_core())
            for t in range(min(TRACE_HORIZON, int(spec.max_steps))):
                obs["t"] = t
                sel = dict(agent.select(obs) or {})
                a = str(_safe_action(sel, "RIGHT"))
                if a not in ("UP", "DOWN", "LEFT", "RIGHT", "INTERACT"):
                    a = "RIGHT"
                next_obs, r, done, info = env.step(a)
                rows.append(_trace_bridge_step("latent_mechanism", case, int(seed), t, obs, agent, sel, a, float(r), bool(done), {"max_steps": int(spec.max_steps)}))
                agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
                obs = next_obs
                if done:
                    break
        out[case] = {"summary": _summarize_rows(rows), "rows": rows}
    return {"status": "executed", "cases": out}


def trace_maintenance(seeds: Sequence[int] = DEFAULT_SEEDS) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for case in ("bandit_like", "middle", "renewal_like"):
        rows: List[Dict[str, Any]] = []
        for seed in seeds:
            spec = spec_from_name(case, int(seed))
            env = MaintenanceReplacementEnv(spec)
            obs, _, done, info = env.reset(seed=int(seed))
            agent = COAdapterMaintenanceReplacement(core=_core())
            t = 0
            while not done and t < TRACE_HORIZON:
                true_health_before = int(getattr(env, "health", info.get("health_true", -1)))
                sel = dict(agent.select(obs) or {})
                a = str(_safe_action(sel, "RUN"))
                if a not in MAINT_ACTIONS:
                    a = "RUN"
                next_obs, r, done, info = env.step(a)
                audit = {
                    "true_health_before": true_health_before,
                    "true_health_norm_before": true_health_before / float(max(1, int(spec.max_health))),
                    "observe_health": str(spec.observe_health),
                    "degradation_prob": float(spec.degradation_prob),
                    "failure_penalty": float(spec.failure_penalty),
                    "repair_cost": float(spec.repair_cost),
                    "replace_cost": float(spec.replace_cost),
                }
                rows.append(_trace_bridge_step("maintenance_replacement", case, int(seed), t, obs, agent, sel, a, float(r), bool(done), audit))
                agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
                obs = next_obs
                t += 1
        out[case] = {"summary": _summarize_rows(rows), "rows": rows}
    return {"status": "executed", "cases": out}


def _classify(result: Mapping[str, Any]) -> Dict[str, Any]:
    findings: List[str] = []
    cases: Dict[str, Any] = {}
    for family, fdata in (result.get("families") or {}).items():
        if not isinstance(fdata, Mapping) or fdata.get("status") != "executed":
            findings.append(f"{family}: not executed")
            continue
        for case, cdata in (fdata.get("cases") or {}).items():
            summary = cdata.get("summary", {}) if isinstance(cdata, Mapping) else {}
            key = f"{family}/{case}"
            modes = summary.get("commitment_modes", {}) or {}
            action_rates = summary.get("action_rates", {}) or {}
            rank_rates = summary.get("chosen_rank1_rates", {}) or {}
            mean_raw_burden = _f(summary.get("mean_raw_burden_proxy"), 0.0) or 0.0
            mean_pub_burden = _f(summary.get("mean_published_burden_pressure"), 0.0) or 0.0
            mean_preventive = _f(summary.get("mean_published_preventive_support"), 0.0) or 0.0
            local_rank = _f(rank_rates.get("published_local_support"), 0.0) or 0.0
            dom_rank = _f(rank_rates.get("commitment_dominance_score"), 0.0) or 0.0
            preventive_rank = _f(rank_rates.get("published_preventive_support"), 0.0) or 0.0
            dominant_mode_share = modes.get("dominance", 0) / float(max(1, summary.get("n_steps", 1)))

            diagnosis = []
            if mean_raw_burden < 0.08:
                diagnosis.append("public/raw burden signal weak")
            elif mean_pub_burden < 0.10:
                diagnosis.append("candidate publication weakens available burden")
            if mean_preventive < 0.05 and mean_raw_burden >= 0.08:
                diagnosis.append("preventive support weak despite raw burden")
            if local_rank >= 0.75 and dom_rank >= 0.75:
                diagnosis.append("local-support dominance survives into commitment")
            if dominant_mode_share >= 0.75:
                diagnosis.append("commitment mostly dominance mode")
            if preventive_rank < 0.20 and mean_raw_burden >= 0.08:
                diagnosis.append("chosen action rarely follows preventive support")
            cases[key] = {
                "action_rates": action_rates,
                "commitment_modes": modes,
                "rank1_rates": rank_rates,
                "mean_raw_burden_proxy": mean_raw_burden,
                "mean_published_burden_pressure": mean_pub_burden,
                "mean_published_preventive_support": mean_preventive,
                "diagnosis_flags": diagnosis,
            }
    # Specific project-level reading.
    maint = cases.get("maintenance_replacement/middle", {})
    if maint:
        flags = maint.get("diagnosis_flags", []) or []
        if "local-support dominance survives into commitment" in flags:
            findings.append("maintenance middle: failure enters before final action; published local support becomes commitment dominance")
        if "preventive support weak despite raw burden" in flags:
            findings.append("maintenance middle: candidate surface still underexpresses preventive burden")
    band = cases.get("bandit/bernoulli_gap_small", {})
    if band and (band.get("action_rates") or {}):
        if max((band.get("action_rates") or {}).values()) >= 0.90:
            findings.append("bandit smoke: action distribution is degenerate; exploration/reopening signal is weak or absent in this smoke")
    return {"case_diagnostics": cases, "headline_findings": findings}


def main() -> None:
    result: Dict[str, Any] = {
        "study": "bridge_signal_trace_v1",
        "status": "diagnostic_not_benchmark_claim",
        "trace_horizon": TRACE_HORIZON,
        "seeds": list(DEFAULT_SEEDS),
        "non_claims": [
            "This is not a performance benchmark.",
            "The family-specific code only instantiates environments/adapters for audit.",
            "No kernel or adapter policy changes are made by this study.",
        ],
        "families": {},
    }
    for name, fn in [
        ("bandit", trace_bandit),
        ("renewal", trace_renewal),
        ("maze", trace_maze),
        ("latent_mechanism", trace_latent),
        ("maintenance_replacement", trace_maintenance),
    ]:
        try:
            result["families"][name] = fn()
        except Exception as exc:
            result["families"][name] = {"status": "failed", "error": repr(exc)}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps({"family_done": name, "status": result["families"][name].get("status")}, sort_keys=True), flush=True)
    result["classification"] = _classify(result)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "families": {k: v.get("status") for k, v in result["families"].items()}}, indent=2, sort_keys=True), flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
