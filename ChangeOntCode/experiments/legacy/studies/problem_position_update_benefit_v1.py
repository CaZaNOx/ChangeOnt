from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

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
from experiments.studies._descriptor_plane_v4 import (
    POSTURES,
    bandit_descriptor,
    renewal_descriptor,
    posture_scores,
    predicted_order,
    problem_contract_for_family,
    target_scope_for_family,
)

STUDY = "problem_position_update_benefit_v1"
OUT = Path("outputs/problem_position_update_benefit_v1.json")
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
SEEDS = [1, 2]
BANDIT_HORIZON = 140
RENEWAL_HORIZON = 160

BANDIT_TRACK = [
    {"name": "bandit_gap_002", "family": "bandit", "probs": [0.49, 0.50, 0.51]},
    {"name": "bandit_gap_008", "family": "bandit", "probs": [0.46, 0.50, 0.54]},
    {"name": "bandit_gap_030", "family": "bandit", "probs": [0.35, 0.50, 0.65]},
    {"name": "bandit_easy_offset", "family": "bandit", "probs": [0.10, 0.20, 0.80]},
]
RENEWAL_TRACK = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_lowmixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.03, "p_noise": 0.02},
    {"name": "renewal_mixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.05, "p_noise": 0.04},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]


def _rank_distance(pred: List[str], obs: List[str]) -> int:
    pos = {name: i for i, name in enumerate(obs)}
    return sum(abs(i - pos[name]) for i, name in enumerate(pred))


def _params(spec, posture_name, descriptor, pred_scores, pred):
    family = str(spec["family"])
    p = deepcopy(CANONICAL_PARAMS)
    p["descriptor_hypothesis"] = {
        "target_scope": target_scope_for_family(family),
        "axes": dict(descriptor),
        "status": "investigatory",
        "source": STUDY,
    }
    p["kernel_posture"] = {"name": posture_name, "axes": dict(POSTURES[posture_name]), "status": "investigatory"}
    p["prediction_protocol"] = {
        "base_problem": {"name": spec["name"]},
        "predicted_ordering_before": list(pred),
        "predicted_scores": dict(pred_scores),
        "status": "investigatory",
    }
    p["problem_contract"] = problem_contract_for_family(family, spec)
    return p


def _run_bandit(spec, posture, descriptor, pred_scores, pred, seed):
    core = build_validated_co_core(_params(spec, posture, descriptor, pred_scores, pred), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    env = BernoulliBanditEnv(spec["probs"], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = COAdapterBandit(core=core, n_arms=env.n_arms)
    best = max(spec["probs"])
    regret = 0.0
    votes = []
    policies = []
    for t in range(BANDIT_HORIZON):
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        a = int(sel.get("action", 0))
        votes.append(int(sel.get("signal_bus_votes", 0)))
        policies.append(str(sel.get("co_policy", "bandit:safe_default")))
        _, r, done, _ = env.step(a)
        agent.update({"action": a, "reward": float(r), "done": bool(done)})
        regret += max(0.0, best - spec["probs"][a])
        if done:
            break
    assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=votes, co_policies=policies)
    return regret


def _run_renewal(spec, posture, descriptor, pred_scores, pred, seed):
    core = build_validated_co_core(_params(spec, posture, descriptor, pred_scores, pred), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    env = CodebookRenewalEnvW(
        EnvCfg(A=int(spec["A"]), L_win=int(spec["L_win"]), p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON),
        seed=seed,
    )
    obs, _, done, _ = env.reset()
    agent = COAdapterRenewal(core=core)
    rewards = []
    votes = []
    policies = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": int(spec["A"]), "L_win": int(spec["L_win"])} )
        a = int(sel.get("action", 0))
        votes.append(int(sel.get("signal_bus_votes", 0)))
        policies.append(str(sel.get("co_policy", "renewal:safe_default")))
        obs, r, done, _ = env.step(a)
        agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": a})
        rewards.append(float(r))
        t += 1
    if policies and all(p == "renewal:safe_default" for p in policies) and all(v == 0 for v in votes):
        raise RuntimeError("invalid renewal rollout")
    return sum(rewards) / float(len(rewards) or 1)


def _descriptor_for(spec):
    if spec["family"] == "bandit":
        return bandit_descriptor(spec["probs"], horizon=BANDIT_HORIZON)
    return renewal_descriptor(p_ren=spec["p_ren"], p_noise=spec["p_noise"], horizon=RENEWAL_HORIZON, action_count=spec["A"])


def _observe_order(spec, descriptor):
    family = str(spec["family"])
    scope = target_scope_for_family(family)
    pred_scores = posture_scores(descriptor, target_scope=scope)
    pred = predicted_order(descriptor, target_scope=scope)
    rec = {}
    for posture in POSTURES:
        vals = [
            _run_bandit(spec, posture, descriptor, pred_scores, pred, s) if family == "bandit" else _run_renewal(spec, posture, descriptor, pred_scores, pred, s)
            for s in SEEDS
        ]
        rec[posture] = {"mean_score": mean(vals), "seed_scores": vals}
    observed = [k for k, _ in sorted(((k, v["mean_score"]) for k, v in rec.items()), key=(lambda kv: (kv[1], kv[0])) if family == "bandit" else (lambda kv: (-kv[1], kv[0])))]
    return rec, observed


def _eval_track(track: List[Dict[str, Any]]) -> Dict[str, Any]:
    anchor = track[0]
    stale_desc = _descriptor_for(anchor)
    scope = target_scope_for_family(str(anchor["family"]))
    stale_pred = predicted_order(stale_desc, target_scope=scope)
    stale_scores = posture_scores(stale_desc, target_scope=scope)

    points = []
    stale_exact = 0
    updated_exact = 0
    stale_better = 0
    updated_better = 0
    ties = 0

    for i, spec in enumerate(track):
        updated_desc = _descriptor_for(spec)
        updated_pred = predicted_order(updated_desc, target_scope=scope)
        updated_scores = posture_scores(updated_desc, target_scope=scope)
        postures, observed = _observe_order(spec, updated_desc)
        d_stale = _rank_distance(stale_pred, observed)
        d_updated = _rank_distance(updated_pred, observed)
        if stale_pred == observed:
            stale_exact += 1
        if updated_pred == observed:
            updated_exact += 1
        if d_updated < d_stale:
            updated_better += 1
        elif d_stale < d_updated:
            stale_better += 1
        else:
            ties += 1
        points.append({
            "index": i,
            "name": spec["name"],
            "updated_descriptor": updated_desc,
            "stale_predicted_order": stale_pred,
            "stale_predicted_scores": stale_scores,
            "updated_predicted_order": updated_pred,
            "updated_predicted_scores": updated_scores,
            "observed_order": observed,
            "rank_distance_stale": d_stale,
            "rank_distance_updated": d_updated,
            "updated_beats_stale": d_updated < d_stale,
            "stale_beats_updated": d_stale < d_updated,
            "postures": postures,
        })
    return {
        "anchor_problem": anchor["name"],
        "anchor_descriptor": stale_desc,
        "stale_predicted_order": stale_pred,
        "summary": {
            "points": len(points),
            "stale_exact_matches": stale_exact,
            "updated_exact_matches": updated_exact,
            "updated_better_count": updated_better,
            "stale_better_count": stale_better,
            "tie_count": ties,
        },
        "points": points,
    }


def main():
    out = {
        "study": STUDY,
        "status": "executed",
        "seeds": SEEDS,
        "bandit_horizon": BANDIT_HORIZON,
        "renewal_horizon": RENEWAL_HORIZON,
        "bandit_track": _eval_track(BANDIT_TRACK),
        "renewal_track": _eval_track(RENEWAL_TRACK),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
