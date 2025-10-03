# experiments/suite_cli.py
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional

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
    """
    Launch a module with this interpreter. Minimal output; exceptions bubble up.
    """
    cmd = [sys.executable, "-m", mod, *args]
    subprocess.run(cmd, check=True)


def _write_tmp_yaml(obj: Dict[str, Any], path: Path) -> None:
    _ensure_dir(path.parent)
    path.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")

def _summarize(suite_root: Path, families: List[str]) -> None:
    try:
        from experiments.plotting.main import summarize_families
        summarize_families(suite_root, families)
    except Exception as e:
        print(f"[warn] plotting failed: {e}", file=sys.stderr)

# -------------------
# Bandit executor
# -------------------

def _suite_bandit(out_root: Path, spec: Dict[str, Any]) -> None:
    problems: List[Dict[str, Any]] = list(spec.get("problems", []))
    for pr in problems:
        mode= str(pr.get("mode", "unnamed"))
        env = dict(pr.get("env", {}))
        seeds: List[int] = list(pr.get("seeds", [7]))
        agents: List[Any] = list(pr.get("agents", [{"type": "ucb1"}]))

        for seed in seeds:
            for agent in agents:
                # agent can be "ucb1" or {"type":"ucb1","params":{...}}
                if isinstance(agent, str):
                    agent_type = agent.lower()
                    agent_params = {}
                else:
                    agent_type = str(agent.get("type", "ucb1")).lower()
                    agent_params = dict(agent.get("params", {}))

                # Build a per-run config for the bandit runner.
                # bandit_runner supports: env.probs, env.horizon, agent.type, agent.params.epsilon (for epsgreedy), seed, out
                cfg = {
                    "env": {
                        "probs": list(env.get("probs", [0.1, 0.2, 0.8])),
                        "horizon": int(env.get("horizon", 2000)),
                    },
                    "agent": {
                        "type": agent_type,
                        "params": agent_params,  # HAQ params may be ignored by current runner; harmless
                    },
                    "seed": int(seed),
                    # The runner writes directly here; no post-copy.
                    "out": str(out_root / "bandit" / mode/ f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "bandit" / mode/ f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                # Minimal status line (non-spammy)
                print(f"[bandit] {mode} :: agent={agent_type} seed={seed}")
                _run_module("experiments.runners.bandit_runner", "--config", str(tmp))


# -------------------
# Maze executor
# -------------------

def _suite_maze(out_root: Path, spec: Dict[str, Any]) -> None:
    envs: List[Dict[str, Any]] = list(spec.get("envs", []))
    for envspec in envs:
        mode= str(envspec.get("mode", "default"))
        env_cfg = dict(envspec.get("env", {}))  # e.g., {"spec_path": None}
        episodes = int(envspec.get("episodes", 5))
        seeds: List[int] = list(envspec.get("seeds", [7]))
        agents: List[Any] = list(envspec.get("agents", [{"type": "bfs"}]))

        # The maze_runner accepts env via config (spec_path) and agent via CLI arg.
        # We write a small config per seed that includes the env + episodes + out.
        for seed in seeds:
            for agent in agents:
                if isinstance(agent, str):
                    agent_type = agent.lower()
                    agent_params = {}
                else:
                    agent_type = str(agent.get("type", "bfs")).lower()
                    agent_params = dict(agent.get("params", {}))  # currently unused; harmless

                env_params = dict(env_cfg.get("params", {})) if isinstance(env_cfg.get("params"), dict) else {}
                env_params.setdefault("width", 5)
                env_params.setdefault("height", 5)
                env_params["seed"] = int(seed)

                cfg = {
                    "env": {
                        # allow null/absent spec_path → internal default 5x5
                        "spec_path": env_cfg.get("spec_path", None),
                        "params": env_params,
                    },
                    "episodes": int(episodes),
                    "seed": int(seed),
                    "out": str(out_root / "maze" / mode/ f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "maze" / mode/ f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                print(f"[maze] {mode} :: agent={agent_type} seed={seed}")
                # Pass agent on CLI, env via config, and force out to align with cfg.out
                _run_module(
                    "experiments.runners.maze_runner",
                    "--config", str(tmp),
                    "--agent", agent_type,
                    "--episodes", str(episodes),
                    "--out", cfg["out"],
                )


# -------------------
# Renewal executor
# -------------------

def _suite_renewal(out_root: Path, spec: Dict[str, Any]) -> None:
    instances: List[Dict[str, Any]] = list(spec.get("instances", []))
    for inst in instances:
        mode= str(inst.get("mode", "inst"))
        env = dict(inst.get("env", {}))  # A, L_win, p_ren, p_noise, T_max
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
                    agent_params = dict(agent.get("params", {}))  # HAQ params currently ignored by runner

                # renewal_runner expects "type": last | phase | ngram | haq
                cfg = {
                    "seed": int(seed),
                    "steps": int(steps),
                    "type": agent_type,  # maps directly
                    "env": {
                        "A": int(env.get("A", 8)),
                        "L_win": int(env.get("L_win", 6)),
                        "p_ren": float(env.get("p_ren", 0.02)),
                        "p_noise": float(env.get("p_noise", 0.0)),
                        "T_max": int(env.get("T_max", steps)),
                    },
                    "out_dir": str(out_root / "renewal" / mode/ f"{agent_type}_s{seed}"),
                }
                tmp = out_root / "tmp" / "renewal" / mode/ f"{agent_type}_s{seed}.yaml"
                _write_tmp_yaml(cfg, tmp)

                print(f"[renewal] {mode} :: agent={agent_type} seed={seed}")
                _run_module("experiments.runners.renewal_runner", "--config", str(tmp))


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

    _summarize(out_root, fams)

    print(json.dumps({"suite_out": str(out_root)}))


if __name__ == "__main__":
    main()
