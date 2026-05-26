"""Produce a small plug-and-play audit artifact for the generic problem contract.

Run:
    python -m experiments.studies.problem_contract_plugplay_v1
"""
from __future__ import annotations

import json
from pathlib import Path

from agents.co.integration.core_builder import build_co_core
from agents.co.adapters.bandit_adapter import COAdapterBandit
from agents.co.adapters.renewal_adapter import COAdapterRenewal
from agents.co.adapters.maze_adapter import COAdapterMaze


def _core():
    return build_co_core({
        "header": {"type": "SSI"},
        "elements": {"commitment_surface": {"enabled": True, "ngram_order": 0}},
        "primitives": {"signal_bus": {}, "bandit_stats": {}, "ngram_model": {}},
    })


def main() -> None:
    out = {}

    bandit = COAdapterBandit(_core(), n_arms=5)
    bandit.select({"family": "bandit", "t": 0, "n_arms": 5})
    out["bandit_5arm"] = dict((bandit._last_obs or {}).get("problem_contract", {}))

    renewal = COAdapterRenewal(_core())
    renewal.select({"family": "renewal", "t": 0, "A": 4, "obs": 1, "L_win": 2})
    out["renewal_A4"] = dict((renewal._last_obs or {}).get("problem_contract", {}))

    maze = COAdapterMaze(_core())
    maze.select({"family": "maze", "t": 0, "pos": [0, 0], "goal": [0, 1], "width": 2, "height": 1, "grid": [[0, 0]]})
    out["maze_2x1"] = dict((maze._last_obs or {}).get("problem_contract", {}))

    result = {
        "schema_match": len({tuple(sorted(v.keys())) for v in out.values()}) == 1,
        "families": out,
        "judgment": "same top-level contract schema present across active adapters; vocabulary still family-specific in values; legacy packet dependence remains",
    }

    path = Path('outputs/problem_contract_plugplay_v1_results.json')
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result, indent=2, sort_keys=True), encoding='utf-8')
    print(path.as_posix())


if __name__ == "__main__":
    main()
