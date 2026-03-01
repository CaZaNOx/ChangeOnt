# experiments/suite_cli.py
# Suite orchestration with canonical job configs and optional parallel execution.

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

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


def _slug(s: str) -> str:
    s = str(s)
    s = re.sub(r"\s+", "_", s.strip())
    s = re.sub(r"[^a-zA-Z0-9_.-]+", "-", s)
    return s[:80] if len(s) > 80 else s


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


# Central summary wrappers
from experiments.plotting.main import (
    summarize_bandit_mode,
    summarize_maze_mode,
    summarize_renewal_mode,
    summarize_family,
    summarize_suite,
)

# ---- CO manifest loader / injector ------------------------------------------

def _load_co_manifest(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    with p.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    agents = data.get("co_agents", data.get("variants", []))
    data["_co_agents_norm"] = agents if isinstance(agents, list) else []
    data["_apply_all_families"] = bool(data.get("apply_to_all_families", True))
    data["_apply_all_modes"] = bool(data.get("apply_to_all_modes", True))
    return data


def _append_agents(dst_list: list, extra: list) -> list:
    """Append agents, avoiding duplicates by (type, name-or-params-hash)."""
    if not extra:
        return dst_list
    out = list(dst_list or [])

    def _key(d: dict) -> tuple:
        t = d.get("type")
        nm = d.get("name")
        return (t, nm) if nm is not None else (t, json.dumps(d.get("params", {}), sort_keys=True))

    seen = {_key(a) for a in out if isinstance(a, dict)}
    for e in extra:
        if isinstance(e, dict):
            if _key(e) not in seen:
                out.append(e)
                seen.add(_key(e))
    return out


def _inject_co_everywhere(suite_cfg: dict, co_manifest: dict) -> dict:
    """Append CO agents to every family/mode in suite_cfg when apply-all flags permit."""
    co_agents = co_manifest.get("_co_agents_norm", [])
    if not co_agents:
        return suite_cfg
    if not co_manifest.get("_apply_all_families", True):
        return suite_cfg
    if not co_manifest.get("_apply_all_modes", True):
        return suite_cfg
    out = dict(suite_cfg)
    fam = out.get("families", {})

    # Bandit: problems[*].agents
    b = fam.get("bandit")
    if b and "problems" in b:
        for prob in b["problems"]:
            prob["agents"] = _append_agents(prob.get("agents", []), co_agents)

    # Maze: envs[*].agents
    m = fam.get("maze")
    if m and "envs" in m:
        for env in m["envs"]:
            env["agents"] = _append_agents(env.get("agents", []), co_agents)

    # Renewal: instances[*].agents
    r = fam.get("renewal")
    if r and "instances" in r:
        for inst in r["instances"]:
            inst["agents"] = _append_agents(inst.get("agents", []), co_agents)

    return out


FAMILY_ORDER = ["maze", "renewal", "bandit"]


@dataclass
class SuiteJob:
    family: str
    mode: str
    seed: int
    agent_type: str
    agent_name: Optional[str]
    agent_tag: str
    runner_module: str
    out_dir: Path
    config_path: Path
    env: Dict[str, Any]
    agent: Dict[str, Any]
    run: Dict[str, Any]
    logging: Dict[str, bool]


# -------------------
# Job config + execution
# -------------------

def _build_job_config(job: SuiteJob) -> Dict[str, Any]:
    job_payload = {
        "family": job.family,
        "mode": job.mode,
        "seed": job.seed,
        "agent_id": job.agent_tag,
        "agent_type": job.agent_type,
        "agent_name": job.agent_name,
        "out_dir": job.out_dir.as_posix(),
        "runner": job.runner_module,
    }

    config = {
        "job": job_payload,
        "env": dict(job.env),
        "agent": dict(job.agent),
        "run": dict(job.run),
        "logging": dict(job.logging),
    }
    return config


def _validate_job_config(cfg: Dict[str, Any]) -> None:
    job = cfg.get("job", {})
    env = cfg.get("env", {})
    agent = cfg.get("agent", {})
    run = cfg.get("run", {})
    logging = cfg.get("logging", {})

    missing = []
    for key in ("job", "env", "agent", "run", "logging"):
        if key not in cfg:
            missing.append(key)
    if missing:
        raise ValueError(f"missing top-level keys: {missing}")

    for k in ("family", "mode", "seed", "out_dir"):
        if k not in job:
            raise ValueError(f"missing job.{k}")
    if "kind" not in env:
        raise ValueError("missing env.kind")
    if "type" not in agent:
        raise ValueError("missing agent.type")

    for k in ("steps", "episodes", "horizon"):
        if k not in run:
            raise ValueError(f"missing run.{k}")
    for k in ("write_metrics", "write_budget", "write_plot"):
        if k not in logging:
            raise ValueError(f"missing logging.{k}")


def _write_job_config(job: SuiteJob) -> None:
    cfg = _build_job_config(job)
    _validate_job_config(cfg)
    _write_tmp_yaml(cfg, job.config_path)


def _write_job_state(path: Path, status: str, job: SuiteJob, started_at: str, ended_at: str, error: Optional[str]) -> None:
    payload = {
        "family": job.family,
        "mode": job.mode,
        "seed": job.seed,
        "agent_tag": job.agent_tag,
        "runner": job.runner_module,
        "out_dir": job.out_dir.as_posix(),
        "status": status,
        "started_at": started_at,
        "ended_at": ended_at,
        "error": error,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def _validate_run_outputs(out_dir: Path) -> bool:
    metrics_ok = (out_dir / "metrics.jsonl").exists()
    budget_ok = (out_dir / "budget.csv").exists()
    manifest_ok = (out_dir / "run_manifest.json").exists()
    return metrics_ok and budget_ok and manifest_ok


def _run_job(job: SuiteJob, continue_on_failure: bool) -> bool:
    state_path = job.out_dir / "job_state.json"
    started_at = _now_iso()
    _write_job_state(state_path, "running", job, started_at, "", None)
    try:
        _run_module(job.runner_module, "--config", str(job.config_path))
        ended_at = _now_iso()
        ok = _validate_run_outputs(job.out_dir)
        status = "succeeded" if ok else "failed"
        err = None if ok else "missing_run_outputs"
        _write_job_state(state_path, status, job, started_at, ended_at, err)
        return ok
    except Exception as exc:
        ended_at = _now_iso()
        _write_job_state(state_path, "failed", job, started_at, ended_at, f"{type(exc).__name__}: {exc}")
        if not continue_on_failure:
            raise
        return False


def _dispatch_jobs(jobs: List[SuiteJob], max_workers: int, continue_on_failure: bool) -> List[bool]:
    if not jobs:
        return []
    results: List[bool] = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_job = {executor.submit(_run_job, job, continue_on_failure): job for job in jobs}
        for future in as_completed(future_to_job):
            try:
                success = future.result()
            except Exception:
                success = False
                if not continue_on_failure:
                    raise
            results.append(success)
    return results


def _write_failure_report(out_root: Path, jobs: List[SuiteJob]) -> None:
    summary_dir = out_root / "summary"
    _ensure_dir(summary_dir)
    report_path = summary_dir / "overall_failures.csv"
    rows: List[Dict[str, Any]] = []
    for job in jobs:
        state_path = job.out_dir / "job_state.json"
        status = "unknown"
        error = ""
        if state_path.exists():
            try:
                data = json.loads(state_path.read_text(encoding="utf-8"))
                status = str(data.get("status", status))
                error = str(data.get("error", "")) if data.get("error") else ""
            except Exception:
                status = "unknown"
        if status != "succeeded":
            rows.append({
                "family": job.family,
                "mode": job.mode,
                "seed": job.seed,
                "agent_tag": job.agent_tag,
                "status": status,
                "error": error,
            })
    with report_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["family", "mode", "seed", "agent_tag", "status", "error"])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


# -------------------
# Job builders
# -------------------

def _agent_fields(agent: Any) -> Tuple[str, Optional[str], Dict[str, Any]]:
    if isinstance(agent, str):
        return agent.lower(), None, {}
    atype = str(agent.get("type", "")).lower()
    aname = agent.get("name")
    aparams = dict(agent.get("params", {}))
    return atype, aname, aparams


def _agent_config(atype: str, aname: Optional[str], aparams: Dict[str, Any]) -> Dict[str, Any]:
    if atype == "co":
        return {"type": "co", "name": aname or "CO", "params": aparams}
    # STOA path
    return {"type": "stoa", "name": aname or atype, "params": aparams}


def _gather_bandit_jobs(out_root: Path, spec: Dict[str, Any]) -> Tuple[List[SuiteJob], Dict[str, Path], List[str]]:
    jobs: List[SuiteJob] = []
    mode_dirs: Dict[str, Path] = {}
    mode_order: List[str] = []
    fam_dir = out_root / "bandit"
    problems: List[Dict[str, Any]] = list(spec.get("problems", []))

    for pr in problems:
        mode = str(pr.get("mode", "unnamed"))
        if mode not in mode_order:
            mode_order.append(mode)
        mode_dirs[mode] = fam_dir / mode
        env = dict(pr.get("env", {}))
        seeds: List[int] = list(pr.get("seeds", [7]))
        agents: List[Any] = list(pr.get("agents", [{"type": "ucb1"}]))

        for seed in seeds:
            for agent in agents:
                atype, aname, aparams = _agent_fields(agent)
                tag = atype if not aname else f"{atype}_{_slug(aname)}"
                out_dir = fam_dir / mode / f"{tag}_s{seed}"
                cfg_path = out_root / "tmp" / "bandit" / mode / f"{tag}_s{seed}.yaml"

                env_payload = {
                    "kind": "bandit",
                    "spec": {},
                    "params": {
                        "probs": list(env.get("probs", [0.1, 0.2, 0.8])),
                        "horizon": int(env.get("horizon", 2000)),
                    },
                }
                agent_payload = _agent_config(atype, aname, aparams)
                run_payload = {"steps": None, "episodes": None, "horizon": int(env_payload["params"]["horizon"])}
                job = SuiteJob(
                    family="bandit",
                    mode=mode,
                    seed=int(seed),
                    agent_type=atype,
                    agent_name=aname,
                    agent_tag=tag,
                    runner_module="experiments.runners.bandit_runner",
                    out_dir=out_dir,
                    config_path=cfg_path,
                    env=env_payload,
                    agent=agent_payload,
                    run=run_payload,
                    logging={"write_metrics": True, "write_budget": True, "write_plot": True},
                )
                _write_job_config(job)
                print(f"[bandit] {mode} :: agent={tag} seed={seed}")
                jobs.append(job)
    return jobs, mode_dirs, mode_order


def _gather_maze_jobs(out_root: Path, spec: Dict[str, Any]) -> Tuple[List[SuiteJob], Dict[str, Path], List[str]]:
    jobs: List[SuiteJob] = []
    mode_dirs: Dict[str, Path] = {}
    mode_order: List[str] = []
    fam_dir = out_root / "maze"
    envs: List[Dict[str, Any]] = list(spec.get("envs", []))

    for envspec in envs:
        mode = str(envspec.get("mode", "default"))
        if mode not in mode_order:
            mode_order.append(mode)
        mode_dirs[mode] = fam_dir / mode
        env_cfg = dict(envspec.get("env", {}))
        episodes = int(envspec.get("episodes", 5))
        seeds: List[int] = list(envspec.get("seeds", [7]))
        agents: List[Any] = list(envspec.get("agents", [{"type": "bfs"}]))

        for seed in seeds:
            env_params = dict(env_cfg.get("params", {})) if isinstance(env_cfg.get("params"), dict) else {}
            env_params.setdefault("width", 5)
            env_params.setdefault("height", 5)
            env_params.setdefault("seed", int(seed))

            for agent in agents:
                atype, aname, aparams = _agent_fields(agent)
                tag = atype if not aname else f"{atype}_{_slug(aname)}"
                out_dir = fam_dir / mode / f"{tag}_s{seed}"
                cfg_path = out_root / "tmp" / "maze" / mode / f"{tag}_s{seed}.yaml"

                env_payload = {
                    "kind": "maze",
                    "spec": {"spec_path": env_cfg.get("spec_path")},
                    "params": env_params,
                }
                agent_payload = _agent_config(atype, aname, aparams)
                run_payload = {"steps": None, "episodes": episodes, "horizon": None}
                job = SuiteJob(
                    family="maze",
                    mode=mode,
                    seed=int(seed),
                    agent_type=atype,
                    agent_name=aname,
                    agent_tag=tag,
                    runner_module="experiments.runners.maze_runner",
                    out_dir=out_dir,
                    config_path=cfg_path,
                    env=env_payload,
                    agent=agent_payload,
                    run=run_payload,
                    logging={"write_metrics": True, "write_budget": True, "write_plot": True},
                )
                _write_job_config(job)
                print(f"[maze] {mode} :: agent={tag} seed={seed}")
                jobs.append(job)
    return jobs, mode_dirs, mode_order


def _gather_renewal_jobs(out_root: Path, spec: Dict[str, Any]) -> Tuple[List[SuiteJob], Dict[str, Path], List[str]]:
    jobs: List[SuiteJob] = []
    mode_dirs: Dict[str, Path] = {}
    mode_order: List[str] = []
    fam_dir = out_root / "renewal"
    instances: List[Dict[str, Any]] = list(spec.get("instances", []))

    for inst in instances:
        mode = str(inst.get("mode", "inst"))
        if mode not in mode_order:
            mode_order.append(mode)
        mode_dirs[mode] = fam_dir / mode
        env = dict(inst.get("env", {}))
        steps = int(inst.get("steps", env.get("T_max", 1000)))
        seeds: List[int] = list(inst.get("seeds", [7]))
        agents: List[Any] = list(inst.get("agents", [{"type": "last"}]))

        for seed in seeds:
            for agent in agents:
                atype, aname, aparams = _agent_fields(agent)
                tag = atype if not aname else f"{atype}_{_slug(aname)}"
                out_dir = fam_dir / mode / f"{tag}_s{seed}"
                cfg_path = out_root / "tmp" / "renewal" / mode / f"{tag}_s{seed}.yaml"

                env_payload = {
                    "kind": "renewal",
                    "spec": {},
                    "params": {
                        "A": int(env.get("A", 8)),
                        "L_win": int(env.get("L_win", 6)),
                        "p_ren": float(env.get("p_ren", 0.02)),
                        "p_noise": float(env.get("p_noise", 0.0)),
                        "T_max": int(env.get("T_max", steps)),
                    },
                }
                agent_payload = _agent_config(atype, aname, aparams)
                run_payload = {"steps": steps, "episodes": None, "horizon": None}
                job = SuiteJob(
                    family="renewal",
                    mode=mode,
                    seed=int(seed),
                    agent_type=atype,
                    agent_name=aname,
                    agent_tag=tag,
                    runner_module="experiments.runners.renewal_runner",
                    out_dir=out_dir,
                    config_path=cfg_path,
                    env=env_payload,
                    agent=agent_payload,
                    run=run_payload,
                    logging={"write_metrics": True, "write_budget": True, "write_plot": True},
                )
                _write_job_config(job)
                print(f"[renewal] {mode} :: agent={tag} seed={seed}")
                jobs.append(job)
    return jobs, mode_dirs, mode_order


# -------------------
# CLI
# -------------------

def main() -> None:
    ap = argparse.ArgumentParser(description="Run a multi-family suite (STOA + CO) from one YAML.")
    ap.add_argument(
        "--config",
        type=str,
        default="experiments/configs/suite_all.yaml",
        help="Suite config YAML",
    )
    args = ap.parse_args()

    suite_cfg = _load_yaml(Path(args.config))
    out_root = Path(suite_cfg.get("out_root", "outputs/suite"))
    if "--config" in sys.argv:
        ts = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        out_root = out_root.parent / f"{out_root.name}_{ts}"
    _ensure_dir(out_root)

    fams = dict(suite_cfg.get("families", {}))

    # Load and inject CO variants everywhere (can be disabled per config)
    inject_co = bool(suite_cfg.get("inject_co", True))
    if inject_co:
        co_manifest_path = suite_cfg.get("co_manifest", "experiments/configs/co_agents/co_agents_selection.yaml")
        co_path = Path(co_manifest_path)
        if not co_path.is_absolute():
            co_path = (Path(args.config).parent / co_path).resolve()
        co_manifest = _load_co_manifest(co_path)
        suite_cfg = _inject_co_everywhere(suite_cfg, co_manifest)
        fams = dict(suite_cfg.get("families", {}))

    family_order = [f for f in FAMILY_ORDER if f in fams]
    builder_map = {
        "bandit": _gather_bandit_jobs,
        "maze": _gather_maze_jobs,
        "renewal": _gather_renewal_jobs,
    }

    all_jobs: List[SuiteJob] = []
    mode_dirs: Dict[Tuple[str, str], Path] = {}
    mode_order: Dict[str, List[str]] = {}

    for family in family_order:
        jobs, dirs, order = builder_map[family](out_root, fams[family])
        all_jobs.extend(jobs)
        mode_order[family] = order
        for mode in order:
            mode_dirs[(family, mode)] = dirs.get(mode, out_root / family / mode)

    max_workers = int(suite_cfg.get("max_workers", 1))
    continue_on_failure = bool(suite_cfg.get("continue_on_failure", True))

    # Execute grouped by (family, mode) with barriers for summaries
    for family in family_order:
        for mode in mode_order.get(family, []):
            group_jobs = [j for j in all_jobs if j.family == family and j.mode == mode]
            _dispatch_jobs(group_jobs, max_workers=max_workers, continue_on_failure=continue_on_failure)

            mode_dir = mode_dirs.get((family, mode), out_root / family / mode)
            if family == "bandit":
                summarize_bandit_mode(mode_dir)
            elif family == "maze":
                summarize_maze_mode(mode_dir)
            elif family == "renewal":
                summarize_renewal_mode(mode_dir)

        summarize_family(out_root, family)

    summarize_suite(out_root, [f for f in ("bandit", "maze", "renewal") if f in family_order])
    _write_failure_report(out_root, all_jobs)

    print(json.dumps({"suite_out": str(out_root)}))


if __name__ == "__main__":
    main()
