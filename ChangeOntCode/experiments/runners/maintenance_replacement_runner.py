from __future__ import annotations

import argparse, json
from pathlib import Path
from typing import Any, Dict, Mapping

from environments.maintenance_replacement.env import ACTIONS, MaintenanceReplacementEnv, MaintenanceSpec
from experiments.baselines.maintenance_replacement import BASELINE_ALIASES, make_maintenance_policy

try:
    from agents.co.adapters.maintenance_replacement_adapter import COAdapterMaintenanceReplacement
    from agents.co.integration.core_builder import build_co_core
    HAS_CO = True
except Exception:
    HAS_CO = False


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(k): _json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_json_safe(v) for v in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def spec_from_name(name: str, seed: int) -> MaintenanceSpec:
    key = str(name or "middle").lower()
    if key in {"bandit_like", "maintenance_bandit_like", "bandit"}:
        return MaintenanceSpec.bandit_like(seed=seed)
    if key in {"renewal_like", "maintenance_renewal_like", "renewal"}:
        return MaintenanceSpec.renewal_like(seed=seed)
    return MaintenanceSpec.middle(seed=seed)


def build_agent(kind: str, seed: int, spec: MaintenanceSpec | None = None, co_params: Dict[str, Any] | None = None):
    k = str(kind).lower()
    spec = spec or spec_from_name("middle", seed)
    if k == "co":
        if not HAS_CO:
            raise RuntimeError("CO adapter unavailable")
        params = dict(co_params or {})
        shape_prior6_override = params.pop("shape_prior6_override", None)
        if not params:
            params = {
                "header": {"type": "SSI"},
                "elements": {
                    "haq": {"enabled": True, "history_len": 16, "ema_alpha": 0.2},
                    # CandidateEvidenceSurface is the public candidate-to-vote
                    # bridge. Without it CommitmentSurface sees no kernel votes
                    # and collapses to tie-breaking over zero scores.
                    "candidate_surface": {"enabled": True},
                    "router": {"enabled": True},
                    "commitment_surface": {"enabled": True, "eps_on_cycle": 0.02, "ngram_order": 0},
                },
                "combinator": {"order": ["haq", "candidate_surface", "router", "commitment_surface"]},
                "primitives": {"signal_bus": {}, "P2": {}, "P4": {}, "P16": {}},
            }
        core = build_co_core(params)
        return COAdapterMaintenanceReplacement(core=core, shape_prior6_override=shape_prior6_override)
    if k in BASELINE_ALIASES:
        return make_maintenance_policy(k, spec, seed=seed)
    raise ValueError(f"unknown maintenance agent kind: {kind}")


def run_episode(*, regime: str = "middle", agent_kind: str = "threshold", seed: int = 0, out_dir: str | None = None, co_params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    spec = spec_from_name(regime, seed)
    env = MaintenanceReplacementEnv(spec)
    obs, _, done, info = env.reset(seed=seed)
    agent = build_agent(agent_kind, seed, spec=spec, co_params=co_params)
    total_reward = 0.0
    rows = []
    while not done:
        co_selection: Dict[str, Any] | None = None
        if agent_kind == "co":
            sel = agent.select(obs)
            co_selection = dict(sel) if isinstance(sel, dict) else {"action": sel}
            action = str(sel.get("action", "")) if isinstance(sel, dict) else str(sel)
        else:
            action = str(agent.select(obs))
        if action not in ACTIONS:
            raise ValueError(
                f"MaintenanceReplacement runner fail-closed: agent {agent_kind!r} emitted invalid action {action!r}. "
                "Evidence-bearing runs must not rescue invalid actions with RUN."
            )
        next_obs, reward, done, info = env.step(action)
        total_reward += float(reward)
        fb = {"action": action, "reward": float(reward), "done": bool(done), "info": dict(info)}
        if hasattr(agent, "update"):
            agent.update(fb)
        row = {"t": int(obs.get("t", 0)), "action": action, "reward": float(reward), "done": bool(done), "obs": obs, "info": info}
        if co_selection is not None:
            row["co_selection"] = co_selection
        rows.append(row)
        obs = next_obs
    result = {
        "family": "maintenance_replacement",
        "regime": regime,
        "agent": agent_kind,
        "seed": int(seed),
        "horizon": int(spec.horizon),
        "observation_mode": str(spec.observe_health),
        "total_reward": float(total_reward),
        "final_health_true": int(info.get("health_true", -1)),
        "steps": len(rows),
    }
    if out_dir:
        out = Path(out_dir)
        out.mkdir(parents=True, exist_ok=True)
        (out / "summary.json").write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
        with (out / "trace.jsonl").open("w", encoding="utf-8") as f:
            for row in rows:
                f.write(json.dumps(_json_safe(row), sort_keys=True) + "\n")
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description="Maintenance/replacement MDP runner")
    ap.add_argument("--regime", default="middle", choices=["bandit_like", "middle", "renewal_like"])
    ap.add_argument("--agent", default="threshold", choices=["threshold", "random", "threshold_opt", "dp", "finite_horizon_dp", "q_learning", "tabular_q", "co"])
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    print(json.dumps(run_episode(regime=args.regime, agent_kind=args.agent, seed=args.seed, out_dir=args.out), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
