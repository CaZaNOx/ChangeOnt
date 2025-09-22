import json
from pathlib import Path
from experiments.runners.renewal_runner import run

def test_runner_writes_jsonl(tmp_path: Path):
    cfg = {
        "seed": 7,
        "steps": 50,
        "env": {"A": 4, "L_win": 3, "p_ren": 0.0, "p_noise": 0.0, "T_max": 50},
        "out_dir": str(tmp_path / "out")
    }
    p = tmp_path / "cfg.json"
    p.write_text(json.dumps(cfg), encoding="utf-8")
    paths = run(str(p))
    m = Path(paths["metrics"])
    assert m.exists()
    data = m.read_text(encoding="utf-8").strip().splitlines()
    assert len(data) >= 2  # header + at least one step
