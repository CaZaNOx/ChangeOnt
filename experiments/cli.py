# PATH: experiments/cli.py
from __future__ import annotations
import argparse
import json
from pathlib import Path
from typing import List, Dict, Any, Optional

# Runner entry-points
from experiments.runners.bandit_runner import main as bandit_main
from experiments.runners.maze_runner   import main as maze_main
from experiments.runners.renewal_runner import main as renewal_main

# Shared evaluator (assumed present)
from experiments.eval import eval_bandit, eval_maze, eval_renewal


# ---------------------------
# Helpers
# ---------------------------

def _split_agents(arg: str) -> List[str]:
    return [a.strip().lower() for a in arg.split(",") if a.strip()]

def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)

def _task_base_dir(base_out_root: Path, task_slug: str) -> Path:
    """
    Respect the configured base output root; place all per-agent runs under <root>/<task>_cli.
    If base already ends with '<task>_cli', use it directly.
    """
    suffix = f"{task_slug}_cli"
    if base_out_root.name.lower() == suffix.lower():
        base = base_out_root
    else:
        base = base_out_root / suffix
    _ensure_dir(base)
    return base

def _read_config_to_dict(path: Optional[Path]) -> Dict[str, Any]:
    if not path:
        return {}
    text = path.read_text(encoding="utf-8")
    # try JSON
    try:
        return json.loads(text) or {}
    except Exception:
        pass
    # try YAML
    try:
        import yaml  # type: ignore
        data = yaml.safe_load(text)
        return data or {}
    except Exception:
        return {}

def _write_yaml_or_json(path: Path, data: Dict[str, Any]) -> None:
    try:
        import yaml  # type: ignore
        path.write_text(yaml.safe_dump(data, sort_keys=False), encoding="utf-8")
        return
    except Exception:
        pass
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------
# BANDIT
# ---------------------------

def _bandit_base_from(cfg: Dict[str, Any], cli_out: Optional[str]) -> Path:
    # Config wins if present
    if "out" in cfg and cfg["out"]:
        return Path(str(cfg["out"]))
    # Else CLI fallback (or "outputs")
    return Path(cli_out or "outputs")

def cmd_bandit(args: argparse.Namespace) -> None:
    agents = _split_agents(args.agents) if args.agents else ["ucb1"]
    cfg_path = Path(args.config) if args.config else None
    cfg_dict = _read_config_to_dict(cfg_path)

    # Where to place all per-agent runs
    base_root = _bandit_base_from(cfg_dict, args.out)
    base = _task_base_dir(base_root, "bandit")

    run_dirs: List[Path] = []

    for agent in agents:
        run_dir = base / f"bandit_{agent}"
        _ensure_dir(run_dir)

        if cfg_path:
            # Respect the config: clone it, only change 'out' and **force the agent type** per run.
            cfg_copy = dict(cfg_dict)
            cfg_copy["out"] = run_dir.as_posix()
            params = {}
            if isinstance(cfg_dict.get("agent"), dict):
                params = dict(cfg_dict["agent"].get("params", {}))
            cfg_copy["agent"] = {"type": agent, "params": params}
            tmp_cfg = run_dir / f"_auto_{agent}.yaml"
            _write_yaml_or_json(tmp_cfg, cfg_copy)
            cli = ["--config", str(tmp_cfg)]
        else:
            # No config: supply minimal CLI; still write into agent subfolder
            cli = ["--agent", agent, "--out", str(run_dir)]
            if args.horizon is not None:
                cli += ["--horizon", str(args.horizon)]
            if args.probs:
                cli += ["--probs", args.probs]
            if args.seed is not None:
                cli += ["--seed", str(args.seed)]

        import sys
        old = sys.argv
        try:
            sys.argv = ["bandit_runner.py"] + cli
            bandit_main()
        finally:
            sys.argv = old

        run_dirs.append(run_dir)

    # Eval bundle
    eval_dir = base / "eval"
    _ensure_dir(eval_dir)
    res = eval_bandit(run_dirs, eval_dir)

    print(json.dumps({
        "bandit_runs": [str(p) for p in run_dirs],
        "eval": {"dir": str(eval_dir), **res}
    }))


# ---------------------------
# MAZE
# ---------------------------

def _maze_base_from(cfg: Dict[str, Any], cli_out: Optional[str]) -> Path:
    if "out" in cfg and cfg["out"]:
        return Path(str(cfg["out"]))
    return Path(cli_out or "outputs")

def cmd_maze(args: argparse.Namespace) -> None:
    agents = _split_agents(args.agents) if args.agents else ["bfs"]
    cfg_path = Path(args.config) if args.config else None
    cfg_dict = _read_config_to_dict(cfg_path)

    base_root = _maze_base_from(cfg_dict, args.out)
    base = _task_base_dir(base_root, "maze")

    run_dirs: List[Path] = []

    for agent in agents:
        if agent not in ("bfs", "haq"):
            raise SystemExit(f"maze: unknown agent '{agent}'")
        run_dir = base / f"maze_{agent}"
        _ensure_dir(run_dir)

        if cfg_path:
            cfg_copy = dict(cfg_dict)
            cfg_copy["out"] = run_dir.as_posix()
            # If your maze_runner reads agent from config, set it here:
            # (If maze_runner ignores agent in config, leave this harmlessly present)
            cfg_copy["agent"] = {"type": agent}
            tmp_cfg = run_dir / f"_auto_{agent}.yaml"
            _write_yaml_or_json(tmp_cfg, cfg_copy)
            cli = ["--config", str(tmp_cfg)]
        else:
            cli = ["--out", str(run_dir)]
            if args.episodes is not None:
                cli += ["--episodes", str(args.episodes)]
            # NOTE: your maze_runner currently hardwires BFS; ensure it reads `agent` from config if you want HAQ here.

        import sys
        old = sys.argv
        try:
            sys.argv = ["maze_runner.py"] + cli
            maze_main()
        finally:
            sys.argv = old

        run_dirs.append(run_dir)

    eval_dir = base / "eval"
    _ensure_dir(eval_dir)
    res = eval_maze(run_dirs, eval_dir)

    print(json.dumps({
        "maze_runs": [str(p) for p in run_dirs],
        "eval": {"dir": str(eval_dir), **res}
    }))


# ---------------------------
# RENEWAL
# ---------------------------

def _renewal_base_from(cfg: Dict[str, Any], cli_out: Optional[str]) -> Path:
    # Renewal uses out_dir in config
    if "out_dir" in cfg and cfg["out_dir"]:
        return Path(str(cfg["out_dir"]))
    # Some older configs may still use 'out'
    if "out" in cfg and cfg["out"]:
        return Path(str(cfg["out"]))
    return Path(cli_out or "outputs")

def _compose_renewal_cfg(base_cfg: Dict[str, Any], mode: str, out_dir: Path,
                         steps: Optional[int], seed: Optional[int]) -> Dict[str, Any]:
    cfg = dict(base_cfg) if base_cfg else {}
    cfg["mode"] = mode
    cfg["out_dir"] = out_dir.as_posix()
    if steps is not None:
        cfg["steps"] = int(steps)
    if seed is not None:
        cfg["seed"] = int(seed)
    if "env" not in cfg or cfg["env"] is None:
        cfg["env"] = {"A": 8, "L_win": 6, "p_ren": 0.02, "p_noise": 0.0, "T_max": 1000}
    return cfg

def cmd_renewal(args: argparse.Namespace) -> None:
    agents = _split_agents(args.agents) if args.agents else ["phase"]
    cfg_path = Path(args.config) if args.config else None
    cfg_dict = _read_config_to_dict(cfg_path)

    base_root = _renewal_base_from(cfg_dict, args.out)
    base = _task_base_dir(base_root, "renewal")

    run_dirs: List[Path] = []

    for agent in agents:
        run_dir = base / f"renewal_{agent}"
        _ensure_dir(run_dir)

        # Always write a per-agent config that only changes mode/out_dir (+ steps/seed if provided)
        merged = _compose_renewal_cfg(cfg_dict, mode=agent, out_dir=run_dir, steps=args.steps, seed=args.seed)
        tmp_cfg = run_dir / f"_auto_{agent}.yaml"
        _write_yaml_or_json(tmp_cfg, merged)
        cli = ["--config", str(tmp_cfg)]

        import sys
        old = sys.argv
        try:
            sys.argv = ["renewal_runner.py"] + cli
            renewal_main()
        finally:
            sys.argv = old

        run_dirs.append(run_dir)

    eval_dir = base / "eval"
    _ensure_dir(eval_dir)
    res = eval_renewal(run_dirs, eval_dir)

    print(json.dumps({
        "renewal_runs": [str(p) for p in run_dirs],
        "eval": {"dir": str(eval_dir), **res}
    }))


# ---------------------------
# Explicit eval subcommand
# ---------------------------

def cmd_eval(args: argparse.Namespace) -> None:
    task = args.task.lower()
    run_dirs = [Path(p) for p in args.runs.split(",") if p.strip()]
    out_dir = Path(args.out)
    _ensure_dir(out_dir)

    if task == "bandit":
        res = eval_bandit(run_dirs, out_dir)
    elif task == "maze":
        res = eval_maze(run_dirs, out_dir)
    elif task == "renewal":
        res = eval_renewal(run_dirs, out_dir)
    else:
        raise SystemExit(f"unknown task: {task}")

    print(json.dumps({"eval": {"dir": str(out_dir), **res}}))


# ---------------------------
# Main
# ---------------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Unified CLI for running agents with config-owned outputs + shared evals")
    sub = ap.add_subparsers(dest="cmd", required=True)

    # bandit
    ap_b = sub.add_parser("bandit")
    ap_b.add_argument("--agents",  type=str, default="ucb1", help="comma-separated: ucb1,epsgreedy,haq")
    ap_b.add_argument("--config",  type=str, default=None,    help="JSON/YAML config; its 'out' wins over --out")
    ap_b.add_argument("--out",     type=str, default="outputs", help="base out if config has no 'out'")
    ap_b.add_argument("--probs",   type=str, default=None)
    ap_b.add_argument("--horizon", type=int, default=None)
    ap_b.add_argument("--seed",    type=int, default=7)
    ap_b.set_defaults(func=cmd_bandit)

    # maze
    ap_m = sub.add_parser("maze")
    ap_m.add_argument("--agents",   type=str, default="bfs",     help="comma-separated: bfs,haq")
    ap_m.add_argument("--config",   type=str, default=None,      help="JSON/YAML config; its 'out' wins over --out")
    ap_m.add_argument("--out",      type=str, default="outputs", help="base out if config has no 'out'")
    ap_m.add_argument("--episodes", type=int, default=None)
    ap_m.add_argument("--seed",     type=int, default=7)
    ap_m.set_defaults(func=cmd_maze)

    # renewal
    ap_r = sub.add_parser("renewal")
    ap_r.add_argument("--agents", type=str, default="phase",     help="comma-separated: last,phase,ngram,haq")
    ap_r.add_argument("--config", type=str, default=None,        help="JSON/YAML; its 'out_dir' (or 'out') wins over --out")
    ap_r.add_argument("--out",    type=str, default="outputs",   help="base out if config has no out_dir/out")
    ap_r.add_argument("--steps",  type=int, default=None)
    ap_r.add_argument("--seed",   type=int, default=7)
    ap_r.set_defaults(func=cmd_renewal)

    # eval
    ap_e = sub.add_parser("eval")
    ap_e.add_argument("task", type=str, choices=["bandit","maze","renewal"])
    ap_e.add_argument("--runs", type=str, required=True, help="comma-separated run dirs")
    ap_e.add_argument("--out",  type=str, default="outputs/cli_eval")
    ap_e.set_defaults(func=cmd_eval)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
