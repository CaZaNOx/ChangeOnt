from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.stoa.bandit.k1_ucb import KLUCB
from agents.stoa.bandit.stoa_agent_bandit import EpsilonGreedyAgent, UCB1Agent
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.renewal.agent_fsm import LastFSM, NGramFSM, PhaseFSM
from agents.stoa.renewal.vo_markov import VOKT
from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    assert_valid_co_rollout,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v4 import (
    POSTURES,
    bandit_descriptor,
    renewal_descriptor,
    predicted_order,
    posture_scores,
    problem_contract_for_family,
    target_scope_for_family,
)

OUT = Path("outputs/stoa_compare_v4_v1.json")
STUDY = "stoa_compare_v4_v1"
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
BANDIT_HORIZON = 250
RENEWAL_HORIZON = 220
SEEDS = [1, 2, 3]

BANDIT_TASKS = [
    {"name": "bandit_gap_008", "family": "bandit", "probs": [0.46, 0.50, 0.54]},
    {"name": "bandit_gap_030", "family": "bandit", "probs": [0.35, 0.50, 0.65]},
    {"name": "bandit_easy_offset", "family": "bandit", "probs": [0.10, 0.20, 0.80]},
]
RENEWAL_TASKS = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_mixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.05, "p_noise": 0.04},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]


def _co_params(spec: Dict[str, Any]) -> Dict[str, Any]:
    family = str(spec["family"])
    scope = target_scope_for_family(family)
    descriptor = bandit_descriptor(spec["probs"], horizon=BANDIT_HORIZON) if family == "bandit" else renewal_descriptor(p_ren=spec["p_ren"], p_noise=spec["p_noise"], horizon=RENEWAL_HORIZON, action_count=spec["A"])
    pred_scores = posture_scores(descriptor, target_scope=scope)
    pred = predicted_order(descriptor, target_scope=scope)
    best_posture = pred[0]
    params = deepcopy(CANONICAL_PARAMS)
    params["descriptor_hypothesis"] = {
        "target_scope": scope,
        "axes": dict(descriptor),
        "status": "investigatory",
        "source": STUDY,
    }
    params["kernel_posture"] = {
        "name": best_posture,
        "axes": dict(POSTURES[best_posture]),
        "status": "investigatory",
    }
    params["prediction_protocol"] = {
        "base_problem": {"name": spec["name"]},
        "predicted_ordering_before": list(pred),
        "predicted_scores": dict(pred_scores),
        "status": "investigatory",
    }
    params["problem_contract"] = problem_contract_for_family(family, spec)
    return params


def _make_bandit_agent(name: str, spec: Dict[str, Any], seed: int):
    n_arms = len(spec["probs"])
    if name == "co_v4":
        core = build_validated_co_core(_co_params(spec), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
        return COAdapterBandit(core=core, n_arms=n_arms)
    if name == "ucb1":
        return UCB1Agent(n_arms)
    if name == "ts":
        return ThompsonSampling(n_arms)
    if name == "kl_ucb":
        return KLUCB(n_arms)
    if name == "epsgreedy":
        return EpsilonGreedyAgent(n_arms, epsilon=0.1, seed=seed)
    raise ValueError(name)


def _run_bandit(name: str, spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    env = BernoulliBanditEnv(spec["probs"], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = _make_bandit_agent(name, spec, seed)
    best = max(spec["probs"])
    regret = 0.0
    actions: List[int] = []
    votes: List[int] = []
    policies: List[str] = []
    for t in range(BANDIT_HORIZON):
        if name == "co_v4":
            sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
            act = int(sel.get("action", 0))
            votes.append(int(sel.get("signal_bus_votes", 0)))
            policies.append(str(sel.get("co_policy", "bandit:safe_default")))
            _, r, done, _ = env.step(act)
            agent.update({"action": act, "reward": float(r), "done": bool(done)})
        else:
            if hasattr(agent, "select"):
                act = int(agent.select())
            elif hasattr(agent, "act"):
                act = int(agent.act())
            else:
                raise RuntimeError(name)
            _, r, done, _ = env.step(act)
            try:
                agent.update(act, r)
            except TypeError:
                try:
                    agent.update(r)
                except Exception:
                    pass
        actions.append(act)
        regret += max(0.0, best - spec["probs"][act])
        if done:
            break
    if name == "co_v4":
        assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=votes, co_policies=policies)
    return {
        "final_regret": regret,
        "first_20_actions": actions[:20],
        **({"co_votes_nonzero_steps": sum(1 for v in votes if v != 0)} if name == "co_v4" else {}),
    }


def _make_renewal_agent(name: str, spec: Dict[str, Any]):
    A = int(spec["A"])
    L = int(spec["L_win"])
    if name == "co_v4":
        core = build_validated_co_core(_co_params(spec), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
        return COAdapterRenewal(core=core)
    if name == "last":
        return LastFSM(A)
    if name == "phase":
        return PhaseFSM(A=A, L_win=L)
    if name == "ngram":
        return NGramFSM(A=A, k=max(0, L - 1))
    if name == "vom":
        return VOKT(A=A, max_order=max(0, L - 1))
    raise ValueError(name)


def _run_renewal(name: str, spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    A = int(spec["A"])
    L = int(spec["L_win"])
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON), seed=seed)
    obs, _, done, _ = env.reset()
    agent = _make_renewal_agent(name, spec)
    if name != "co_v4":
        agent.reset(int(obs))
    rewards: List[float] = []
    actions: List[int] = []
    votes: List[int] = []
    policies: List[str] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        if name == "co_v4":
            sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": A, "L_win": L})
            act = int(sel.get("action", 0))
            votes.append(int(sel.get("signal_bus_votes", 0)))
            policies.append(str(sel.get("co_policy", "renewal:safe_default")))
        else:
            act = int(agent.act(int(obs)))
        obs, r, done, _ = env.step(act)
        if name == "co_v4":
            agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": act})
        rewards.append(float(r)); actions.append(act); t += 1
    if name == "co_v4":
        if policies and all(p == "renewal:safe_default" for p in policies) and all(int(v) == 0 for v in votes):
            raise RuntimeError("invalid renewal rollout")
    return {
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "first_25_actions": actions[:25],
        **({"co_votes_nonzero_steps": sum(1 for v in votes if v != 0)} if name == "co_v4" else {}),
    }


def _aggregate_bandit(spec: Dict[str, Any]) -> Dict[str, Any]:
    agents = ["co_v4", "ts", "kl_ucb", "ucb1", "epsgreedy"]
    out: Dict[str, Any] = {"probs": spec["probs"], "agents": {}}
    for name in agents:
        runs = [_run_bandit(name, spec, seed) for seed in SEEDS]
        out["agents"][name] = {"mean_final_regret": mean(r["final_regret"] for r in runs), "runs": runs}
    out["regret_ranking"] = sorted(((name, float(rec["mean_final_regret"])) for name, rec in out["agents"].items()), key=lambda kv: kv[1])
    return out


def _aggregate_renewal(spec: Dict[str, Any]) -> Dict[str, Any]:
    agents = ["co_v4", "last", "phase", "ngram", "vom"]
    out: Dict[str, Any] = {"params": {k: spec[k] for k in ("A", "L_win", "p_ren", "p_noise")}, "agents": {}}
    for name in agents:
        runs = [_run_renewal(name, spec, seed) for seed in SEEDS]
        out["agents"][name] = {"mean_reward": mean(r["mean_reward"] for r in runs), "runs": runs}
    out["reward_ranking"] = sorted(((name, float(rec["mean_reward"])) for name, rec in out["agents"].items()), key=lambda kv: (-kv[1], kv[0]))
    return out


def main() -> None:
    out: Dict[str, Any] = {
        "study": STUDY,
        "status": "executed",
        "bandit_horizon": BANDIT_HORIZON,
        "renewal_horizon": RENEWAL_HORIZON,
        "seeds": SEEDS,
        "manifest_path": DEFAULT_CANONICAL_MANIFEST.as_posix(),
        "co_agent_name": DEFAULT_CANONICAL_AGENT_NAME,
        "bandit": {},
        "renewal": {},
        "judgment": "Fresh STOA comparison on the current valid V4 kernel state, using the descriptor-plane predicted best posture per task.",
    }
    for spec in BANDIT_TASKS:
        out["bandit"][spec["name"]] = _aggregate_bandit(spec)
    for spec in RENEWAL_TASKS:
        out["renewal"][spec["name"]] = _aggregate_renewal(spec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
