from __future__ import annotations

"""Small STOA/baseline comparison for maintenance/replacement.

This is a runner/study scaffold, not evidence of general CO success.  DP is run
only in fully observed regimes; hidden/partial regimes record an explicit skip.
"""

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
from agents.co.placement.shape_prior6 import derive_shape_prior6, shape_prior6_to_direct_controls
from environments.maintenance_replacement.env import MaintenanceReplacementEnv
from experiments.runners.maintenance_replacement_runner import run_episode, spec_from_name

REGIMES = ("bandit_like", "middle", "renewal_like")
DEFAULT_SEEDS = (0, 1, 2)
BASELINE_AGENTS = ("random", "threshold", "threshold_opt", "q_learning", "finite_horizon_dp", "co")


def _shape_report(regime: str) -> Dict[str, Any]:
    spec = spec_from_name(regime, 0)
    env = MaintenanceReplacementEnv(spec)
    obs, _, _, _ = env.reset(seed=0)
    adapter = COAdapterMaintenanceReplacement(core=None)
    contract = adapter._problem_contract(obs)  # public contract audit; no core needed
    shape = derive_shape_prior6(contract)
    controls = shape_prior6_to_direct_controls(shape)
    return {
        "regime": regime,
        "observation_mode": str(spec.observe_health),
        "problem_contract": contract,
        "shape_prior6": shape,
        "direct_controls": controls,
    }


def run_study(seeds=DEFAULT_SEEDS, agents=BASELINE_AGENTS) -> Dict[str, Any]:
    rows: List[Dict[str, Any]] = []
    skips: List[Dict[str, Any]] = []
    for regime in REGIMES:
        spec = spec_from_name(regime, 0)
        for agent in agents:
            if agent == "finite_horizon_dp" and str(spec.observe_health) != "direct":
                skips.append({
                    "regime": regime,
                    "agent": agent,
                    "reason": "finite_horizon_dp is parity-valid only when health is publicly direct-observed",
                })
                continue
            for seed in seeds:
                try:
                    rows.append(run_episode(regime=regime, agent_kind=agent, seed=int(seed)))
                except Exception as exc:
                    rows.append({
                        "family": "maintenance_replacement",
                        "regime": regime,
                        "agent": agent,
                        "seed": int(seed),
                        "error": type(exc).__name__,
                        "message": str(exc),
                    })
    aggregate: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        if "error" in row:
            continue
        key = f"{row['regime']}::{row['agent']}"
        aggregate.setdefault(key, {"regime": row["regime"], "agent": row["agent"], "n": 0, "total_rewards": []})
        aggregate[key]["n"] += 1
        aggregate[key]["total_rewards"].append(float(row["total_reward"]))
    for val in aggregate.values():
        rewards = list(val.pop("total_rewards"))
        val["mean_total_reward"] = float(mean(rewards)) if rewards else None
        val["min_total_reward"] = float(min(rewards)) if rewards else None
        val["max_total_reward"] = float(max(rewards)) if rewards else None
    return {
        "study": "maintenance_replacement_stoa_compare_v1",
        "status": "scaffolded_comparison_not_general_success_claim",
        "seeds": list(map(int, seeds)),
        "shape_reports": [_shape_report(r) for r in REGIMES],
        "rows": rows,
        "skips": skips,
        "aggregate": sorted(aggregate.values(), key=lambda x: (x["regime"], x["agent"])),
        "non_claims": [
            "This does not prove CO generality.",
            "finite_horizon_dp is included only for direct public health observation; skipped otherwise.",
            "q_learning is a sampled public-observation baseline, not an exact optimum.",
        ],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="Maintenance replacement STOA/baseline comparison v1")
    ap.add_argument("--out", default="outputs/maintenance_replacement_stoa_compare_v1.json")
    ap.add_argument("--seeds", default="0,1,2")
    args = ap.parse_args()
    seeds = tuple(int(x.strip()) for x in str(args.seeds).split(",") if x.strip())
    result = run_study(seeds=seeds)
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps({"wrote": str(out), "rows": len(result["rows"]), "skips": len(result["skips"])}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
