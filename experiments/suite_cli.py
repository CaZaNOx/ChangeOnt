# experiments/suite_cli.py
# Wire per-mode, per-family, and suite-level summaries exactly once, in order.
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

try:
    import yaml  # type: ignore
except Exception as e:
    raise SystemExit("PyYAML is required: pip install pyyaml") from e

# -------------------
# Utilities
# -------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(data, dict):
        raise ValueError(f"YAML root must be a mapping: {path}")
    return data

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def _run_module(mod: str, *args: str) -> None:
    cmd = [sys.executable, "-m", mod, *args]
    subprocess.run(cmd, check=True)

def _write_tmp_yaml(obj: Dict[str, Any], path: Path) -> None:
    _ensure_dir(path.parent)
    path.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

# Central summary wrappers
from experiments.plotting.main import (
    summarize_bandit_mode,
    summarize_maze_mode,
    summarize_renewal_mode,
    summarize_family,
    summarize_suite,
)

# -------------------
# Bandit executor
# -------------------

def _suite_bandit(out_root: Path, spec: Dict[str, Any]) -> None:
    problems: List[Dict[str, Any]] = list(spec.get("problems", []))
    fam_dir = out_root / "bandit"

    for pr in problems:
        mode = str(pr.get("mode", "unnamed"))
        mode_dir = fam_dir / mode
        env = dict(pr.get("env", {}))
        seeds: List[int] = list(pr.get("seeds", [7]))
        agents: List[Any] = list(pr.get("agents", [{"type": "ucb1"}]))

        for seed in seeds:
            for agent in agents:
                if isinstance(agent, str):
                    agent_type = agent.lower()
                    agent_params = {}
                else:
                    agent_type = str(agent.get("type", "ucb1")).lower()
                    agent_params = dict(agent.get("params", {}))

                cfg = {
                    "env": {
                        "probs": list(env.get("probs", [0.1, 0.2, 0.8])),
                        "horizon": int(env.get("horizon", 2000)),
                    },
                    "agent": {"type": agent_type, "params": agent_params},
                    "seed": int(seed),
                    "out": str(out_root / "bandit" / mode / f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "bandit" / mode / f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                print(f"[bandit] {mode} :: agent={agent_type} seed={seed}")
                _run_module("experiments.runners.bandit_runner", "--config", str(tmp))

        # Per-mode summary (right after mode finishes)
        summarize_bandit_mode(mode_dir)

    # Family aggregation (once)
    summarize_family(out_root, "bandit")

# -------------------
# Maze executor
# -------------------

def _suite_maze(out_root: Path, spec: Dict[str, Any]) -> None:
    envs: List[Dict[str, Any]] = list(spec.get("envs", []))
    fam_dir = out_root / "maze"

    for envspec in envs:
        mode = str(envspec.get("mode", "default"))
        mode_dir = fam_dir / mode
        env_cfg = dict(envspec.get("env", {}))
        episodes = int(envspec.get("episodes", 5))
        seeds: List[int] = list(envspec.get("seeds", [7]))
        agents: List[Any] = list(envspec.get("agents", [{"type": "bfs"}]))

        for seed in seeds:
            for agent in agents:
                if isinstance(agent, str):
                    agent_type = agent.lower()
                    agent_params = {}
                else:
                    agent_type = str(agent.get("type", "bfs")).lower()
                    agent_params = dict(agent.get("params", {}))

                env_params = dict(env_cfg.get("params", {})) if isinstance(env_cfg.get("params"), dict) else {}
                env_params.setdefault("width", 5)
                env_params.setdefault("height", 5)
                env_params["seed"] = int(seed)

                cfg = {
                    "env": {"spec_path": env_cfg.get("spec_path", None), "params": env_params},
                    "episodes": int(episodes),
                    "seed": int(seed),
                    "out": str(out_root / "maze" / mode / f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "maze" / mode / f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                print(f"[maze] {mode} :: agent={agent_type} seed={seed}")
                _run_module(
                    "experiments.runners.maze_runner",
                    "--config", str(tmp),
                    "--agent", agent_type,
                    "--episodes", str(episodes),
                    "--out", cfg["out"],
                )

        # Per-mode summary
        summarize_maze_mode(mode_dir)

    # Family aggregation
    summarize_family(out_root, "maze")

# -------------------
# Renewal executor
# -------------------

def _suite_renewal(out_root: Path, spec: Dict[str, Any]) -> None:
    instances: List[Dict[str, Any]] = list(spec.get("instances", []))
    fam_dir = out_root / "renewal"

    for inst in instances:
        mode = str(inst.get("mode", "inst"))
        mode_dir = fam_dir / mode
        env = dict(inst.get("env", {}))
        steps = int(inst.get("steps", env.get("T_max", 1000)))
        seeds: List[int] = list(inst.get("seeds", [7]))
        agents: List[Any] = list(inst.get("agents", [{"type": "last"}]))

        for seed in seeds:
            for agent in agents:
                if isinstance(agent, str):
                    agent_type = agent.lower()
                    agent_params = {}
                else:
                    agent_type = str(agent.get("type", "last")).lower()
                    agent_params = dict(agent.get("params", {}))

                cfg = {
                    "seed": int(seed),
                    "steps": int(steps),
                    "agent": {                           # <-- write agent exactly like bandit/maze
                        "type": agent_type,
                        "params": agent_params,
                    },
                    "env": {
                        "A": int(env.get("A", 8)),
                        "L_win": int(env.get("L_win", 6)),
                        "p_ren": float(env.get("p_ren", 0.02)),
                        "p_noise": float(env.get("p_noise", 0.0)),
                        "T_max": int(env.get("T_max", steps)),
                    },
                    "out_dir": str(out_root / "renewal" / mode / f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "renewal" / mode / f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                print(f"[renewal] {mode} :: agent={agent_type} seed={seed}")
                _run_module("experiments.runners.renewal_runner", "--config", str(tmp))

        # Per-mode summary
        summarize_renewal_mode(mode_dir)

    # Family aggregation
    summarize_family(out_root, "renewal")

# -------------------
# CLI
# -------------------

@dataclass
class SuiteCfg:
    out_root: Path
    families: Dict[str, Any]

def main() -> None:
    ap = argparse.ArgumentParser(description="Run a multi-family suite (STOA + CO) from one YAML.")

    cfg_raw = _load_yaml(Path("experiments/configs/suite_all.yaml"))
    out_root = Path(cfg_raw.get("out_root", "outputs/suite"))
    _ensure_dir(out_root)

    fams = dict(cfg_raw.get("families", {}))

    if "maze" in fams:
        _suite_maze(out_root, dict(fams["maze"]))
    if "renewal" in fams:
        _suite_renewal(out_root, dict(fams["renewal"]))
    if "bandit" in fams:
        _suite_bandit(out_root, dict(fams["bandit"]))

    # OPTIONAL: overall suite summary (CSV only)
    present = [f for f in ("bandit", "maze", "renewal") if f in fams]
    summarize_suite(out_root, present)

    print(json.dumps({"suite_out": str(out_root)}))

if __name__ == "__main__":
    main()
