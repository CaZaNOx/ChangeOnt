from __future__ import annotations

"""Small cross-family diagnostic after CanonicalCommitmentRule v1.

This is not a benchmark claim. It verifies that the generic commitment/readout
rewrite can run through all active families and records obvious behavior shifts
or failures without tuning to one family.
"""

import json, os
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

import yaml  # type: ignore

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement

from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from environments.maze1.env import GridMazeEnv, MazeSpec
from environments.latent_mechanism.env import LatentMechanismDoorWorld, MechanismSpec
from environments.maintenance_replacement.env import MaintenanceReplacementEnv
from experiments.runners.maintenance_replacement_runner import spec_from_name


OUT = Path("outputs/canonical_commitment_cross_family_smoke_v1.json")


def _canonical_params() -> Dict[str, Any]:
    path = Path("experiments/configs/co_agents/co_agents_canonical_core.yaml")
    payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    for rec in payload.get("co_agents", []):
        if rec.get("name") == "CO_canonical_core":
            return dict(rec.get("params", {}))
    raise RuntimeError("CO_canonical_core missing")


def _core() -> Any:
    return build_co_core(_canonical_params())


def _safe_action(sel: Any, default: Any) -> Any:
    if isinstance(sel, dict):
        return sel.get("action", default)
    return default if sel is None else sel


def run_bandit() -> Dict[str, Any]:
    rows = []
    for seed in (0,):
        env = BernoulliBanditEnv([0.46, 0.50, 0.54], horizon=24)
        env.reset(seed=seed)
        agent = COAdapterBandit(core=_core(), n_arms=3)
        total = 0.0
        counts: Counter = Counter()
        for t in range(24):
            sel = agent.select({"family": "bandit", "t": t, "n_arms": 3})
            a = int(_safe_action(sel, 0))
            if a < 0 or a >= 3:
                a = 0
            _, r, done, info = env.step(a)
            total += float(r)
            counts[a] += 1
            agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
            if done:
                break
        rows.append({"seed": seed, "total_reward": total, "actions": dict(counts)})
    return {"status": "executed_smoke", "rows": rows, "mean_total_reward": mean(r["total_reward"] for r in rows)}


def run_renewal() -> Dict[str, Any]:
    rows = []
    for seed in (0,):
        cfg = EnvCfg(A=4, L_win=4, p_ren=0.08, p_noise=0.02, T_max=24)
        env = CodebookRenewalEnvW(cfg, seed=seed)
        obs, _, done, info = env.reset()
        agent = COAdapterRenewal(core=_core())
        total = 0.0
        counts: Counter = Counter()
        t = 0
        while not done and t < 24:
            sel = agent.select({"family": "renewal", "t": t, "obs": int(obs), "x": int(obs), "A": cfg.A, "action_space": list(range(cfg.A))})
            a = int(_safe_action(sel, 0))
            if a < 0 or a >= cfg.A:
                a = 0
            nxt, r, done, info = env.step(a)
            total += float(r)
            counts[a] += 1
            agent.update({"action": a, "reward": float(r), "done": bool(done), "observation": int(nxt), "info": dict(info)})
            obs = nxt
            t += 1
        rows.append({"seed": seed, "total_reward": total, "actions": dict(counts)})
    return {"status": "executed_smoke", "rows": rows, "mean_total_reward": mean(r["total_reward"] for r in rows)}


def run_maze() -> Dict[str, Any]:
    rows = []
    for seed in (0,):
        spec = MazeSpec(width=7, height=7, seed=seed, partial_observability=False)
        env = GridMazeEnv(spec=spec)
        agent = COAdapterMaze(core=_core())
        counts: Counter = Counter()
        solved = False
        for t in range(24):
            obs = env.get_observation()
            obs["t"] = t
            sel = agent.select(obs)
            a = str(_safe_action(sel, "RIGHT"))
            if a not in ("UP", "DOWN", "LEFT", "RIGHT"):
                a = "RIGHT"
            _, reward, done, info = env.step(a)
            counts[a] += 1
            agent.update({"action": a, "reward": float(reward), "done": bool(done), "info": dict(info)})
            if done or tuple(env.pos) == tuple(env.goal):
                solved = True
                break
        rows.append({"seed": seed, "solved": bool(solved), "steps": sum(counts.values()), "actions": dict(counts)})
    return {"status": "executed_smoke", "rows": rows, "solved_count": sum(1 for r in rows if r["solved"])}


def run_latent() -> Dict[str, Any]:
    specs = {
        "easy_visible": MechanismSpec.easy_visible,
    }
    out: Dict[str, Any] = {}
    for name, maker in specs.items():
        rows = []
        for seed in (0,):
            spec = maker(seed=seed)
            env = LatentMechanismDoorWorld(spec)
            obs, _, done, info = env.reset(seed=seed)
            agent = COAdapterLatentMechanism(core=_core())
            counts: Counter = Counter()
            total = 0.0
            for t in range(min(8, spec.max_steps)):
                obs["t"] = t
                sel = agent.select(obs)
                a = str(_safe_action(sel, "RIGHT"))
                if a not in ("UP", "DOWN", "LEFT", "RIGHT", "INTERACT"):
                    a = "RIGHT"
                obs, r, done, info = env.step(a)
                total += float(r)
                counts[a] += 1
                agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
                if done:
                    break
            rows.append({"seed": seed, "done": bool(done), "total_reward": total, "steps": sum(counts.values()), "actions": dict(counts)})
        out[name] = {"rows": rows, "success_count": sum(1 for r in rows if r["done"])}
    return {"status": "executed_smoke", "specs": out}


def run_maintenance() -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for regime in ("bandit_like", "middle", "renewal_like"):
        rows = []
        for seed in (0,):
            spec = spec_from_name(regime, seed)
            spec.horizon = min(int(spec.horizon), 24)
            env = MaintenanceReplacementEnv(spec)
            obs, _, done, info = env.reset(seed=seed)
            agent = COAdapterMaintenanceReplacement(core=_core())
            total = 0.0
            counts: Counter = Counter()
            while not done:
                sel = agent.select(obs)
                a = str(_safe_action(sel, "RUN"))
                if a not in ("RUN", "INSPECT", "REPAIR", "REPLACE", "WAIT"):
                    a = "RUN"
                obs, r, done, info = env.step(a)
                total += float(r)
                counts[a] += 1
                agent.update({"action": a, "reward": float(r), "done": bool(done), "info": dict(info)})
            rows.append({"seed": seed, "total_reward": total, "actions": dict(counts)})
        out[regime] = {"rows": rows, "mean_total_reward": mean(r["total_reward"] for r in rows)}
    return {"status": "executed_smoke", "regimes": out}


def main() -> None:
    result: Dict[str, Any] = {
        "study": "canonical_commitment_cross_family_smoke_v1",
        "status": "diagnostic_not_benchmark_claim",
        "families": {},
        "non_claims": [
            "Small smoke horizons only.",
            "Not a STOA comparison.",
            "Used to catch runtime crashes and obvious cross-family behavior effects after generic commitment rewrite.",
        ],
    }
    for name, fn in [
        ("bandit", run_bandit),
        ("renewal", run_renewal),
        ("maze", run_maze),
        ("latent_mechanism", run_latent),
        ("maintenance_replacement", run_maintenance),
    ]:
        try:
            result["families"][name] = fn()
        except Exception as exc:
            result["families"][name] = {"status": "failed", "error": repr(exc)}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        print(json.dumps({"family_done": name, "status": result["families"][name].get("status")}, sort_keys=True), flush=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"wrote": str(OUT), "families": {k: v.get("status") for k, v in result["families"].items()}}, indent=2, sort_keys=True), flush=True)
    os._exit(0)


if __name__ == "__main__":
    main()
