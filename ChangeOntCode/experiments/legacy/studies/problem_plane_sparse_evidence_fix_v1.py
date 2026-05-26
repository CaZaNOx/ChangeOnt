from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from statistics import mean
from typing import Any, Dict

from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    assert_valid_co_rollout,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v2 import (
    POSTURES,
    bandit_descriptor,
    renewal_descriptor,
    predicted_order,
    posture_scores,
    problem_contract_for_family,
    target_scope_for_family,
)

OUT = Path("outputs/problem_plane_sparse_evidence_fix_v1.json")
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
BANDIT_HORIZON = 80
RENEWAL_HORIZON = 120
SEEDS = [1, 2]

BANDITS = [
    {"name": "bandit_confusable", "family": "bandit", "probs": [0.46, 0.50, 0.54]},
    {"name": "bandit_clarified", "family": "bandit", "probs": [0.20, 0.50, 0.80]},
    {"name": "bandit_easy", "family": "bandit", "probs": [0.10, 0.20, 0.80]},
]
RENEWALS = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]


def _params_for(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float]) -> Dict[str, Any]:
    family = str(spec["family"])
    pred = predicted_order(descriptor, target_scope=target_scope_for_family(family))
    pred_scores = posture_scores(descriptor, target_scope=target_scope_for_family(family))
    params = deepcopy(CANONICAL_PARAMS)
    params["descriptor_hypothesis"] = {
        "target_scope": target_scope_for_family(family),
        "axes": dict(descriptor),
        "status": "investigatory",
        "source": "problem_plane_sparse_evidence_fix_v1",
    }
    params["kernel_posture"] = {
        "name": posture_name,
        "axes": dict(POSTURES[posture_name]),
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


def _run_bandit(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], seed: int) -> Dict[str, Any]:
    core = build_validated_co_core(_params_for(spec, posture_name, descriptor), study_name="problem_plane_sparse_evidence_fix_v1", manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    env = BernoulliBanditEnv(spec["probs"], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = COAdapterBandit(core=core, n_arms=env.n_arms)
    best = max(spec["probs"])
    actions = []
    votes = []
    policies = []
    regret = 0.0
    for t in range(BANDIT_HORIZON):
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        act = int(sel.get("action", 0))
        votes.append(int(sel.get("signal_bus_votes", 0)))
        policies.append(str(sel.get("co_policy", "bandit:safe_default")))
        _, reward, done, _ = env.step(act)
        agent.update({"action": act, "reward": float(reward), "done": bool(done)})
        actions.append(act)
        regret += max(0.0, best - spec["probs"][act])
        if done:
            break
    assert_valid_co_rollout(study_name="problem_plane_sparse_evidence_fix_v1", signal_bus_votes=votes, co_policies=policies)
    return {
        "final_regret": regret,
        "first_25_actions": actions[:25],
        "co_votes_nonzero_steps": sum(1 for v in votes if int(v) != 0),
    }


def _run_renewal(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], seed: int) -> Dict[str, Any]:
    core = build_validated_co_core(_params_for(spec, posture_name, descriptor), study_name="problem_plane_sparse_evidence_fix_v1", manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    env = CodebookRenewalEnvW(
        EnvCfg(A=int(spec["A"]), L_win=int(spec["L_win"]), p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON),
        seed=seed,
    )
    obs, _, done, _ = env.reset()
    agent = COAdapterRenewal(core=core)
    rewards = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": int(spec["A"]), "L_win": int(spec["L_win"])})
        act = int(sel.get("action", 0))
        obs, reward, done, _ = env.step(act)
        agent.update({"observation": int(obs), "reward": float(reward), "done": bool(done), "action": act})
        rewards.append(float(reward))
        t += 1
    return {"mean_reward": sum(rewards) / float(len(rewards) or 1)}


def _bandit_summary(spec: Dict[str, Any]) -> Dict[str, Any]:
    descriptor = bandit_descriptor(spec["probs"], horizon=BANDIT_HORIZON)
    pred = predicted_order(descriptor, target_scope=target_scope_for_family("bandit"))
    pred_scores = posture_scores(descriptor, target_scope=target_scope_for_family("bandit"))
    runs = {}
    for posture_name in POSTURES:
        seed_runs = [_run_bandit(spec, posture_name, descriptor, seed) for seed in SEEDS]
        runs[posture_name] = {"mean_regret": mean(r["final_regret"] for r in seed_runs), "seed_runs": seed_runs}
    observed = [k for k, _ in sorted(((k, v["mean_regret"]) for k, v in runs.items()), key=lambda kv: (kv[1], kv[0]))]
    return {"descriptor": descriptor, "predicted_scores": pred_scores, "predicted_order": pred, "observed_order": observed, "postures": runs}


def _renewal_summary(spec: Dict[str, Any]) -> Dict[str, Any]:
    descriptor = renewal_descriptor(p_ren=spec["p_ren"], p_noise=spec["p_noise"], horizon=RENEWAL_HORIZON, action_count=spec["A"])
    pred = predicted_order(descriptor, target_scope=target_scope_for_family("renewal"))
    pred_scores = posture_scores(descriptor, target_scope=target_scope_for_family("renewal"))
    runs = {}
    for posture_name in POSTURES:
        seed_runs = [_run_renewal(spec, posture_name, descriptor, seed) for seed in SEEDS]
        runs[posture_name] = {"mean_reward": mean(r["mean_reward"] for r in seed_runs), "seed_runs": seed_runs}
    observed = [k for k, _ in sorted(((k, v["mean_reward"]) for k, v in runs.items()), key=lambda kv: (-kv[1], kv[0]))]
    return {"descriptor": descriptor, "predicted_scores": pred_scores, "predicted_order": pred, "observed_order": observed, "postures": runs}


def main() -> None:
    out = {"study": "problem_plane_sparse_evidence_fix_v1", "bandit": {}, "renewal": {}}
    for spec in BANDITS:
        out["bandit"][spec["name"]] = _bandit_summary(spec)
    for spec in RENEWALS:
        out["renewal"][spec["name"]] = _renewal_summary(spec)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
