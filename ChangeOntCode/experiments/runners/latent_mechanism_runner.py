from __future__ import annotations

from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import argparse, json, os, random
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from collections import deque

from environments.latent_mechanism.env import LatentMechanismDoorWorld, MechanismSpec, ACTIONS, DIRS
from experiments.logging.logging import write_metric_line, write_budget_csv
from experiments.config_utils import normalize_agent_config

try:
    from agents.co.adapters.latent_mechanism_adapter import COAdapterLatentMechanism
    from agents.co.integration.core_builder import build_co_core
    HAS_CO = True
except Exception:
    HAS_CO = False


def _iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _strict_errors() -> bool:
    return str(os.environ.get("CO_STRICT_ERRORS", "")).strip() == "1"


def _parse_yaml(text: str) -> dict:
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text) or {}
    except Exception:
        return {}


@dataclass
class RunCfg:
    seed: int
    out_dir: str
    spec_name: str
    spec_params: Dict[str, Any]
    agent: Dict[str, Any]
    log_every: int


def _load_cfg(path: str) -> RunCfg:
    text = Path(path).read_text(encoding="utf-8")
    data = json.loads(text) if path.endswith('.json') else _parse_yaml(text)
    job = data.get("job", {}) if isinstance(data.get("job"), dict) else {}
    env = data.get("env", {}) if isinstance(data.get("env"), dict) else {}
    spec = data.get("spec", {}) if isinstance(data.get("spec"), dict) else {}
    agent = normalize_agent_config(data.get("agent", {"type": "co", "params": {}}), default_algo="co")
    return RunCfg(
        seed=int(data.get("seed", job.get("seed", 0))),
        out_dir=str(data.get("out_dir", job.get("out_dir", "outputs/latent_mechanism_run"))),
        spec_name=str(spec.get("name", env.get("name", "hidden_depth2"))),
        spec_params=dict(spec.get("params", env.get("params", {})) or {}),
        agent=agent,
        log_every=int(data.get("log_every", job.get("log_every", 10))),
    )


def _make_spec(name: str, params: Dict[str, Any]) -> MechanismSpec:
    seed = int(params.get("seed", 0))
    if name == "easy_visible":
        spec = MechanismSpec.easy_visible(seed=seed)
    elif name == "hidden_depth2":
        spec = MechanismSpec.hidden_depth2(seed=seed)
    elif name == "deceptive_depth3":
        spec = MechanismSpec.deceptive_depth3(seed=seed)
    else:
        raise ValueError(f"Unknown latent mechanism spec: {name}")
    for k, v in params.items():
        if hasattr(spec, k):
            setattr(spec, k, v)
    return spec


def _bfs_action(obs: Dict[str, Any], target: Tuple[int, int]) -> Optional[str]:
    pos = tuple(obs.get("pos") or (0, 0))
    H = int(obs.get("height", 0) or 0)
    W = int(obs.get("width", 0) or 0)
    grid = obs.get("grid")
    if pos == target:
        return None
    def passable(r: int, c: int) -> bool:
        if not (0 <= r < H and 0 <= c < W):
            return False
        try:
            return int(grid[r][c]) in (0, 2, 3, 5, 6)
        except Exception:
            return False
    q = deque([pos])
    prev: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {}
    seen = {pos}
    while q:
        cur = q.popleft()
        for a, (dr, dc) in DIRS.items():
            nxt = (cur[0] + dr, cur[1] + dc)
            if nxt in seen or not passable(nxt[0], nxt[1]):
                continue
            prev[nxt] = (cur, a)
            if nxt == target:
                p = nxt
                while prev[p][0] != pos:
                    p = prev[p][0]
                return prev[p][1] if p in prev else a
            seen.add(nxt)
            q.append(nxt)
    return None


def _heuristic_action(obs: Dict[str, Any], memory: Dict[str, Any]) -> str:
    pos = tuple(obs.get("pos") or (0, 0))
    goal = tuple(obs.get("goal") or (0, 0))
    switches = [tuple(x) for x in list(obs.get("switches") or [])]
    decoys = [tuple(x) for x in list(obs.get("decoys") or [])]
    door_open = bool(obs.get("door_open", False))
    legal = list(obs.get("legal_actions") or [])
    attempted = memory.setdefault("attempted", {})
    if "INTERACT" in legal and (pos in switches or pos in decoys):
        if memory.setdefault("attempted", {}).get(pos, 0) == 0 or (pos in switches and not door_open):
            return "INTERACT"
    if door_open:
        act = _bfs_action(obs, goal)
        return act or (legal[0] if legal else "UP")
    # prefer untried switches, then untried decoys, then door, then goal
    candidates = [s for s in switches if attempted.get(s, 0) == 0]
    if not candidates:
        candidates = [s for s in decoys if attempted.get(s, 0) == 0]
    if candidates:
        tgt = min(candidates, key=lambda s: abs(s[0] - pos[0]) + abs(s[1] - pos[1]))
        act = _bfs_action(obs, tgt)
        return act or (legal[0] if legal else "UP")
    act = _bfs_action(obs, tuple(obs.get("door") or goal))
    return act or (legal[0] if legal else "UP")


def run(config_path: str) -> Dict[str, Any]:
    cfg = _load_cfg(config_path)
    out_dir = Path(cfg.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = out_dir / "metrics.jsonl"
    budget_path = out_dir / "budget.csv"
    manifest_path = out_dir / "run_manifest.json"
    started_at = _iso_now()
    status = "failed"
    error: Optional[str] = None
    co_runtime_contract: Optional[Dict[str, Any]] = None
    for p in (metrics_path, budget_path):
        if p.exists():
            p.unlink()
    spec = _make_spec(cfg.spec_name, cfg.spec_params)
    env = LatentMechanismDoorWorld(spec=spec)
    agent_cfg = dict(cfg.agent)
    atype = str(agent_cfg.get("type", "co")).lower()
    aparams = dict(agent_cfg.get("params", {}))
    aname = agent_cfg.get("name")
    agent_tag = atype if not aname else f"{atype}:{aname}"
    write_budget_csv(budget_path, [{"params_bits": 0, "flops_per_step": 1, "memory_bytes": 0}])
    mem: Dict[str, Any] = {}
    try:
        obs, _, done, info = env.reset(seed=cfg.seed)
        if atype == "co":
            if not HAS_CO:
                raise RuntimeError("CO latent_mechanism adapter/core not importable")
            core = build_co_core(aparams)
            co_runtime_contract = core.export_runtime_contract()
            agent = COAdapterLatentMechanism(core=core, name=(aname or "CO_latent_mechanism"))
        else:
            agent = None
        write_metric_line(metrics_path, {
            "record_type": "header",
            "runner": "latent_mechanism",
            "family": "latent_mechanism",
            "seed": cfg.seed,
            "spec_name": cfg.spec_name,
            "spec_params": cfg.spec_params,
            "agent": agent_tag,
            "out_dir": str(out_dir),
            "co_runtime_contract": co_runtime_contract,
        })
        rewards = 0.0
        success = 0
        reframes = 0
        rows: List[Dict[str, Any]] = []
        prev_door = bool(obs.get("door_open", False))
        while True:
            if atype == "co":
                sel = agent.select({"family": "latent_mechanism", **obs})  # type: ignore[union-attr]
                act = sel.get("action") if isinstance(sel, dict) else sel
                if isinstance(sel, dict):
                    row = {
                        "t": int(obs.get("t", 0) or 0),
                        "action": act,
                        "co_policy": sel.get("co_policy"),
                        "co_weight": float(sel.get("co_weight", 1.0) or 1.0),
                        "signal_bus_votes": int(sel.get("signal_bus_votes", 0) or 0),
                    }
                    for key in (
                        "canonical_commitment_mode",
                        "canonical_commitment_reason",
                        "certificate_aware_stable_continuation_applied",
                        "certificate_aware_reopen_or_sample_applied",
                        "candidate_final_scores",
                        "candidate_obs_scores",
                        "canonical_commitment_assessment",
                        "commit_readiness",
                        "evidence_margin",
                        "evidence_support",
                        "co_sources",
                        "co_evidence_valid_for_step",
                    ):
                        if key in sel:
                            row[key] = sel[key]
                    rows.append(row)
            elif atype == "heuristic":
                act = _heuristic_action(obs, mem)
            elif atype == "random":
                act = random.Random(cfg.seed + int(obs.get("t", 0))).choice(list(obs.get("legal_actions") or ["UP"]))
            else:
                act = "UP"
            next_obs, r, done, info = env.step(str(act))
            rewards += float(r)
            if str(act) == "INTERACT":
                tile = tuple(obs.get("pos") or (0, 0))
                mem.setdefault("attempted", {})[tile] = mem.setdefault("attempted", {}).get(tile, 0) + 1
            if not prev_door and bool(next_obs.get("door_open", False)):
                reframes += 1
            prev_door = bool(next_obs.get("door_open", False))
            if bool(done) and tuple(next_obs.get("pos") or (0, 0)) == tuple(next_obs.get("goal") or (999, 999)):
                success = 1
            t_cur = int(obs.get("t", 0) or 0)
            if (t_cur % max(1, int(cfg.log_every))) == 0 or done:
                write_metric_line(metrics_path, {
                    "metric": "step",
                    "t": t_cur,
                    "action": str(act),
                    "reward": float(r),
                    "door_open": bool(next_obs.get("door_open", False)),
                    "progress_obs": next_obs.get("progress_obs"),
                    "last_event": info.get("last_event"),
                })
            if atype == "co":
                try:
                    agent.update({"observation": tuple(next_obs.get("pos") or (0, 0)), "reward": float(r), "done": done, "action": act})  # type: ignore[union-attr]
                except Exception:
                    if _strict_errors():
                        raise
            if done:
                break
            obs = next_obs
        nsteps = max(1, int(obs.get("t", 0) or 0) + 1)
        summary = {
            "spec_name": cfg.spec_name,
            "agent": agent_tag,
            "steps": nsteps,
            "mean_reward": float(rewards / nsteps),
            "success": int(success),
            "door_reframes": int(reframes),
            "wrong_count": int(info.get("wrong_count", 0) or 0),
            "mechanism_depth": int(info.get("mechanism_depth", spec.mechanism_depth)),
            "co_runtime_contract": co_runtime_contract,
        }
        (out_dir / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
        if rows:
            (out_dir / "co_debug_rows.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
        status = "ok"
        return summary
    except Exception as exc:
        error = f"{type(exc).__name__}: {exc}"
        raise
    finally:
        manifest_path.write_text(json.dumps({
            "started_at": started_at,
            "finished_at": _iso_now(),
            "status": status,
            "error": error,
            "seed": cfg.seed,
            "spec_name": cfg.spec_name,
            "agent": agent_tag,
        }, indent=2), encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description="Latent mechanism door worlds runner")
    ap.add_argument("--config", type=str, required=True)
    args = ap.parse_args()
    summary = run(args.config)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
