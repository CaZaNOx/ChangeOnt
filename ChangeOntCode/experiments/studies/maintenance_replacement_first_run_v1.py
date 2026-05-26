from __future__ import annotations

import json
from pathlib import Path

from experiments.runners.maintenance_replacement_runner import run_episode


def main() -> None:
    out = Path("outputs/maintenance_replacement_first_run_v1")
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for regime in ("bandit_like", "middle", "renewal_like"):
        for agent in ("threshold", "random", "co"):
            for seed in range(3):
                try:
                    rows.append(run_episode(regime=regime, agent_kind=agent, seed=seed))
                except Exception as exc:
                    rows.append({"family": "maintenance_replacement", "regime": regime, "agent": agent, "seed": seed, "error": repr(exc)})
    (out / "summary.json").write_text(json.dumps(rows, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(rows, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
