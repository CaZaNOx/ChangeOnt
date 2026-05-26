from __future__ import annotations

"""Pass-1 factor/causal sweep v1.

Diagnostic-only investigation of why the current Pass-1 CO kernel performs as it
does against repo-available public/STOA baselines.  The sweep varies generic
kernel factors and counterfactual public-shape profiles.  It is not a tuning run
and it must not be treated as evidence that any counterfactual variant is
canonical.

Factors varied:
- recent kernel mechanisms: dynamic shape, quotient, scheduler, sequence;
- dynamic-shape update rate;
- public shape profile / shape derivation counterfactuals;
- generic readout resolver gate permissiveness/conservativeness.

Guards:
- no native action-name bonuses;
- no hidden state / DP value inside CO;
- no family-specific kernel rules;
- shape variants are labelled study counterfactuals;
- baselines remain external comparison only.
"""

import argparse
import copy
import json
import os
import subprocess
import sys
import time
from collections import Counter, defaultdict
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, pstdev
from typing import Any, Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from experiments.studies._co_eval_common import load_co_manifest_params, build_validated_co_core
from agents.co.placement.shape_prior6 import SHAPE_PRIOR6_AXES, derive_shape_prior6, shape_prior6_to_direct_controls

STUDY = "pass1_factor_causal_sweep_v1"
OUT_DIR = ROOT / "outputs" / STUDY
RUNS_JSONL = OUT_DIR / "runs.jsonl"
STEPS_JSONL = OUT_DIR / "steps.jsonl"
SUMMARY_JSON = OUT_DIR / "summary.json"
SHAPE_JSON = OUT_DIR / "shape_factor_reports.json"
REPORT_MD = ROOT.parent / "PASS1_FACTOR_CAUSAL_SWEEP_REPORT_2026-05-25.md"

SEEDS = [0]
BANDIT_HORIZON = 24
RENEWAL_HORIZON = 24
MAZE_MAX_STEPS = 32
LATENT_MAX_STEPS = 8

CLAIM_BOUNDARY = (
    "Diagnostic factor sweep only. Counterfactual shapes/readout parameters are not canonical, not tuned outputs, "
    "and not evidence for publication claims. The goal is causal understanding: which generic factors explain current "
    "CO behavior and where performance deficits remain after plausible factor variation."
)

SHAPE_VARIANTS: Dict[str, Dict[str, float]] = {
    "shape_flat_mid": {k: 0.50 for k in SHAPE_PRIOR6_AXES},
    "shape_local_fast": {
        "hidden_decisiveness": 0.00,
        "reshapeability": 0.25,
        "local_cue_reliability": 1.00,
        "revision_cost": 0.00,
        "consequence_span": 0.00,
        "topology_constraint": 0.25,
    },
    "shape_hidden_long": {
        "hidden_decisiveness": 1.00,
        "reshapeability": 0.75,
        "local_cue_reliability": 0.25,
        "revision_cost": 1.00,
        "consequence_span": 1.00,
        "topology_constraint": 0.50,
    },
    "shape_rigid_topology": {
        "hidden_decisiveness": 0.50,
        "reshapeability": 0.00,
        "local_cue_reliability": 0.75,
        "revision_cost": 0.75,
        "consequence_span": 0.75,
        "topology_constraint": 1.00,
    },
}

VARIANTS: Dict[str, Dict[str, Any]] = {
    "co_canonical": {},
    "co_static_shape": {"candidate_surface": {"dynamic_shape_enabled": False}},
    "co_no_quotient": {"candidate_surface": {"quotient_enabled": False}},
    "co_no_scheduler": {"candidate_surface": {"recursion_scheduler_enabled": False}},
    "co_no_sequence": {"candidate_surface": {"sequence_composition_enabled": False}},
    "co_minimal_recent_core": {"candidate_surface": {"dynamic_shape_enabled": False, "quotient_enabled": False, "recursion_scheduler_enabled": False, "sequence_composition_enabled": False}},
    "co_dynamic_alpha_low": {"candidate_surface": {"dynamic_shape_alpha": 0.12}},
    "co_dynamic_alpha_high": {"candidate_surface": {"dynamic_shape_alpha": 0.70}},
    "co_shape_flat_mid": {"shape_axes": SHAPE_VARIANTS["shape_flat_mid"]},
    "co_shape_local_fast": {"shape_axes": SHAPE_VARIANTS["shape_local_fast"]},
    "co_shape_hidden_long": {"shape_axes": SHAPE_VARIANTS["shape_hidden_long"]},
    "co_shape_rigid_topology": {"shape_axes": SHAPE_VARIANTS["shape_rigid_topology"]},
    "co_readout_resolver_permissive": {"commitment_formula_params": {
        "preblocking_carrier_pressure_floor": 0.34,
        "preblocking_carrier_pressure_base": 0.62,
        "preblocking_resolver_support_floor": 0.06,
        "preblocking_resolver_support_base": 0.08,
        "preblocking_score_margin_base": 0.040,
        "preblocking_support_margin_base": 0.080,
        "resolver_support_threshold": 0.055,
        "resolver_support_scaled_base": 0.055,
    }},
    "co_readout_resolver_conservative": {"commitment_formula_params": {
        "preblocking_carrier_pressure_floor": 0.50,
        "preblocking_carrier_pressure_base": 0.78,
        "preblocking_resolver_support_floor": 0.14,
        "preblocking_resolver_support_base": 0.16,
        "preblocking_score_margin_base": 0.075,
        "preblocking_support_margin_base": 0.145,
        "resolver_support_threshold": 0.11,
        "resolver_support_scaled_base": 0.11,
    }},
}

FACTOR_GROUPS = {
    "canonical": ["co_canonical"],
    "mechanism_ablation": ["co_static_shape", "co_no_quotient", "co_no_scheduler", "co_no_sequence", "co_minimal_recent_core"],
    "dynamic_alpha": ["co_dynamic_alpha_low", "co_dynamic_alpha_high"],
    "shape_counterfactual": ["co_shape_flat_mid", "co_shape_local_fast", "co_shape_hidden_long", "co_shape_rigid_topology"],
    "readout_gate": ["co_readout_resolver_permissive", "co_readout_resolver_conservative"],
}

BASELINE_RUNNERS = {
    "bandit": ["ts", "ucb1", "kl_ucb", "epsgreedy"],
    "renewal": ["phase", "last", "ngram", "vom"],
    "maze": ["astar_full_grid", "bfs_full_grid", "visible_replanning_astar"],
    "latent": ["heuristic", "random"],
    "maintenance": ["threshold", "threshold_opt", "q_learning", "random", "finite_horizon_dp"],
}


def _iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_safe(x: Any) -> Any:
    if isinstance(x, Mapping):
        return {str(k): _json_safe(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_json_safe(v) for v in x]
    if isinstance(x, (str, int, float, bool)) or x is None:
        return x
    return str(x)


def _append_jsonl(path: Path, row: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(_json_safe(dict(row)), sort_keys=True) + "\n")


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(_json_safe(payload), indent=2, sort_keys=True), encoding="utf-8")


def _read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _clear_outputs() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in (RUNS_JSONL, STEPS_JSONL, SUMMARY_JSON, SHAPE_JSON):
        if p.exists():
            p.unlink()


def _mean(xs: Sequence[float]) -> Optional[float]:
    return float(mean(xs)) if xs else None


def _std(xs: Sequence[float]) -> float:
    return float(pstdev(xs)) if len(xs) > 1 else 0.0


def _base_params() -> Dict[str, Any]:
    return load_co_manifest_params(ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml")


def _params_for_variant(base: Mapping[str, Any], variant: str) -> Dict[str, Any]:
    cfg = VARIANTS.get(variant, {})
    params = copy.deepcopy(dict(base))
    elements = dict(params.get("elements", {}) or {})
    cand = dict(elements.get("candidate_surface", {}) or {})
    cand.setdefault("enabled", True)
    cand.update(dict(cfg.get("candidate_surface", {}) or {}))
    elements["candidate_surface"] = cand
    comm = dict(elements.get("commitment_surface", {}) or {})
    comm.setdefault("enabled", True)
    if cfg.get("commitment_formula_params"):
        base_formula = dict(comm.get("commitment_formula_params", {}) or {})
        base_formula.update(dict(cfg.get("commitment_formula_params") or {}))
        comm["commitment_formula_params"] = base_formula
    elements["commitment_surface"] = comm
    params["elements"] = elements
    return params


@contextmanager
def _shape_override_context(axes: Optional[Mapping[str, float]]):
    if not axes:
        yield
        return
    import agents.co.core.contracts.placement_contract as pc
    orig = pc.build_runtime_contract
    shape = {"schema": "co_shape_prior6_v2", "axes": dict(axes), "source": "pass1_factor_counterfactual_shape_override", "status": "study_only"}

    def wrapped(params: Any):
        payload = dict(params or {}) if isinstance(params, Mapping) else {}
        if payload.get("problem_contract"):
            payload["shape_prior6"] = shape
            return orig(payload)
        return orig(params)

    pc.build_runtime_contract = wrapped
    try:
        yield
    finally:
        pc.build_runtime_contract = orig


def _variant_shape_axes(variant: str) -> Optional[Dict[str, float]]:
    axes = VARIANTS.get(variant, {}).get("shape_axes")
    return dict(axes) if isinstance(axes, Mapping) else None


def _core_for_variant(base: Mapping[str, Any], variant: str):
    return build_validated_co_core(_params_for_variant(base, variant), study_name=STUDY)


def _rows_from_agent(agent: Any) -> List[Dict[str, Any]]:
    core = getattr(agent, "core", None)
    prims = getattr(core, "primitives", {}) if core is not None else {}
    rows = prims.get("__candidate_publication_rows__", []) if isinstance(prims, dict) else []
    return [dict(r) for r in rows if isinstance(r, dict)]


def _step_telemetry(sel: Mapping[str, Any], rows: Sequence[Mapping[str, Any]]) -> Dict[str, Any]:
    def avg(key: str) -> float:
        vals = []
        for r in rows:
            try:
                vals.append(float(r.get(key, 0.0) or 0.0))
            except Exception:
                pass
        return float(mean(vals)) if vals else 0.0
    def mx(key: str) -> float:
        vals = []
        for r in rows:
            try:
                vals.append(float(r.get(key, 0.0) or 0.0))
            except Exception:
                pass
        return max(vals) if vals else 0.0
    rel = {}
    for r in rows:
        if isinstance(r.get("relation_surface_telemetry"), dict):
            rel = dict(r.get("relation_surface_telemetry") or {})
            break
    return {
        "candidate_rows": len(rows),
        "sequence_active_rows": sum(1 for r in rows if bool(r.get("sequence_composition_active"))),
        "quotient_rows": sum(1 for r in rows if float(r.get("quotient_share_count", 1) or 1) > 1),
        "avg_recursion_demand": avg("recursion_scheduler_demand"),
        "max_recursion_demand": mx("recursion_scheduler_demand"),
        "avg_sequence_support": avg("sequence_composition_support"),
        "max_sequence_support": mx("sequence_composition_support"),
        "avg_field_debt": avg("field_debt"),
        "avg_grey_pressure": avg("field_grey_pressure"),
        "dynamic_shape_applied": any(isinstance(r.get("dynamic_shape_update"), dict) and bool(r.get("dynamic_shape_update", {}).get("applied")) for r in rows),
        "shape_gauged_resolver": bool(sel.get("shape_gauged_resolver_timing_applied", False)),
        "commitment_mode": str(sel.get("canonical_commitment_mode", "")),
        "commitment_reason": str(sel.get("canonical_commitment_reason", "")),
        "relations_by_type": dict(rel.get("relations_by_type", {}) or {}),
    }


def _record_run(row: Mapping[str, Any]) -> Dict[str, Any]:
    _append_jsonl(RUNS_JSONL, row)
    return dict(row)


def _record_step(row: Mapping[str, Any]) -> None:
    _append_jsonl(STEPS_JSONL, row)


def _run_co_bandit(base: Mapping[str, Any], variant: str, seed: int) -> Dict[str, Any]:
    from environments.bandit.bandit import BernoulliBanditEnv
    from agents.co.adapters.bandit_adapter import COAdapterBandit
    probs = [0.10, 0.20, 0.80]
    env = BernoulliBanditEnv(probs, horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    core = _core_for_variant(base, variant)
    agent = COAdapterBandit(core=core, n_arms=env.n_arms)
    total_reward = 0.0; regret = 0.0; actions=[]; done=False; t=0
    with _shape_override_context(_variant_shape_axes(variant)):
        while not done and t < BANDIT_HORIZON:
            sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
            act = int(sel["action"])
            _, r, done, _ = env.step(act)
            rows = _rows_from_agent(agent)
            tel = _step_telemetry(sel, rows)
            _record_step({"family":"bandit","mode":"easy_public_bandit","variant":variant,"seed":seed,"t":t,"action":act,"reward":float(r), **tel})
            agent.update({"action": act, "reward": float(r), "done": bool(done)})
            total_reward += float(r); regret += max(0.0, max(probs) - probs[act]); actions.append(act); t += 1
    return {"family":"bandit","mode":"easy_public_bandit","variant":variant,"seed":seed,"agent":variant,"agent_kind":"co_variant","metric_name":"final_cumulative_regret","metric_value":float(regret),"metric_direction":"lower_is_better","secondary_metric":{"total_reward":float(total_reward)},"first_actions":actions[:24],"horizon":BANDIT_HORIZON}


def _run_baseline_bandit(agent_name: str, seed: int) -> Dict[str, Any]:
    from environments.bandit.bandit import BernoulliBanditEnv
    from agents.stoa.bandit.stoa_agent_bandit import UCB1Agent, EpsilonGreedyAgent
    from agents.stoa.bandit.ts import ThompsonSampling
    from agents.stoa.bandit.k1_ucb import KLUCB
    probs=[0.10,0.20,0.80]
    env=BernoulliBanditEnv(probs,horizon=BANDIT_HORIZON); env.reset(seed=seed)
    if agent_name=="ts": agent=ThompsonSampling(env.n_arms)
    elif agent_name=="ucb1": agent=UCB1Agent(env.n_arms)
    elif agent_name=="kl_ucb": agent=KLUCB(env.n_arms)
    else: agent=EpsilonGreedyAgent(env.n_arms, epsilon=0.1, seed=seed)
    total=0.0; regret=0.0; done=False; t=0; actions=[]
    while not done and t < BANDIT_HORIZON:
        act=int(agent.select() if hasattr(agent,"select") else agent.act())
        _,r,done,_=env.step(act)
        try: agent.update(act,r)
        except TypeError:
            try: agent.update(r)
            except Exception: pass
        total += float(r); regret += max(0.0, max(probs)-probs[act]); actions.append(act); t += 1
    return {"family":"bandit","mode":"easy_public_bandit","variant":agent_name,"seed":seed,"agent":agent_name,"agent_kind":"baseline","metric_name":"final_cumulative_regret","metric_value":float(regret),"metric_direction":"lower_is_better","secondary_metric":{"total_reward":float(total)},"first_actions":actions[:24],"horizon":BANDIT_HORIZON}


def _run_co_renewal(base: Mapping[str, Any], variant: str, seed: int) -> Dict[str, Any]:
    from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
    from agents.co.adapters.renewal_adapter import COAdapterRenewal
    A,L=4,3
    env=CodebookRenewalEnvW(EnvCfg(A=A,L_win=L,p_ren=0.04,p_noise=0.02,T_max=RENEWAL_HORIZON), seed=seed)
    obs,_,done,_=env.reset(); core=_core_for_variant(base,variant); agent=COAdapterRenewal(core=core)
    rewards=[]; actions=[]; t=0
    with _shape_override_context(_variant_shape_axes(variant)):
        while not done and t < RENEWAL_HORIZON:
            sel=agent.select({"family":"renewal","obs":int(obs),"t":t,"A":A,"L_win":L})
            act=int(sel["action"])
            obs,r,done,_=env.step(act)
            rows=_rows_from_agent(agent); tel=_step_telemetry(sel, rows)
            _record_step({"family":"renewal","mode":"noisy_renewal","variant":variant,"seed":seed,"t":t,"action":act,"reward":float(r), **tel})
            agent.update({"observation":int(obs),"reward":float(r),"done":bool(done),"action":act})
            rewards.append(float(r)); actions.append(act); t += 1
    mean_reward=float(sum(rewards)/float(len(rewards) or 1))
    return {"family":"renewal","mode":"noisy_renewal","variant":variant,"seed":seed,"agent":variant,"agent_kind":"co_variant","metric_name":"mean_reward","metric_value":mean_reward,"metric_direction":"higher_is_better","secondary_metric":{"total_reward":float(sum(rewards))},"first_actions":actions[:24],"horizon":RENEWAL_HORIZON}


def _run_baseline_renewal(agent_name: str, seed: int) -> Dict[str, Any]:
    from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
    from agents.stoa.renewal.agent_fsm import LastFSM, PhaseFSM, NGramFSM
    from agents.stoa.renewal.vo_markov import VOKT
    A,L=4,3
    env=CodebookRenewalEnvW(EnvCfg(A=A,L_win=L,p_ren=0.04,p_noise=0.02,T_max=RENEWAL_HORIZON), seed=seed)
    obs,_,done,_=env.reset()
    agent = PhaseFSM(A=A,L_win=L) if agent_name=="phase" else LastFSM(A) if agent_name=="last" else NGramFSM(A=A,k=L-1) if agent_name=="ngram" else VOKT(A=A,max_order=L-1)
    if hasattr(agent,"reset"): agent.reset(int(obs))
    rewards=[]; actions=[]; t=0
    while not done and t < RENEWAL_HORIZON:
        act=int(agent.act(int(obs)))
        obs,r,done,_=env.step(act)
        rewards.append(float(r)); actions.append(act); t+=1
    return {"family":"renewal","mode":"noisy_renewal","variant":agent_name,"seed":seed,"agent":agent_name,"agent_kind":"baseline","metric_name":"mean_reward","metric_value":float(sum(rewards)/float(len(rewards) or 1)),"metric_direction":"higher_is_better","secondary_metric":{"total_reward":float(sum(rewards))},"first_actions":actions[:24],"horizon":RENEWAL_HORIZON}


def _run_co_maze(base: Mapping[str, Any], variant: str, seed: int) -> Dict[str, Any]:
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from agents.co.adapters.maze_adapter import COAdapterMaze
    env=GridMazeEnv(spec=MazeSpec(width=5,height=5,seed=seed,partial_observability=False,dynamic_walls=False)); env.reset(seed=seed)
    agent=COAdapterMaze(core=_core_for_variant(base,variant), name="CO_factor")
    total=0.0; actions=[]; done=False; steps=0
    with _shape_override_context(_variant_shape_axes(variant)):
        while not done and steps < MAZE_MAX_STEPS:
            obs={"family":"maze","t":steps,"episode":0, **env.get_observation()}
            sel=agent.select(obs); act=str(sel["action"])
            _,r,done,_=env.step(act)
            rows=_rows_from_agent(agent); tel=_step_telemetry(sel, rows)
            _record_step({"family":"maze","mode":"static_visible_5x5","variant":variant,"seed":seed,"t":steps,"action":act,"reward":float(r), **tel})
            agent.update({"observation":tuple(env.pos),"reward":float(r),"done":bool(done),"action":act})
            total += float(r); actions.append(act); steps += 1
    return {"family":"maze","mode":"static_visible_5x5","variant":variant,"seed":seed,"agent":variant,"agent_kind":"co_variant","metric_name":"episode_return","metric_value":float(total),"metric_direction":"higher_is_better","secondary_metric":{"solved":bool(env.pos==env.goal),"steps":steps},"first_actions":actions[:24],"horizon":MAZE_MAX_STEPS}


def _run_baseline_maze(agent_name: str, seed: int) -> Dict[str, Any]:
    from environments.maze1.env import GridMazeEnv, MazeSpec
    from agents.stoa.maze.stoa_agent_maze import bfs_path
    from agents.stoa.maze.astar_maze import astar_path
    from agents.stoa.maze.replanning_visible_astar import visible_replanning_astar_action
    env=GridMazeEnv(spec=MazeSpec(width=5,height=5,seed=seed,partial_observability=False,dynamic_walls=False)); env.reset(seed=seed)
    planned=[]
    if agent_name=="bfs_full_grid": planned=bfs_path(env)
    elif agent_name=="astar_full_grid": planned=astar_path(env)
    total=0.0; actions=[]; done=False; steps=0
    while not done and steps < MAZE_MAX_STEPS:
        if agent_name in {"bfs_full_grid","astar_full_grid"}: act=planned[steps] if steps < len(planned) else "UP"
        else: act=visible_replanning_astar_action(env.get_observation(), optimistic_unknown=True, unknown_penalty=0.0) or "UP"
        _,r,done,_=env.step(act); total += float(r); actions.append(str(act)); steps += 1
    return {"family":"maze","mode":"static_visible_5x5","variant":agent_name,"seed":seed,"agent":agent_name,"agent_kind":"baseline","metric_name":"episode_return","metric_value":float(total),"metric_direction":"higher_is_better","secondary_metric":{"solved":bool(env.pos==env.goal),"steps":steps},"first_actions":actions[:24],"horizon":MAZE_MAX_STEPS}


def _run_latent_agent(base: Mapping[str, Any], variant: str, seed: int, spec_name: str, agent_kind: str) -> Dict[str, Any]:
    from experiments.runners.latent_mechanism_runner import run as run_latent
    cfg_agent: Dict[str, Any]
    if agent_kind == "co":
        cfg_agent={"type":"co","name":variant,"params":_params_for_variant(base, variant)}
    else:
        cfg_agent={"type":agent_kind,"params":{}}
    cfg_path=OUT_DIR/"configs"/f"latent_{spec_name}_{variant if agent_kind=='co' else agent_kind}_s{seed}.json"
    out_dir=OUT_DIR/"raw_runs"/f"latent_{spec_name}_{variant if agent_kind=='co' else agent_kind}_s{seed}"
    cfg={"seed":seed,"out_dir":str(out_dir),"spec":{"name":spec_name,"params":{"seed":seed,"max_steps":LATENT_MAX_STEPS}},"agent":cfg_agent,"log_every":1}
    cfg_path.parent.mkdir(parents=True, exist_ok=True); cfg_path.write_text(json.dumps(_json_safe(cfg), indent=2, sort_keys=True), encoding="utf-8")
    with _shape_override_context(_variant_shape_axes(variant) if agent_kind=="co" else None):
        result=run_latent(str(cfg_path))
    return {"family":"latent_mechanism","mode":spec_name,"variant":variant if agent_kind=="co" else agent_kind,"seed":seed,"agent":variant if agent_kind=="co" else agent_kind,"agent_kind":"co_variant" if agent_kind=="co" else "baseline","metric_name":"success","metric_value":float(result.get("success",0.0)),"metric_direction":"higher_is_better","secondary_metric":{"mean_reward":float(result.get("mean_reward",0.0)),"steps":int(result.get("steps",0)),"door_reframes":int(result.get("door_reframes",0))},"horizon":LATENT_MAX_STEPS}


def _run_maintenance_agent(base: Mapping[str, Any], variant: str, seed: int, regime: str, agent_kind: str) -> Dict[str, Any]:
    from experiments.runners.maintenance_replacement_runner import build_agent, spec_from_name
    from environments.maintenance_replacement.env import MaintenanceReplacementEnv, ACTIONS
    spec = spec_from_name(regime, seed)
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=seed)
    max_steps = min(16, int(spec.horizon))
    if agent_kind == "co":
        co_params = _params_for_variant(base, variant)
        axes = _variant_shape_axes(variant)
        if axes is not None:
            co_params = copy.deepcopy(co_params)
            co_params["shape_prior6_override"] = {"axes": axes, "source": "pass1_factor_counterfactual_shape_override", "status": "study_only"}
        agent = build_agent("co", seed, spec=spec, co_params=co_params)
        agent_label = variant
        kind = "co_variant"
    else:
        if agent_kind == "finite_horizon_dp" and str(spec.observe_health) != "direct":
            return {"family":"maintenance_replacement","mode":regime,"variant":agent_kind,"seed":seed,"agent":agent_kind,"agent_kind":"baseline","skipped":True,"skip_reason":"finite_horizon_dp skipped: hidden/partial health would be oracle in this regime"}
        try:
            agent = build_agent(agent_kind, seed, spec=spec)
        except Exception as e:
            return {"family":"maintenance_replacement","mode":regime,"variant":agent_kind,"seed":seed,"agent":agent_kind,"agent_kind":"baseline","skipped":True,"skip_reason":repr(e)}
        agent_label = agent_kind
        kind = "baseline"
    total_reward = 0.0
    actions: List[str] = []
    t = 0
    with _shape_override_context(_variant_shape_axes(variant) if agent_kind == "co" else None):
        while not done and t < max_steps:
            if agent_kind == "co":
                sel = agent.select(obs)
                action = str(sel.get("action", "")) if isinstance(sel, dict) else str(sel)
                rows = _rows_from_agent(agent)
                tel = _step_telemetry(sel if isinstance(sel, dict) else {}, rows)
            else:
                action = str(agent.select(obs))
                tel = {}
            if action not in ACTIONS:
                raise ValueError(f"maintenance factor sweep fail-closed: invalid action {action!r}")
            next_obs, reward, done, info = env.step(action)
            total_reward += float(reward)
            actions.append(action)
            if hasattr(agent, "update"):
                agent.update({"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)})
            if agent_kind == "co":
                _record_step({"family":"maintenance_replacement","mode":regime,"variant":variant,"seed":seed,"t":t,"action":action,"reward":float(reward), **tel})
            obs = next_obs
            t += 1
    return {"family":"maintenance_replacement","mode":regime,"variant":agent_label,"seed":seed,"agent":agent_label,"agent_kind":kind,"metric_name":"truncated_total_reward_32","metric_value":float(total_reward),"metric_direction":"higher_is_better","secondary_metric":{"steps":t,"observation_mode":str(spec.observe_health),"truncated": True},"horizon":max_steps,"first_actions":actions[:24]}

def _run_family(fam: str) -> List[Dict[str, Any]]:
    base=_base_params()
    rows=[]
    variants=list(VARIANTS.keys())
    for seed in SEEDS:
        if fam=="bandit":
            for v in variants: rows.append(_record_run(_run_co_bandit(base,v,seed)))
            for b in BASELINE_RUNNERS["bandit"]: rows.append(_record_run(_run_baseline_bandit(b,seed)))
        elif fam=="renewal":
            for v in variants: rows.append(_record_run(_run_co_renewal(base,v,seed)))
            for b in BASELINE_RUNNERS["renewal"]: rows.append(_record_run(_run_baseline_renewal(b,seed)))
        elif fam=="maze":
            for v in variants: rows.append(_record_run(_run_co_maze(base,v,seed)))
            for b in BASELINE_RUNNERS["maze"]: rows.append(_record_run(_run_baseline_maze(b,seed)))
        elif fam=="latent":
            for spec in ["easy_visible", "hidden_depth2"]:
                for v in variants: rows.append(_record_run(_run_latent_agent(base,v,seed,spec,"co")))
                for b in BASELINE_RUNNERS["latent"]: rows.append(_record_run(_run_latent_agent(base,b,seed,spec,b)))
        elif fam=="maintenance":
            for regime in ["bandit_like","middle","renewal_like"]:
                for v in variants: rows.append(_record_run(_run_maintenance_agent(base,v,seed,regime,"co")))
                for b in BASELINE_RUNNERS["maintenance"]: rows.append(_record_run(_run_maintenance_agent(base,b,seed,regime,b)))
        else:
            raise ValueError(fam)
    return rows


def _shape_reports() -> Dict[str, Any]:
    # Reuse the previous comparison study for canonical shapes.
    try:
        from experiments.studies.pass1_all_problem_stoa_comparison_v1 import _shape_reports as previous_shape_reports
        canonical = previous_shape_reports()
    except Exception as e:
        canonical = [{"error": repr(e)}]
    counterfactuals=[]
    for name, axes in SHAPE_VARIANTS.items():
        counterfactuals.append({"variant": name, "shape_prior6": {"axes": axes, "source":"pass1_factor_counterfactual_shape_override", "status":"study_only"}, "direct_controls": shape_prior6_to_direct_controls({"axes":axes})})
    return {"canonical_derived_shape_reports": canonical, "counterfactual_shape_reports": counterfactuals, "claim_boundary": "counterfactual shapes are study-only; canonical shape still derives from public problem contracts"}


def _aggregate(rows: Sequence[Mapping[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    grouped=defaultdict(list)
    for r in rows:
        if r.get("skipped") or r.get("error") or "metric_value" not in r: continue
        grouped[(str(r["family"]), str(r["mode"]), str(r["agent"]))].append(r)
    aggs={}
    for (family,mode,agent), vals in sorted(grouped.items()):
        nums=[float(v["metric_value"]) for v in vals]
        aggs[f"{family}/{mode}/{agent}"]={"family":family,"mode":mode,"agent":agent,"agent_kind":str(vals[0].get("agent_kind")),"metric_name":vals[0].get("metric_name"),"metric_direction":vals[0].get("metric_direction"),"runs":len(vals),"mean_metric_value":_mean(nums),"std_population":_std(nums),"values":nums}
    by_mode=defaultdict(list)
    for val in aggs.values():
        by_mode[(val["family"],val["mode"])].append(val)
    comparisons={}
    for (family,mode), vals in sorted(by_mode.items()):
        co=[v for v in vals if v["agent"]=="co_canonical"]
        if not co: continue
        co=co[0]; direction=str(co["metric_direction"])
        baselines=[v for v in vals if v["agent_kind"]=="baseline"]
        co_vars=[v for v in vals if v["agent_kind"]=="co_variant"]
        if not baselines: continue
        if direction=="lower_is_better":
            best_base=min(baselines, key=lambda x: float(x["mean_metric_value"]))
            best_co=min(co_vars, key=lambda x: float(x["mean_metric_value"]))
            delta_base=float(co["mean_metric_value"])-float(best_base["mean_metric_value"])
            delta_best_co=float(best_co["mean_metric_value"])-float(best_base["mean_metric_value"])
            co_improve=float(co["mean_metric_value"])-float(best_co["mean_metric_value"])
        else:
            best_base=max(baselines, key=lambda x: float(x["mean_metric_value"]))
            best_co=max(co_vars, key=lambda x: float(x["mean_metric_value"]))
            delta_base=float(co["mean_metric_value"])-float(best_base["mean_metric_value"])
            delta_best_co=float(best_co["mean_metric_value"])-float(best_base["mean_metric_value"])
            co_improve=float(best_co["mean_metric_value"])-float(co["mean_metric_value"])
        # group ranges
        group_effects={}
        for g, names in FACTOR_GROUPS.items():
            vals_g=[v for v in co_vars if v["agent"] in names]
            if vals_g:
                ms=[float(v["mean_metric_value"]) for v in vals_g]
                group_effects[g]={"agents":[v["agent"] for v in vals_g],"min":min(ms),"max":max(ms),"range":max(ms)-min(ms),"best_agent": (min(vals_g, key=lambda x: float(x["mean_metric_value"])) if direction=="lower_is_better" else max(vals_g, key=lambda x: float(x["mean_metric_value"]))) ["agent"]}
        comparisons[f"{family}/{mode}"]={"metric_name":co["metric_name"],"metric_direction":direction,"canonical_co_mean":co["mean_metric_value"],"best_baseline_agent":best_base["agent"],"best_baseline_mean":best_base["mean_metric_value"],"canonical_minus_best_baseline":delta_base,"best_co_variant_agent":best_co["agent"],"best_co_variant_mean":best_co["mean_metric_value"],"best_co_variant_minus_best_baseline":delta_best_co,"best_variant_improvement_over_canonical":co_improve,"factor_group_effects":group_effects}
    return aggs, comparisons


def _step_summaries() -> Dict[str, Any]:
    steps=_read_jsonl(STEPS_JSONL)
    out={}
    grouped=defaultdict(list)
    for s in steps:
        grouped[(str(s.get("family")),str(s.get("mode")),str(s.get("variant")))].append(s)
    for (family,mode,variant), vals in grouped.items():
        out[f"{family}/{mode}/{variant}"]={
            "steps": len(vals),
            "dynamic_shape_applied_steps": sum(1 for v in vals if v.get("dynamic_shape_applied")),
            "shape_gauged_resolver_steps": sum(1 for v in vals if v.get("shape_gauged_resolver")),
            "avg_sequence_active_rows": _mean([float(v.get("sequence_active_rows",0) or 0) for v in vals]),
            "avg_quotient_rows": _mean([float(v.get("quotient_rows",0) or 0) for v in vals]),
            "avg_recursion_demand": _mean([float(v.get("avg_recursion_demand",0) or 0) for v in vals]),
            "actions": dict(Counter(str(v.get("action")) for v in vals)),
            "commitment_modes": dict(Counter(str(v.get("commitment_mode")) for v in vals)),
        }
    return out


def _write_report(summary: Mapping[str, Any]) -> None:
    comps=summary.get("comparisons", {})
    lines=[
        "# Pass-1 Factor / Causal Sweep — 2026-05-25",
        "",
        "## Claim boundary",
        "",
        CLAIM_BOUNDARY,
        "",
        "## What varied",
        "",
        "- kernel mechanism toggles: dynamic shape, quotient, scheduler, sequence, all recent core off;",
        "- dynamic-shape update rate;",
        "- counterfactual public shape profiles;",
        "- generic readout resolver gate permissive/conservative settings;",
        "- repo-available baselines/STOA references per family.",
        "",
        "## Main comparison table",
        "",
        "| family/mode | metric | canonical CO | best baseline | best baseline mean | best CO variant | best CO variant mean | canonical-best baseline | best CO-best baseline | best variant improvement |",
        "|---|---|---:|---|---:|---|---:|---:|---:|---:|",
    ]
    for key,val in sorted(comps.items()):
        lines.append(f"| {key} | {val.get('metric_name')} ({val.get('metric_direction')}) | {float(val.get('canonical_co_mean')):.4f} | {val.get('best_baseline_agent')} | {float(val.get('best_baseline_mean')):.4f} | {val.get('best_co_variant_agent')} | {float(val.get('best_co_variant_mean')):.4f} | {float(val.get('canonical_minus_best_baseline')):.4f} | {float(val.get('best_co_variant_minus_best_baseline')):.4f} | {float(val.get('best_variant_improvement_over_canonical')):.4f} |")
    lines += ["", "## Factor interpretation", ""]
    for key,val in sorted(comps.items()):
        ge=val.get("factor_group_effects", {})
        lines.append(f"### {key}")
        lines.append("")
        lines.append(f"- Canonical CO vs best baseline delta: `{float(val.get('canonical_minus_best_baseline')):.4f}`.")
        lines.append(f"- Best CO variant: `{val.get('best_co_variant_agent')}`; delta vs best baseline: `{float(val.get('best_co_variant_minus_best_baseline')):.4f}`.")
        for g,gv in sorted(ge.items()):
            lines.append(f"- `{g}` range: `{float(gv.get('range',0.0)):.4f}`, best within group: `{gv.get('best_agent')}`.")
        lines.append("")
    lines += [
        "## Cold interpretation",
        "",
        "If a counterfactual shape or readout variant improves CO but still remains below the best baseline, the deficit is not explained by that factor alone. If disabling recent mechanisms improves CO, the new mechanism may be misweighted or harmful in that family. If all variants remain far below baseline, the likely cause is deeper adapter/readout/objective mismatch or that the classical baseline is well matched to the family.",
        "",
        "## Full JSON summary",
        "",
        "```json",
        json.dumps(_json_safe(summary), indent=2, sort_keys=True),
        "```",
        "",
    ]
    REPORT_MD.write_text("\n".join(lines), encoding="utf-8")


def _finalize() -> Dict[str, Any]:
    rows=_read_jsonl(RUNS_JSONL)
    aggs, comps=_aggregate(rows)
    summary={"study":STUDY,"status":"executed_family_by_family_timeout_safe","claim_boundary":CLAIM_BOUNDARY,"completed_at":_iso(),"seeds":SEEDS,"run_settings":{"bandit_horizon":BANDIT_HORIZON,"renewal_horizon":RENEWAL_HORIZON,"maze_max_steps":MAZE_MAX_STEPS,"latent_max_steps":LATENT_MAX_STEPS,"maintenance_native_horizons":"regime defaults"},"variants":VARIANTS,"factor_groups":FACTOR_GROUPS,"rows":len(rows),"skipped_rows":sum(1 for r in rows if r.get("skipped")),"aggregates":aggs,"comparisons":comps,"step_summaries":_step_summaries(),"outputs":{"runs_jsonl":str(RUNS_JSONL.relative_to(ROOT)),"steps_jsonl":str(STEPS_JSONL.relative_to(ROOT)),"summary_json":str(SUMMARY_JSON.relative_to(ROOT)),"shape_reports_json":str(SHAPE_JSON.relative_to(ROOT)),"report_md":str(REPORT_MD.relative_to(ROOT.parent))},"non_claims":["Counterfactual shape/readout variants are not canonical.","Do not tune constants from this result.","This sweep is small-N and bounded; it explains behavior, it does not establish final empirical evidence."]}
    _write_json(SUMMARY_JSON, summary); _write_report(summary)
    return summary


def main(argv: Optional[Sequence[str]]=None) -> Dict[str, Any]:
    ap=argparse.ArgumentParser(description="Pass-1 factor/causal sweep")
    ap.add_argument("--family", choices=["bandit","renewal","maze","latent","maintenance"], default=None)
    ap.add_argument("--init-only", action="store_true")
    ap.add_argument("--finalize-only", action="store_true")
    args=ap.parse_args(list(argv) if argv is not None else None)
    if args.init_only:
        _clear_outputs(); _write_json(SHAPE_JSON, _shape_reports()); print(json.dumps({"initialized":True}, indent=2)); return {"initialized":True}
    if args.family:
        rows=_run_family(args.family); print(json.dumps({"family":args.family,"rows":len(rows)}, indent=2)); return {"family":args.family,"rows":len(rows)}
    if args.finalize_only:
        summary=_finalize(); print(json.dumps({"status":summary["status"],"rows":summary["rows"]}, indent=2)); return summary
    _clear_outputs(); _write_json(SHAPE_JSON, _shape_reports())
    env=dict(os.environ); env["PYTHONPATH"]=str(ROOT)+(os.pathsep+env.get("PYTHONPATH","") if env.get("PYTHONPATH") else "")
    for fam in ["bandit","renewal","maze","latent","maintenance"]:
        subprocess.run([sys.executable,"-m","experiments.studies.pass1_factor_causal_sweep_v1","--family",fam], cwd=str(ROOT), env=env, check=True)
    summary=_finalize(); print(json.dumps({"status":summary["status"],"rows":summary["rows"],"summary":str(SUMMARY_JSON)}, indent=2)); return summary

if __name__ == "__main__":
    main()
