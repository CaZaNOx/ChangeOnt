from __future__ import annotations

"""Small frozen empirical sanity smoke.

This is deliberately not a benchmark. It runs a small, fixed, low-seed smoke on
already-defined environments after structural/formula gates so we can detect
catastrophic runtime breakage, invalid actions, missing configs, or total lack of
CO telemetry. Constants must not be changed in response to this output.
"""

import json
import sys
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import yaml  # type: ignore

from experiments.runners.maintenance_replacement_runner import run_episode as run_maintenance
from experiments.runners.latent_mechanism_runner import run as run_latent

OUT_DIR = ROOT / "outputs" / "frozen_empirical_sanity_smoke_v1"
OUT = OUT_DIR / "summary.json"


def _load_co_params() -> Dict[str, Any]:
    cfg_path = ROOT / "experiments" / "configs" / "co_agents" / "co_agents_canonical_core.yaml"
    payload = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    for agent in list(payload.get("co_agents", [])):
        if str(agent.get("name")) == "CO_canonical_core":
            return dict(agent.get("params", {}) or {})
    raise RuntimeError("CO_canonical_core config not found")


def _maintenance_rows(co_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for regime in ["bandit_like", "middle", "renewal_like"]:
        for agent in ["random", "threshold", "co"]:
            for seed in [0, 1]:
                params = co_params if agent == "co" else None
                rows.append(run_maintenance(regime=regime, agent_kind=agent, seed=seed, co_params=params))
    return rows


def _latent_rows(co_params: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for agent in [{"type": "random", "params": {}}, {"type": "heuristic", "params": {}}, {"type": "co", "params": co_params}]:
        out_dir = OUT_DIR / "latent_easy_visible_seed0_max20" / str(agent["type"])
        out_dir.mkdir(parents=True, exist_ok=True)
        cfg = {
            "seed": 0,
            "out_dir": str(out_dir),
            "spec": {"name": "easy_visible", "params": {"seed": 0, "max_steps": 20}},
            "agent": agent,
            "log_every": 5,
        }
        cfg_path = out_dir / "cfg.json"
        cfg_path.write_text(json.dumps(cfg, indent=2, sort_keys=True), encoding="utf-8")
        rows.append({"family": "latent_mechanism", "spec": "easy_visible_max20", "seed": 0, "agent_kind": agent["type"], **run_latent(str(cfg_path))})
    return rows


def _aggregate(rows: List[Dict[str, Any]], family: str) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    agents = sorted({str(r.get("agent", r.get("agent_kind", r.get("agent", "unknown")))) for r in rows})
    for agent in agents:
        subset = [r for r in rows if str(r.get("agent", r.get("agent_kind", "unknown"))) == agent]
        if family == "maintenance_replacement":
            out[agent] = {
                "runs": len(subset),
                "mean_total_reward": mean(float(r.get("total_reward", 0.0)) for r in subset) if subset else 0.0,
                "errors": [r for r in subset if "error" in r],
            }
        else:
            out[agent] = {
                "runs": len(subset),
                "mean_reward": mean(float(r.get("mean_reward", 0.0)) for r in subset) if subset else 0.0,
                "success_rate": mean(float(r.get("success", 0.0)) for r in subset) if subset else 0.0,
                "errors": [r for r in subset if "error" in r],
            }
    return out


def main() -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    co_params = _load_co_params()
    maintenance = _maintenance_rows(co_params)
    latent = _latent_rows(co_params)
    result = {
        "study": "frozen_empirical_sanity_smoke_v1",
        "claim_boundary": "small frozen runtime sanity only; not benchmark evidence, not tuning evidence, not novelty proof",
        "frozen_baseline": "STRUCTURAL_BASELINE_FREEZE_2026-05-16.md",
        "constants_frozen": True,
        "maintenance_rows": maintenance,
        "latent_rows": latent,
        "summary": {
            "maintenance_replacement": _aggregate(maintenance, "maintenance_replacement"),
            "latent_mechanism": _aggregate(latent, "latent_mechanism"),
        },
    }
    OUT.write_text(json.dumps(result, indent=2, sort_keys=True), encoding="utf-8")
    return result


if __name__ == "__main__":
    payload = main()
    print(json.dumps({"output": str(OUT.relative_to(ROOT)), "summary": payload["summary"]}, indent=2, sort_keys=True))
