from __future__ import annotations

import json
from copy import deepcopy
from math import log
from pathlib import Path
from statistics import mean
from typing import Any, Dict, Iterable, List, Tuple

from environments.bandit.bandit import BernoulliBanditEnv
from environments.renewal.env import CodebookRenewalEnvW, EnvCfg
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.stoa.bandit.ts import ThompsonSampling
from agents.stoa.renewal.vo_markov import VOKT
from experiments.studies._co_eval_common import (
    DEFAULT_CANONICAL_AGENT_NAME,
    DEFAULT_CANONICAL_MANIFEST,
    assert_valid_co_rollout,
    build_validated_co_core,
    load_co_manifest_params,
)
from experiments.studies._descriptor_plane_v1 import (
    POSTURES,
    bandit_descriptor,
    deformation_summary,
    posture_scores,
    predicted_order,
    problem_contract_for_family,
    renewal_descriptor,
    target_scope_for_family,
)

OUT = Path("outputs/problem_plane_crossfamily_v1.json")
STUDY = "problem_plane_crossfamily_v1"
CANONICAL_PARAMS = load_co_manifest_params(DEFAULT_CANONICAL_MANIFEST, DEFAULT_CANONICAL_AGENT_NAME)
SEEDS = [1, 2]
BANDIT_HORIZON = 150
RENEWAL_HORIZON = 180

BANDIT_TRACK = [
    {"name": "bandit_confusable", "family": "bandit", "probs": [0.46, 0.50, 0.54]},
    {"name": "bandit_clarified", "family": "bandit", "probs": [0.20, 0.50, 0.80]},
    {"name": "bandit_easy", "family": "bandit", "probs": [0.10, 0.20, 0.80]},
]

RENEWAL_TRACK = [
    {"name": "renewal_stable", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.01, "p_noise": 0.00},
    {"name": "renewal_mixed", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.05, "p_noise": 0.04},
    {"name": "renewal_volatile", "family": "renewal", "A": 8, "L_win": 6, "p_ren": 0.15, "p_noise": 0.10},
]


def _safe_float(x: Any, default: float = 0.0) -> float:
    try:
        return float(x)
    except Exception:
        return float(default)


def _entropy_from_counts(counts: Iterable[int]) -> float:
    vals = [max(0, int(v)) for v in counts]
    total = sum(vals)
    if total <= 0:
        return 0.0
    probs = [v / float(total) for v in vals if v > 0]
    ent = -sum(p * log(p) for p in probs)
    max_ent = log(len(vals)) if len(vals) > 1 else 1.0
    if max_ent <= 0:
        return 0.0
    return float(ent / max_ent)


def _apply_contract_overlay(base_params: Dict[str, Any], *, family: str, spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], pred_before: List[str], pred_after: List[str], deformation_name: str, descriptor_after: Dict[str, float]) -> Dict[str, Any]:
    params = deepcopy(base_params)
    params["descriptor_hypothesis"] = {
        "target_scope": target_scope_for_family(family),
        "axes": descriptor,
        "notes": f"Study-declared descriptor for {spec['name']}.",
        "source": "problem_plane_crossfamily_v1",
        "status": "investigatory",
    }
    params["kernel_posture"] = {
        "name": posture_name,
        "axes": deepcopy(POSTURES[posture_name]),
        "notes": f"Study posture {posture_name} attached generically via descriptor-plane evaluation.",
        "status": "investigatory",
    }
    params["prediction_protocol"] = {
        "base_problem": {"name": spec["name"], "notes": "Declared track position only."},
        "predicted_ordering_before": list(pred_before),
        "deformation": {
            "name": deformation_name,
            "notes": "Track-local movement on the descriptor plane.",
            "expected_descriptor_shift": {"axes": deformation_summary(descriptor, descriptor_after)},
        },
        "predicted_ordering_after": list(pred_after),
        "falsifier": "Observed posture ranking fails to move with the declared descriptor shift.",
        "status": "investigatory",
    }
    params["problem_contract"] = problem_contract_for_family(family, spec)
    return params


def _validate_nontrivial_rollout(*, family: str, signal_bus_votes: List[int], co_policies: List[str]) -> None:
    if family == "bandit":
        assert_valid_co_rollout(study_name=STUDY, signal_bus_votes=signal_bus_votes, co_policies=co_policies)
        return
    policies = [str(p) for p in co_policies]
    if policies and all(p == "renewal:safe_default" for p in policies) and all(int(v) == 0 for v in signal_bus_votes):
        raise RuntimeError(f"{STUDY}: renewal rollout stayed on safe_default with zero votes; invalid CO evaluation.")


def _run_bandit_co(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], pred_before: List[str], pred_after: List[str], descriptor_after: Dict[str, float], seed: int) -> Dict[str, Any]:
    params = _apply_contract_overlay(
        CANONICAL_PARAMS,
        family="bandit",
        spec=spec,
        posture_name=posture_name,
        descriptor=descriptor,
        pred_before=pred_before,
        pred_after=pred_after,
        deformation_name="increase_evidence_discriminability",
        descriptor_after=descriptor_after,
    )
    core = build_validated_co_core(
        params,
        study_name=STUDY,
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    env = BernoulliBanditEnv(spec["probs"], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = COAdapterBandit(core=core, n_arms=env.n_arms)
    best_mean = max(spec["probs"])
    regret = 0.0
    rewards: List[float] = []
    actions: List[int] = []
    policies: List[str] = []
    votes: List[int] = []
    for t in range(BANDIT_HORIZON):
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        act = int(sel.get("action", 0)) if isinstance(sel, dict) else int(sel or 0)
        policies.append(str(sel.get("co_policy", "bandit:safe_default")) if isinstance(sel, dict) else "bandit:safe_default")
        votes.append(int(sel.get("signal_bus_votes", 0)) if isinstance(sel, dict) else 0)
        _, r, done, _ = env.step(act)
        agent.update({"action": act, "reward": float(r), "done": bool(done)})
        actions.append(act)
        rewards.append(float(r))
        regret += max(0.0, best_mean - spec["probs"][act])
        if done:
            break
    _validate_nontrivial_rollout(family="bandit", signal_bus_votes=votes, co_policies=policies)
    counts = [actions.count(i) for i in range(len(spec["probs"]))]
    switches = sum(1 for i in range(1, len(actions)) if actions[i] != actions[i - 1])
    return {
        "final_regret": regret,
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "first_25_actions": actions[:25],
        "arm_pull_counts": counts,
        "action_entropy": _entropy_from_counts(counts),
        "switch_rate": switches / float(max(1, len(actions) - 1)),
        "co_votes_nonzero_steps": sum(1 for v in votes if int(v) != 0),
        "co_policy_first10": policies[:10],
    }


def _run_bandit_ts(spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    env = BernoulliBanditEnv(spec["probs"], horizon=BANDIT_HORIZON)
    env.reset(seed=seed)
    agent = ThompsonSampling(env.n_arms)
    best_mean = max(spec["probs"])
    regret = 0.0
    rewards: List[float] = []
    actions: List[int] = []
    for _ in range(BANDIT_HORIZON):
        act = int(agent.select())
        _, r, done, _ = env.step(act)
        agent.update(act, r)
        actions.append(act)
        rewards.append(float(r))
        regret += max(0.0, best_mean - spec["probs"][act])
        if done:
            break
    counts = [actions.count(i) for i in range(len(spec["probs"]))]
    switches = sum(1 for i in range(1, len(actions)) if actions[i] != actions[i - 1])
    return {
        "final_regret": regret,
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "first_25_actions": actions[:25],
        "arm_pull_counts": counts,
        "action_entropy": _entropy_from_counts(counts),
        "switch_rate": switches / float(max(1, len(actions) - 1)),
    }


def _run_renewal_co(spec: Dict[str, Any], posture_name: str, descriptor: Dict[str, float], pred_before: List[str], pred_after: List[str], descriptor_after: Dict[str, float], seed: int) -> Dict[str, Any]:
    params = _apply_contract_overlay(
        CANONICAL_PARAMS,
        family="renewal",
        spec=spec,
        posture_name=posture_name,
        descriptor=descriptor,
        pred_before=pred_before,
        pred_after=pred_after,
        deformation_name="increase_deformation_and_noise",
        descriptor_after=descriptor_after,
    )
    core = build_validated_co_core(
        params,
        study_name=STUDY,
        manifest_path=DEFAULT_CANONICAL_MANIFEST,
        agent_name=DEFAULT_CANONICAL_AGENT_NAME,
    )
    env = CodebookRenewalEnvW(
        EnvCfg(A=int(spec["A"]), L_win=int(spec["L_win"]), p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON),
        seed=seed,
    )
    obs, _, done, _ = env.reset()
    agent = COAdapterRenewal(core=core)
    rewards: List[float] = []
    actions: List[int] = []
    policies: List[str] = []
    votes: List[int] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        sel = agent.select({"family": "renewal", "obs": int(obs), "t": t, "A": int(spec["A"]), "L_win": int(spec["L_win"])})
        act = int(sel.get("action", 0)) if isinstance(sel, dict) else int(sel or 0)
        policies.append(str(sel.get("co_policy", "renewal:safe_default")) if isinstance(sel, dict) else "renewal:safe_default")
        votes.append(int(sel.get("signal_bus_votes", 0)) if isinstance(sel, dict) else 0)
        obs, r, done, _ = env.step(act)
        agent.update({"observation": int(obs), "reward": float(r), "done": bool(done), "action": int(act)})
        actions.append(act)
        rewards.append(float(r))
        t += 1
    _validate_nontrivial_rollout(family="renewal", signal_bus_votes=votes, co_policies=policies)
    counts = [actions.count(i) for i in range(int(spec["A"]))]
    switches = sum(1 for i in range(1, len(actions)) if actions[i] != actions[i - 1])
    return {
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "total_reward": sum(rewards),
        "first_40_actions": actions[:40],
        "action_entropy": _entropy_from_counts(counts),
        "switch_rate": switches / float(max(1, len(actions) - 1)),
        "co_votes_nonzero_steps": sum(1 for v in votes if int(v) != 0),
        "co_policy_first10": policies[:10],
    }


def _run_renewal_vom(spec: Dict[str, Any], seed: int) -> Dict[str, Any]:
    env = CodebookRenewalEnvW(
        EnvCfg(A=int(spec["A"]), L_win=int(spec["L_win"]), p_ren=float(spec["p_ren"]), p_noise=float(spec["p_noise"]), T_max=RENEWAL_HORIZON),
        seed=seed,
    )
    obs, _, done, _ = env.reset()
    agent = VOKT(A=int(spec["A"]), max_order=max(0, int(spec["L_win"]) - 1))
    rewards: List[float] = []
    actions: List[int] = []
    t = 0
    while not done and t < RENEWAL_HORIZON:
        act = int(agent.act(int(obs)))
        obs, r, done, _ = env.step(act)
        actions.append(act)
        rewards.append(float(r))
        t += 1
    counts = [actions.count(i) for i in range(int(spec["A"]))]
    switches = sum(1 for i in range(1, len(actions)) if actions[i] != actions[i - 1])
    return {
        "mean_reward": sum(rewards) / float(len(rewards) or 1),
        "total_reward": sum(rewards),
        "first_40_actions": actions[:40],
        "action_entropy": _entropy_from_counts(counts),
        "switch_rate": switches / float(max(1, len(actions) - 1)),
    }


def _aggregate_bandit_runs(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "mean_final_regret": mean(r["final_regret"] for r in runs),
        "mean_reward": mean(r["mean_reward"] for r in runs),
        "mean_action_entropy": mean(r["action_entropy"] for r in runs),
        "mean_switch_rate": mean(r["switch_rate"] for r in runs),
        "first_run_first25_actions": runs[0]["first_25_actions"] if runs else [],
        "first_run_arm_pull_counts": runs[0]["arm_pull_counts"] if runs else [],
        "co_votes_nonzero_steps_mean": mean(r.get("co_votes_nonzero_steps", 0) for r in runs),
        "co_policy_first10": runs[0].get("co_policy_first10", []),
        "runs": runs,
    }


def _aggregate_renewal_runs(runs: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "mean_reward": mean(r["mean_reward"] for r in runs),
        "mean_total_reward": mean(r["total_reward"] for r in runs),
        "mean_action_entropy": mean(r["action_entropy"] for r in runs),
        "mean_switch_rate": mean(r["switch_rate"] for r in runs),
        "first_run_first40_actions": runs[0]["first_40_actions"] if runs else [],
        "co_votes_nonzero_steps_mean": mean(r.get("co_votes_nonzero_steps", 0) for r in runs),
        "co_policy_first10": runs[0].get("co_policy_first10", []),
        "runs": runs,
    }


def _rank_bandit(results: Dict[str, Dict[str, Any]]) -> List[Tuple[str, float]]:
    return sorted(((name, float(data["mean_final_regret"])) for name, data in results.items()), key=lambda kv: kv[1])


def _rank_renewal(results: Dict[str, Dict[str, Any]]) -> List[Tuple[str, float]]:
    return sorted(((name, float(data["mean_reward"])) for name, data in results.items()), key=lambda kv: -kv[1])


def _evaluate_bandit_track() -> Dict[str, Any]:
    tasks: Dict[str, Any] = {}
    for idx, spec in enumerate(BANDIT_TRACK):
        descriptor = bandit_descriptor(spec["probs"])
        pred_before = predicted_order(descriptor)
        descriptor_after = bandit_descriptor(BANDIT_TRACK[min(idx + 1, len(BANDIT_TRACK) - 1)]["probs"])
        pred_after = predicted_order(descriptor_after)
        posture_results: Dict[str, Any] = {}
        for posture_name in POSTURES:
            runs = [_run_bandit_co(spec, posture_name, descriptor, pred_before, pred_after, descriptor_after, seed) for seed in SEEDS]
            posture_results[posture_name] = _aggregate_bandit_runs(runs)
        ts_runs = [_run_bandit_ts(spec, seed) for seed in SEEDS]
        ts_agg = _aggregate_bandit_runs(ts_runs)
        ranking = _rank_bandit(posture_results)
        tasks[spec["name"]] = {
            "family": "bandit",
            "spec": spec,
            "descriptor": descriptor,
            "posture_scores": posture_scores(descriptor),
            "predicted_order": pred_before,
            "observed_order": [name for name, _ in ranking],
            "top_prediction_match": pred_before[0] == ranking[0][0],
            "postures": posture_results,
            "ts_context": ts_agg,
            "observed_regret_ranking": ranking,
        }
    transitions = []
    for a, b in zip(BANDIT_TRACK[:-1], BANDIT_TRACK[1:]):
        first = tasks[a["name"]]
        second = tasks[b["name"]]
        transitions.append({
            "from": a["name"],
            "to": b["name"],
            "descriptor_shift": deformation_summary(first["descriptor"], second["descriptor"]),
            "predicted_top_shift": [first["predicted_order"][0], second["predicted_order"][0]],
            "observed_top_shift": [first["observed_order"][0], second["observed_order"][0]],
            "top_shift_match": (first["predicted_order"][0], second["predicted_order"][0]) == (first["observed_order"][0], second["observed_order"][0]),
        })
    return {"tasks": tasks, "transitions": transitions}


def _evaluate_renewal_track() -> Dict[str, Any]:
    tasks: Dict[str, Any] = {}
    for idx, spec in enumerate(RENEWAL_TRACK):
        descriptor = renewal_descriptor(p_ren=spec["p_ren"], p_noise=spec["p_noise"])
        pred_before = predicted_order(descriptor)
        next_spec = RENEWAL_TRACK[min(idx + 1, len(RENEWAL_TRACK) - 1)]
        descriptor_after = renewal_descriptor(p_ren=next_spec["p_ren"], p_noise=next_spec["p_noise"])
        pred_after = predicted_order(descriptor_after)
        posture_results: Dict[str, Any] = {}
        for posture_name in POSTURES:
            runs = [_run_renewal_co(spec, posture_name, descriptor, pred_before, pred_after, descriptor_after, seed) for seed in SEEDS]
            posture_results[posture_name] = _aggregate_renewal_runs(runs)
        vom_runs = [_run_renewal_vom(spec, seed) for seed in SEEDS]
        vom_agg = _aggregate_renewal_runs(vom_runs)
        ranking = _rank_renewal(posture_results)
        tasks[spec["name"]] = {
            "family": "renewal",
            "spec": spec,
            "descriptor": descriptor,
            "posture_scores": posture_scores(descriptor),
            "predicted_order": pred_before,
            "observed_order": [name for name, _ in ranking],
            "top_prediction_match": pred_before[0] == ranking[0][0],
            "postures": posture_results,
            "vom_context": vom_agg,
            "observed_reward_ranking": ranking,
        }
    transitions = []
    for a, b in zip(RENEWAL_TRACK[:-1], RENEWAL_TRACK[1:]):
        first = tasks[a["name"]]
        second = tasks[b["name"]]
        transitions.append({
            "from": a["name"],
            "to": b["name"],
            "descriptor_shift": deformation_summary(first["descriptor"], second["descriptor"]),
            "predicted_top_shift": [first["predicted_order"][0], second["predicted_order"][0]],
            "observed_top_shift": [first["observed_order"][0], second["observed_order"][0]],
            "top_shift_match": (first["predicted_order"][0], second["predicted_order"][0]) == (first["observed_order"][0], second["observed_order"][0]),
        })
    return {"tasks": tasks, "transitions": transitions}


def main() -> None:
    bandit = _evaluate_bandit_track()
    renewal = _evaluate_renewal_track()
    out = {
        "study": STUDY,
        "status": "executed",
        "manifest_path": DEFAULT_CANONICAL_MANIFEST.as_posix(),
        "co_agent_name": DEFAULT_CANONICAL_AGENT_NAME,
        "seeds": SEEDS,
        "bandit_horizon": BANDIT_HORIZON,
        "renewal_horizon": RENEWAL_HORIZON,
        "posture_library": POSTURES,
        "tracks": {
            "bandit_evidence_track": bandit,
            "renewal_deformation_track": renewal,
        },
        "judgment": (
            "This study implements a generic descriptor-plane evaluation layer using the same 4-axis schema and the same posture library across bandit and renewal. "
            "Predictions are made from descriptor position rather than family labels; failures to produce ranking shifts should be read against the current live posture law, not explained away after the fact."
        ),
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(out, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
