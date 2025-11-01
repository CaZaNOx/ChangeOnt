# experiments/cli.py
from __future__ import annotations
import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Dict, Any, List, Iterable

# --- tiny YAML loader ---------------------------------------------------------
def _load_cfg(path: Path) -> Dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text) or {}
    except Exception:
        data = json.loads(text)
    if not isinstance(data, dict):
        raise ValueError(f"Config must be a mapping at root: {path}")
    return data

# --- safe run of python -m module --------------------------------------------
def _run_module(mod: str, *args: str) -> None:
    cmd = [sys.executable, "-m", mod, *args]
    subprocess.run(cmd, check=True)

# --- helpers to materialize temp runner configs -------------------------------
def _tmp_write(obj: Dict[str, Any], where: Path) -> Path:
    where.parent.mkdir(parents=True, exist_ok=True)
    p = where / "_tmp.yaml"
    try:
        import yaml  # type: ignore
        p.write_text(yaml.safe_dump(obj, sort_keys=False), encoding="utf-8")
    except Exception:
        p.write_text(json.dumps(obj, indent=2), encoding="utf-8")
    return p

# --- BANDIT orchestration -----------------------------------------------------
def _run_bandit_family(suite_root: Path, spec: Dict[str, Any]) -> None:
    fam_root = suite_root / "bandit"
    fam_root.mkdir(parents=True, exist_ok=True)

    problems = spec.get("problems", {})
    seeds: List[int] = list(spec.get("seeds", [1]))
    agents: List[str] = list(spec.get("agents", ["ucb1"]))

    for prob_name, prob_cfg in problems.items():
        prob_dir = fam_root / str(prob_name)
        prob_dir.mkdir(parents=True, exist_ok=True)

        probs = prob_cfg.get("probs", [0.1, 0.2, 0.8])
        horizon = int(prob_cfg.get("horizon", 2000))

        for agent in agents:
            for seed in seeds:
                run_dir = prob_dir / f"{agent}_s{seed}"
                run_dir.mkdir(parents=True, exist_ok=True)

                # bandit_runner expects:
                # {
                #   "env": {"probs":[...], "horizon": int},
                #   "agent": {"type": "ucb1"|"epsgreedy"|"haq", "params": {...}},
                #   "seed": int,
                #   "out": <dir>
                # }
                agent_type = agent
                agent_params: Dict[str, Any] = {}

                # map a few friendly aliases to your runner’s types
                if agent in ("haq_base", "haq_fastema", "haq_slowema"):
                    agent_type = "haq"
                    if agent == "haq_fastema":
                        agent_params["ema_alpha"] = 0.3
                    elif agent == "haq_slowema":
                        agent_params["ema_alpha"] = 0.03
                    else:
                        agent_params["ema_alpha"] = 0.1
                elif agent in ("ucb", "ucb1"):
                    agent_type = "ucb1"
                elif agent in ("eps", "epsilon_greedy", "epsgreedy"):
                    agent_type = "epsgreedy"

                cfg = {
                    "env": {"probs": list(probs), "horizon": int(horizon)},
                    "agent": {"type": agent_type, "params": agent_params},
                    "seed": int(seed),
                    "out": str(run_dir),
                }
                tmp_cfg = _tmp_write(cfg, run_dir)
                _run_module("experiments.runners.bandit_runner", "--config", str(tmp_cfg))

# --- MAZE orchestration -------------------------------------------------------
def _run_maze_family(suite_root: Path, spec: Dict[str, Any]) -> None:
    fam_root = suite_root / "maze"
    fam_root.mkdir(parents=True, exist_ok=True)

    envs = spec.get("envs", {})
    agents: List[str] = list(spec.get("agents", ["bfs"]))

    for env_name, env_cfg in envs.items():
        env_dir = fam_root / str(env_name)
        env_dir.mkdir(parents=True, exist_ok=True)

        episodes = int(env_cfg.get("episodes", 5))
        spec_path = env_cfg.get("spec_path", None)

        for agent in agents:
            run_dir = env_dir / agent
            run_dir.mkdir(parents=True, exist_ok=True)

            # maze_runner expects either CLI flags or a config:
            # {
            #   "env": {"spec_path": "..."},
            #   "episodes": int,
            #   "out": <dir>,
            #   "agent": {"type": "bfs" | "haq", "params": {...}}  # (we added "haq")
            # }
            agent_type = agent
            agent_params: Dict[str, Any] = {}
            if agent in ("bfs",):
                agent_type = "bfs"
            elif agent in ("haq", "haq_maze"):
                agent_type = "haq"  # HAQ Maze adapter in agents.co.agent_maze

            cfg = {
                "env": {"spec_path": spec_path},
                "episodes": int(episodes),
                "out": str(run_dir),
                "agent": {"type": agent_type, "params": agent_params},
            }
            tmp_cfg = _tmp_write(cfg, run_dir)
            _run_module("experiments.runners.maze_runner", "--config", str(tmp_cfg))

# --- RENEWAL orchestration ----------------------------------------------------
def _run_renewal_family(suite_root: Path, spec: Dict[str, Any]) -> None:
    fam_root = suite_root / "renewal"
    fam_root.mkdir(parents=True, exist_ok=True)

    instances = spec.get("instances", {})
    for inst_name, inst_cfg in instances.items():
        inst_dir = fam_root / str(inst_name)
        inst_dir.mkdir(parents=True, exist_ok=True)

        env_dict = dict(inst_cfg.get("env", {}))
        agents: List[str] = list(inst_cfg.get("agents", ["last", "phase", "ngram"]))
        seeds: List[int] = list(inst_cfg.get("seeds", [7]))

        for agent in agents:
            for seed in seeds:
                run_dir = inst_dir / f"{agent}_s{seed}"
                run_dir.mkdir(parents=True, exist_ok=True)

                # renewal_runner config:
                # {
                #   "seed": int,
                #   "steps": int,
                #   "mode": "last"|"phase"|"ngram"|"haq",
                #   "env": {...},
                #   "out_dir": <dir>
                # }
                mode = agent
                steps = int(env_dict.get("T_max", 1000))
                if agent in ("haq_base", "haq_L6_e01", "haq_L6_e03", "haq_L10_e01"):
                    mode = "haq"  # HAQ agent inside renewal runner
                cfg = {
                    "seed": int(seed),
                    "steps": steps,
                    "mode": mode,
                    "env": env_dict,
                    "out_dir": str(run_dir),
                }
                tmp_cfg = _tmp_write(cfg, run_dir)
                _run_module("experiments.runners.renewal_runner", "--config", str(tmp_cfg))

# --- Plotting hook (always on after runs) -------------------------------------
def _summarize(suite_root: Path, families: List[str]) -> None:
    try:
        from experiments.plotting.main import summarize_families
        summarize_families(suite_root, families)
    except Exception as e:
        print(f"[warn] plotting failed: {e}", file=sys.stderr)

# --- CLI ----------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser(description="Unified runner: bandit/maze/renewal with auto summaries.")
    sub = ap.add_subparsers(dest="cmd", required=True)

    runp = sub.add_parser("run", help="run a family or all")
    runp.add_argument("target", choices=["bandit", "maze", "renewal", "all"])
    runp.add_argument("--config", type=str, required=True, help="suite config (YAML/JSON)")
    runp.add_argument("--out-root", type=str, default="outputs/suite", help="output root directory")

    args = ap.parse_args()

    if args.cmd == "run":
        cfg_path = Path(args.config)
        suite_root = Path(args.out_root)
        data = _load_cfg(cfg_path)

        families: List[str]
        if args.target == "all":
            families = ["bandit", "maze", "renewal"]
        else:
            families = [args.target]

        if "bandit" in families:
            spec = data.get("bandit", {})
            if spec:
                _run_bandit_family(suite_root, spec)

        if "maze" in families:
            spec = data.get("maze", {})
            if spec:
                _run_maze_family(suite_root, spec)

        if "renewal" in families:
            spec = data.get("renewal", {})
            if spec:
                _run_renewal_family(suite_root, spec)

        _summarize(suite_root, families)

if __name__ == "__main__":
    main()
