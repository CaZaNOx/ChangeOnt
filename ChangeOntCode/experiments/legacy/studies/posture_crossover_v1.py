from __future__ import annotations

import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from environments.bandit.bandit import BernoulliBanditEnv
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.integration.core_builder import build_co_core

OUT_PATH = Path("outputs/posture_crossover_v1_results.json")

COMMON_PARAMS: Dict[str, Any] = {
    "header": {"mode": "SSI"},
    "elements": {
        "haq": {"enabled": True, "history_len": 64, "ema_alpha": 0.2},
        "EC_Identity": {"enabled": True},
        "density": {"enabled": True, "rounding": 2},
        "change_ops": {"enabled": True, "k": 4, "mdl_select": False},
        "candidate_surface": {"enabled": True},
        "commitment_surface": {
            "enabled": True,
            "prefer_bus_if_present": True,
            "use_translator": True,
            "blend_mode": "co_only",
            "use_classical_proposal": False,
            "allow_classical_fallback": False,
            "allow_policy_rescue": False,
            "co_weight_override": None,
            "eps_on_cycle": 0.10,
            "ngram_order": 2,
            "greedy_explore_bias": 0.10,
        },
    },
    "primitives": {
        "signal_bus": {},
        "kernel_substrate": {},
        "P0": {},
        "P1": {},
        "P2": {},
        "P4": {"epsilon": 0.2, "window": 5},
        "P7": {},
        "P16": {},
        "p10": {},
        "p12": {},
        "id_mem": {},
        "bandit_stats": {},
        "ngram_model": {},
    },
    "combinator": {"order": ["haq", "EC_Identity", "density", "change_ops", "candidate_surface", "commitment_surface"]},
}

POSTURES: Dict[str, Dict[str, Any]] = {
    "early_hardening": {
        "name": "early_hardening",
        "axes": {
            "hardening_bias": 0.85,
            "reopen_bias": 0.25,
            "persistence_depth": 0.60,
            "contradiction_tolerance": 0.35,
            "collapse_readiness": 0.55,
        },
    },
    "late_hardening": {
        "name": "late_hardening",
        "axes": {
            "hardening_bias": 0.20,
            "reopen_bias": 0.80,
            "persistence_depth": 0.40,
            "contradiction_tolerance": 0.35,
            "collapse_readiness": 0.20,
        },
    },
}

ENVS: Dict[str, Dict[str, Any]] = {
    "P_confusable_stationary": {
        "probs": [0.46, 0.50, 0.54],
        "horizon": 400,
        "descriptor_hypothesis": {
            "target_scope": "hypothesis_over_anchor",
            "axes": {
                "evidence_discriminability": 0.22,
                "persistence_reliability": 0.85,
                "revision_cost": 0.80,
                "deformation_rate": 0.05,
            },
        },
        "predicted_ordering": ["late_hardening", "early_hardening"],
    },
    "P_clarified_stationary": {
        "probs": [0.20, 0.50, 0.80],
        "horizon": 400,
        "descriptor_hypothesis": {
            "target_scope": "hypothesis_over_anchor",
            "axes": {
                "evidence_discriminability": 0.82,
                "persistence_reliability": 0.85,
                "revision_cost": 0.45,
                "deformation_rate": 0.05,
            },
        },
        "predicted_ordering": ["early_hardening", "late_hardening"],
    },
}

SEEDS: List[int] = [1, 2, 3]
ACTION_EQUIVALENCE_SEED = 2
ACTION_EQUIVALENCE_HORIZON = 100


def run_bandit(env_name: str, env_cfg: Dict[str, Any], posture_name: str, posture_cfg: Dict[str, Any], seed: int) -> Dict[str, Any]:
    env = BernoulliBanditEnv(env_cfg["probs"], horizon=int(env_cfg["horizon"]))
    env.reset(seed=seed)
    params = dict(COMMON_PARAMS)
    params["descriptor_hypothesis"] = dict(env_cfg["descriptor_hypothesis"])
    params["kernel_posture"] = dict(posture_cfg)
    params["prediction_protocol"] = {
        "base_problem": {"name": env_name},
        "predicted_ordering_before": list(env_cfg["predicted_ordering"]),
        "status": "declared",
    }
    core = build_co_core(params)
    agent = COAdapterBandit(core=core, name=posture_name, n_arms=env.n_arms)

    best = max(env_cfg["probs"])
    regret = 0.0
    pulls = [0] * env.n_arms
    actions: List[int] = []
    done = False
    t = 0
    while not done:
        sel = agent.select({"family": "bandit", "t": t, "n_arms": env.n_arms})
        a = int(sel["action"]) if isinstance(sel, dict) else int(sel)
        actions.append(a)
        _, r, done, _ = env.step(a)
        agent.update({"action": a, "reward": float(r), "done": bool(done)})
        pulls[a] += 1
        regret += max(0.0, best - env_cfg["probs"][a])
        t += 1
    return {
        "seed": seed,
        "final_regret": regret,
        "pulls": pulls,
        "actions": actions,
    }


def main() -> None:
    out: Dict[str, Any] = {
        "study": "posture_crossover_v1",
        "status": "failed_first_attempt",
        "seeds": SEEDS,
        "envs": {},
        "action_equivalence_check": {},
        "conclusion": {
            "predicted_crossover_observed": False,
            "summary": (
                "The first controlled bandit posture crossover attempt did not produce the predicted ranking shift. "
                "Across the tested seeds, early_hardening and late_hardening produced identical mean regret in both the confusable and clarified settings."
            ),
        },
    }

    for env_name, env_cfg in ENVS.items():
        env_out: Dict[str, Any] = {
            "probs": list(env_cfg["probs"]),
            "horizon": int(env_cfg["horizon"]),
            "descriptor_hypothesis": dict(env_cfg["descriptor_hypothesis"]),
            "predicted_ordering": list(env_cfg["predicted_ordering"]),
            "postures": {},
        }
        ranking: List[tuple[str, float]] = []
        for posture_name, posture_cfg in POSTURES.items():
            runs = [run_bandit(env_name, env_cfg, posture_name, posture_cfg, seed) for seed in SEEDS]
            mean_regret = mean(r["final_regret"] for r in runs)
            env_out["postures"][posture_name] = {
                "kernel_posture": dict(posture_cfg),
                "mean_final_regret": mean_regret,
                "runs": [{"seed": r["seed"], "final_regret": r["final_regret"], "pulls": r["pulls"]} for r in runs],
            }
            ranking.append((posture_name, mean_regret))
        env_out["observed_ordering"] = [name for name, _ in sorted(ranking, key=lambda kv: kv[1])]
        out["envs"][env_name] = env_out

        eq_actions = {}
        for posture_name, posture_cfg in POSTURES.items():
            eq_run = run_bandit(
                env_name,
                {**env_cfg, "horizon": ACTION_EQUIVALENCE_HORIZON},
                posture_name,
                posture_cfg,
                ACTION_EQUIVALENCE_SEED,
            )
            eq_actions[posture_name] = eq_run["actions"]
        same = eq_actions["early_hardening"] == eq_actions["late_hardening"]
        first_diff = None
        if not same:
            for i, (a, b) in enumerate(zip(eq_actions["early_hardening"], eq_actions["late_hardening"])):
                if a != b:
                    first_diff = i
                    break
        out["action_equivalence_check"][env_name] = {
            "seed": ACTION_EQUIVALENCE_SEED,
            "horizon": ACTION_EQUIVALENCE_HORIZON,
            "same_actions": same,
            "first_difference_index": first_diff,
            "early_first20": eq_actions["early_hardening"][:20],
            "late_first20": eq_actions["late_hardening"][:20],
        }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
