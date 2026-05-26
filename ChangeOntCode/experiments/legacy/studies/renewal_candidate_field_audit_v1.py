from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List

from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.stoa.renewal.agent_fsm import PhaseFSM
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v4 import (
    POSTURES,
    posture_scores,
    predicted_order,
    problem_contract_for_family,
    renewal_descriptor,
    target_scope_for_family,
)

OUT = Path("outputs/renewal_candidate_field_audit_v1.json")
STUDY = "renewal_candidate_field_audit_v1"
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
RENEWAL_HORIZON = 220
SEEDS = [1, 2, 3]
RENEWAL_TASKS = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_mixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.05, "p_noise": 0.04},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]
FIELDS = ["goal_relation", "context_relation", "reward_relation", "tested_hint", "continuity_support"]


def _co_params(spec: Dict[str, Any]) -> Dict[str, Any]:
    scope = target_scope_for_family("renewal")
    descriptor = renewal_descriptor(
        p_ren=spec["p_ren"],
        p_noise=spec["p_noise"],
        horizon=RENEWAL_HORIZON,
        action_count=spec["A"],
    )
    pred_scores = posture_scores(descriptor, target_scope=scope)
    pred = predicted_order(descriptor, target_scope=scope)
    best_posture = pred[0]
    params = dict(CANONICAL_PARAMS)
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
    params["problem_contract"] = problem_contract_for_family("renewal", spec)
    return params


def _run_co(spec: Dict[str, Any], seed: int, *, field_ablation: Iterable[str] | None = None, field_keep_only: Iterable[str] | None = None) -> Dict[str, Any]:
    A = int(spec["A"])
    L = int(spec["L_win"])
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON), seed=seed)
    obs, _, done, _ = env.reset()
    core = build_validated_co_core(_co_params(spec), study_name=STUDY, manifest_path=DEFAULT_CANONICAL_MANIFEST, agent_name=DEFAULT_CANONICAL_AGENT_NAME)
    agent = COAdapterRenewal(core=core)
    rewards: List[float] = []
    votes: List[int] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        payload = {"family": "renewal", "obs": int(obs), "t": t, "A": A, "L_win": L}
        if field_ablation:
            payload["field_ablation"] = list(field_ablation)
        if field_keep_only:
            payload["field_keep_only"] = list(field_keep_only)
        sel = agent.select(payload)
        act = int(sel.get("action", 0))
        votes.append(int(sel.get("signal_bus_votes", 0)))
        obs, r, done, _ = env.step(act)
        agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": act})
        rewards.append(float(r))
        t += 1
    return {
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "co_votes_nonzero_steps": sum(1 for v in votes if v != 0),
    }


def _run_phase(spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    A = int(spec["A"])
    L = int(spec["L_win"])
    env = CodebookRenewalEnvW(EnvCfg(A=A, L_win=L, p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON), seed=seed)
    obs, _, done, _ = env.reset()
    agent = PhaseFSM(A=A, L_win=L)
    agent.reset(int(obs))
    rewards: List[float] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        act = int(agent.act(int(obs)))
        obs, r, done, _ = env.step(act)
        rewards.append(float(r))
        t += 1
    return {"mean_reward": sum(rewards) / float(len(rewards) or 1)}


def _aggregate(spec: Dict[str, Any], *, field_ablation: Iterable[str] | None = None, field_keep_only: Iterable[str] | None = None) -> Dict[str, Any]:
    runs = [_run_co(spec, seed, field_ablation=field_ablation, field_keep_only=field_keep_only) for seed in SEEDS]
    return {
        "mean_reward": mean(r["mean_reward"] for r in runs),
        "mean_nonzero_vote_steps": mean(r["co_votes_nonzero_steps"] for r in runs),
        "runs": runs,
    }


def main() -> None:
    out: Dict[str, Any] = {
        "study": STUDY,
        "status": "executed",
        "renewal_horizon": RENEWAL_HORIZON,
        "seeds": SEEDS,
        "fields": list(FIELDS),
        "by_task": {},
    }
    for spec in RENEWAL_TASKS:
        task: Dict[str, Any] = {}
        task["baseline"] = _aggregate(spec)
        task["phase_ref"] = {"mean_reward": mean(_run_phase(spec, s)["mean_reward"] for s in SEEDS)}
        task["drop_one"] = {f: _aggregate(spec, field_ablation=[f]) for f in FIELDS}
        task["keep_only_one"] = {f: _aggregate(spec, field_keep_only=[f]) for f in FIELDS}
        out["by_task"][spec["name"]] = task
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
