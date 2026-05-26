from __future__ import annotations

import json
from statistics import mean
from typing import Any, Dict, Mapping

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.maze_adapter import COAdapterMaze
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.placement.shape_prior6 import derive_shape_prior6
from environments.maze1.env import GridMazeEnv, MazeSpec
from environments.renewal.env import EnvCfg, CodebookRenewalEnvW
from environments.bandit.bandit import BernoulliBanditEnv


def _core(problem_contract: Mapping[str, Any], shape_prior6: Mapping[str, Any]):
    cfg = {
        "name": "six_question_shape_prior_behavior_v1",
        "elements": {"candidate_surface": {"enabled": True}, "commitment_surface": {"enabled": True, "collapse_enabled": False}},
        "primitives": {"signal_bus": {}, "bandit_stats": {}, "ngram_model": {}},
        "problem_contract": dict(problem_contract),
        "shape_prior6": dict(shape_prior6),
    }
    return build_co_core(cfg)


def _shape_with_updates(base: Mapping[str, Any], notes: str = "shape override for comparison", **updates: float) -> Dict[str, Any]:
    out = {"axes": dict(base.get("axes", {})), "source": "study_override", "status": "declared", "notes": notes}
    out["axes"].update({k: max(0.0, min(1.0, float(v))) for k, v in updates.items()})
    return out


def _maze_contract(partial: bool, dynamic: bool) -> Dict[str, Any]:
    return {
        "actions": {"count": 4, "labels": ["UP", "DOWN", "LEFT", "RIGHT"]},
        "observation_channels": ["visible_position", "visible_goal", "legality_geometry", "trace_history"] if not partial else ["partial_position", "visible_goal", "local_legality", "trace_history"],
        "task_anchor": {"kind": "goal_reach", "provided_externally": True},
        "hard_constraints": ["bounds", "wall_blockage"] if not dynamic else ["bounds"],
        "mutable_factors": ["moving_walls"] if dynamic else [],
        "timescale_profile": {"horizon_fixity": "fixed" if not dynamic else "mixed", "drift": "fixed" if not dynamic else "active"},
        "observability_profile": {"state": "direct" if not partial else "partial", "outcome": "direct", "constraints": "direct" if not partial else "partial"},
        "reversibility_profile": {"action_reversibility": "partly_reversible", "commitment_cost": "medium" if not dynamic else "high"},
    }


def _renewal_contract(volatile: bool) -> Dict[str, Any]:
    return {
        "actions": {"count": 8},
        "observation_channels": ["symbol_observation", "reward_feedback", "trace_history"],
        "task_anchor": {"kind": "predictive_reward_alignment", "provided_externally": True},
        "hard_constraints": [],
        "mutable_factors": [] if not volatile else ["latent_regime_drift"],
        "timescale_profile": {"horizon_fixity": "mixed" if not volatile else "active", "drift": "slow" if not volatile else "active"},
        "observability_profile": {"state": "direct", "outcome": "direct", "constraints": "unknown"},
        "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium" if not volatile else "high"},
    }


def _bandit_contract() -> Dict[str, Any]:
    return {
        "actions": {"count": 4},
        "observation_channels": ["action_identity", "reward_feedback", "trace_history"],
        "task_anchor": {"kind": "reward_maximization", "provided_externally": True},
        "hard_constraints": [],
        "mutable_factors": [],
        "timescale_profile": {"horizon_fixity": "fixed", "drift": "unknown"},
        "observability_profile": {"state": "partial", "outcome": "direct", "constraints": "unknown"},
        "reversibility_profile": {"action_reversibility": "reversible", "commitment_cost": "medium"},
    }


def run_maze(spec: MazeSpec, problem_contract: Mapping[str, Any], shape_prior6: Mapping[str, Any], seeds=range(1), step_limit=50):
    trials = []
    for seed in seeds:
        env = GridMazeEnv(spec=spec)
        env.reset(seed=seed)
        core = _core(problem_contract, shape_prior6)
        ag = COAdapterMaze(core=core)
        steps = 0
        solved = False
        actions = []
        controls = []
        while steps < step_limit and env.pos != env.goal:
            obs = {"family": "maze", "t": steps, **env.get_observation()}
            sel = ag.select(obs)
            a = sel.get("action") if isinstance(sel, dict) else sel
            if a not in ("UP", "DOWN", "LEFT", "RIGHT"):
                a = "RIGHT"
            _, reward, done, _ = env.step(a)
            ag.update({"observation": tuple(env.pos), "reward": reward, "done": done, "action": a})
            actions.append(a)
            hs = core.header.state
            controls.append({"local": hs.local_authority, "nonlocal": hs.nonlocal_authority, "path": hs.path_sensitivity})
            steps += 1
            if done:
                solved = True
                break
        trials.append({"solved": solved, "steps": steps, "actions": actions, "controls": controls})
    solved = [t for t in trials if t["solved"]]
    return {
        "solve_rate": mean(1.0 if t["solved"] else 0.0 for t in trials),
        "mean_steps_solved": mean(t["steps"] for t in solved) if solved else None,
        "seed0_actions": trials[0]["actions"],
        "mean_controls": {k: mean(c[k] for t in trials for c in t["controls"]) for k in ["local", "nonlocal", "path"]},
    }


def run_renewal(noise: float, p_ren: float, problem_contract: Mapping[str, Any], shape_prior6: Mapping[str, Any], seeds=range(1), horizon=50):
    trials = []
    for seed in seeds:
        env = CodebookRenewalEnvW(EnvCfg(A=8, L_win=6, p_ren=p_ren, p_noise=noise, T_max=horizon), seed=seed)
        obs, _, done, _ = env.reset()
        core = _core(problem_contract, shape_prior6)
        ag = COAdapterRenewal(core=core)
        rewards = []
        actions = []
        warmup = [0, 1, 2, 3, 4, 5]
        for a in warmup:
            obs, r, done, _ = env.step(a)
            ag.update({"action": a, "reward": float(r), "done": bool(done), "obs": obs, "A": 8})
            rewards.append(r)
            actions.append(a)
            if done:
                break
        controls = []
        t = len(actions)
        while not done and t < horizon:
            sel = ag.select({"family": "renewal", "t": t, "A": 8, "obs": obs})
            a = sel["action"]
            obs, r, done, _ = env.step(a)
            ag.update({"action": a, "reward": float(r), "done": bool(done), "obs": obs, "A": 8})
            rewards.append(r)
            actions.append(a)
            hs = core.header.state
            controls.append({"local": hs.local_authority, "nonlocal": hs.nonlocal_authority, "path": hs.path_sensitivity})
            t += 1
        trials.append({"reward_rate": mean(rewards), "actions": actions, "controls": controls})
    return {
        "mean_reward_rate": mean(t["reward_rate"] for t in trials),
        "seed0_actions": trials[0]["actions"],
        "mean_controls": {k: mean(c[k] for t in trials for c in t["controls"]) for k in ["local", "nonlocal", "path"]},
    }


def run_bandit(probs, problem_contract: Mapping[str, Any], shape_prior6: Mapping[str, Any], seeds=range(1), horizon=35):
    trials = []
    best = max(probs)
    for seed in seeds:
        env = BernoulliBanditEnv(probs, horizon=horizon)
        env.reset(seed=seed)
        core = _core(problem_contract, shape_prior6)
        ag = COAdapterBandit(core=core, n_arms=len(probs))
        regret = 0.0
        rewards = []
        actions = []
        warmup = [0, 1, 2, 3][:len(probs)]
        for a in warmup:
            _, r, d, _ = env.step(a)
            ag.update({"action": a, "reward": float(r), "done": bool(d)})
            regret += best - probs[a]
            rewards.append(r)
            actions.append(a)
        controls = []
        for t in range(len(warmup), horizon):
            sel = ag.select({"family": "bandit", "t": t, "n_arms": len(probs)})
            a = sel["action"]
            _, r, d, _ = env.step(a)
            ag.update({"action": a, "reward": float(r), "done": bool(d)})
            regret += best - probs[a]
            rewards.append(r)
            actions.append(a)
            hs = core.header.state
            controls.append({"local": hs.local_authority, "nonlocal": hs.nonlocal_authority, "path": hs.path_sensitivity})
        trials.append({"regret": regret, "reward_rate": mean(rewards), "actions": actions, "controls": controls})
    return {
        "mean_regret": mean(t["regret"] for t in trials),
        "mean_reward_rate": mean(t["reward_rate"] for t in trials),
        "seed0_actions": trials[0]["actions"],
        "mean_controls": {k: mean(c[k] for t in trials for c in t["controls"]) for k in ["local", "nonlocal", "path"]},
    }


def main():
    maze_static_contract = _maze_contract(partial=False, dynamic=False)
    maze_dynamic_contract = _maze_contract(partial=True, dynamic=True)
    renewal_stable_contract = _renewal_contract(volatile=False)
    renewal_volatile_contract = _renewal_contract(volatile=True)
    bandit_contract = _bandit_contract()

    priors = {
        "maze_visible_static": derive_shape_prior6(maze_static_contract),
        "maze_partial_dynamic": derive_shape_prior6(maze_dynamic_contract),
        "renewal_stable_noisy": derive_shape_prior6(renewal_stable_contract),
        "renewal_volatile_noisy": derive_shape_prior6(renewal_volatile_contract),
        "bandit_public": derive_shape_prior6(bandit_contract),
    }

    # Deliberately wrong priors, still in the same 6-question language.
    wrong = {
        "maze_visible_static": _shape_with_updates(priors["maze_partial_dynamic"], notes="dynamic shape forced on static maze"),
        "maze_partial_dynamic": _shape_with_updates(priors["maze_visible_static"], notes="static shape forced on dynamic maze"),
        "renewal_stable_noisy": _shape_with_updates(priors["renewal_volatile_noisy"], notes="volatile shape forced on stable renewal"),
        "renewal_volatile_noisy": _shape_with_updates(priors["renewal_stable_noisy"], notes="stable shape forced on volatile renewal"),
        "bandit_public": _shape_with_updates(priors["bandit_public"], hidden_decisiveness=0.90, reshapeability=0.80, local_cue_reliability=0.20, notes="wrong highly hidden/volatile shape forced on public stationary bandit"),
    }

    out = {"study": "six_question_shape_prior_behavior_v1", "shape_prior6": priors, "results": {}}

    out["results"]["maze_visible_static"] = {
        "derived": run_maze(MazeSpec(width=7, height=7, seed=0, partial_observability=False, dynamic_walls=False), maze_static_contract, priors["maze_visible_static"]),
        "wrong_shape": run_maze(MazeSpec(width=7, height=7, seed=0, partial_observability=False, dynamic_walls=False), maze_static_contract, wrong["maze_visible_static"]),
    }
    out["results"]["maze_partial_dynamic"] = {
        "derived": run_maze(MazeSpec(width=7, height=7, seed=0, partial_observability=True, view_radius=1, dynamic_walls=True, wall_flip_prob=0.08, max_flips_per_step=1), maze_dynamic_contract, priors["maze_partial_dynamic"]),
        "wrong_shape": run_maze(MazeSpec(width=7, height=7, seed=0, partial_observability=True, view_radius=1, dynamic_walls=True, wall_flip_prob=0.08, max_flips_per_step=1), maze_dynamic_contract, wrong["maze_partial_dynamic"]),
    }
    out["results"]["renewal_stable_noisy"] = {
        "derived": run_renewal(0.2, 0.02, renewal_stable_contract, priors["renewal_stable_noisy"]),
        "wrong_shape": run_renewal(0.2, 0.02, renewal_stable_contract, wrong["renewal_stable_noisy"]),
    }
    out["results"]["renewal_volatile_noisy"] = {
        "derived": run_renewal(0.2, 0.12, renewal_volatile_contract, priors["renewal_volatile_noisy"]),
        "wrong_shape": run_renewal(0.2, 0.12, renewal_volatile_contract, wrong["renewal_volatile_noisy"]),
    }
    out["results"]["bandit_easy_gap"] = {
        "derived": run_bandit([0.85, 0.55, 0.25, 0.10], bandit_contract, priors["bandit_public"]),
        "wrong_shape": run_bandit([0.85, 0.55, 0.25, 0.10], bandit_contract, wrong["bandit_public"]),
    }
    out["results"]["bandit_hard_gap"] = {
        "derived": run_bandit([0.55, 0.50, 0.45, 0.40], bandit_contract, priors["bandit_public"]),
        "wrong_shape": run_bandit([0.55, 0.50, 0.45, 0.40], bandit_contract, wrong["bandit_public"]),
    }
    return out


if __name__ == "__main__":
    print(json.dumps(main(), indent=2))
