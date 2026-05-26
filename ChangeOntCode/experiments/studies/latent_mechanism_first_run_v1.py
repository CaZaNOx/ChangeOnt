from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse, json, tempfile
from pathlib import Path
from statistics import mean
from typing import Any, Dict, List
import yaml  # type: ignore

from experiments.runners.latent_mechanism_runner import run as run_cfg


SPECS = ["easy_visible", "hidden_depth2", "deceptive_depth3"]
SEEDS = list(range(5))
AGENTS = [
    {"type": "random", "params": {}},
    {"type": "heuristic", "params": {}},
    {"type": "co", "params": {}},
]


def _load_co_full_params() -> Dict[str, Any]:
    cfg_path = Path("experiments/configs/co_agents/co_agents_canonical_core.yaml")
    payload = yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}
    for agent in list(payload.get("co_agents", [])):
        if str(agent.get("name")) == "CO_canonical_core":
            return dict(agent.get("params", {}))
    raise RuntimeError("CO_canonical_core config not found")


def _cfg_dict(spec_name: str, seed: int, out_dir: str, agent: Dict[str, Any], co_params: Dict[str, Any]) -> Dict[str, Any]:
    params = dict(agent.get("params", {}))
    if str(agent.get("type", "")).lower() == "co":
        params = dict(co_params)
    return {
        "seed": int(seed),
        "out_dir": out_dir,
        "spec": {"name": spec_name, "params": {"seed": int(seed)}},
        "agent": {"type": str(agent.get("type")), "params": params},
        "log_every": 10,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=str, default="outputs/latent_mechanism_first_run_v1.json")
    args = ap.parse_args()
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    co_params = _load_co_full_params()
    rows: List[Dict[str, Any]] = []
    tmp_root = Path(tempfile.mkdtemp(prefix="latent_mech_run_"))
    for spec_name in SPECS:
        for seed in SEEDS:
            for agent in AGENTS:
                out_dir = tmp_root / spec_name / f"seed{seed}" / str(agent['type'])
                cfg = _cfg_dict(spec_name, seed, str(out_dir), agent, co_params)
                cfg_path = out_dir / "cfg.json"
                out_dir.mkdir(parents=True, exist_ok=True)
                cfg_path.write_text(json.dumps(cfg, indent=2), encoding="utf-8")
                summary = run_cfg(str(cfg_path))
                rows.append({"spec": spec_name, "seed": seed, "agent": agent["type"], **summary})
    by_spec: Dict[str, Dict[str, Dict[str, float]]] = {}
    for spec_name in SPECS:
        by_spec[spec_name] = {}
        for agent in ["random", "heuristic", "co"]:
            subset = [r for r in rows if r["spec"] == spec_name and r["agent"] == agent]
            by_spec[spec_name][agent] = {
                "success_rate": mean([float(r["success"]) for r in subset]) if subset else 0.0,
                "mean_reward": mean([float(r["mean_reward"]) for r in subset]) if subset else 0.0,
                "mean_steps": mean([float(r["steps"]) for r in subset]) if subset else 0.0,
                "mean_wrong_count": mean([float(r["wrong_count"]) for r in subset]) if subset else 0.0,
            }
    out = {"study": "latent_mechanism_first_run_v1", "rows": rows, "summary": by_spec}
    out_path.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
