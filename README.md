# ChangeOnt — CO-core (Change Ontology) reference implementation

**ChangeOnt** is a reference implementation of the **Change Ontology (CO)** “core”:
- **Philosophy → Math → Spec → Code → Benchmarks → Falsifiers.**
- CO treats *change* as primitive (Immediate Datum), builds **eventlets → paths → bends (τ) → equivalence → quotient Q → gauge G**, and shows how “classical” regimes arise as a **collapse header** (a stabilized special case).

## Why this repo
- Provide an **auditable, prereg-like spec** for CO-core (a–i) with guardrails (no oracles, budget parity, LLN drift-guards).
- Offer **baseline comparisons** on small, honest tasks (renewal/codebook, drifting bandit, maze).
- Keep **results reproducible**: seeds, configs, JSONL logs, plots, and acceptance bands.

## Quick start
1. Create venv and install deps:
   - Windows (PowerShell): `python -m venv .venv; .\.venv\Scripts\Activate.ps1; pip install -r requirements.txt`
   - macOS/Linux: `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`
2. Populate empty files from payloads (safe):
   - Preview: `python tools/populate_repo.py --dry-run`
   - Apply:   `python tools/populate_repo.py`
3. Run a tiny smoke test (after later batches land):  
   `python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml`

## Project layout (high level)
- `docs/` — philosophy, math, logic, spec, proofs, compliance, benchmarks, evaluation.
- `core/` — CO math/logic, gauge/quotient/loops/headers, and agent implementations.
- `benchmarks/` — small environments (renewal/codebook, bandit, maze).
- `experiments/` — runners, configs, logging & plotting.
- `evaluation/` — metrics, reports.
- `tests/` — unit + property tests.
- `outputs/` — run artifacts; ignored by git.

## CO-strict guardrails (zero smuggling)
- **No oracles** from the plant (no step indices, lap counts, renewal flags).
- **No topology edits**; only quotienting & gauge-warped costs.
- **Two-time-scale RM** for gauge; drift guard + sample floor for LLN.
- **Collapse header** recognizes classical as a stabilized limit (H≤0.10 bits, var≤5%).
- **Falsifiers** per mechanism with pass/fail gates.

See `docs/OVERVIEW.md` after Batch 2 for the complete narrative.



# ChangeOnt — CO-core runnable skeleton

This repository contains a minimal, testable scaffold for **Change Ontology (CO)** experiments:

- Toy **renewal/codebook** environment,
    
- **Drifting bandit** and **grid maze** baselines,
    
- A single **experiment runner** that writes JSONL logs,
    
- Unit tests to sanity-check each component.
    

> Goal: make it easy to drop in CO-core mechanisms (HAQ, quotient, headers), run parity fixtures, and compare to classical baselines under **budget parity**.

## 1) Setup (Windows PowerShell or macOS/Linux bash)

Create and activate a virtual environment, then install deps:

PowerShell (Windows):  
python -m venv .venv  
..venv\Scripts\Activate.ps1  
python -m pip install --upgrade pip  
pip install -r requirements.txt

bash (macOS/Linux):  
python3 -m venv .venv  
source .venv/bin/activate  
python -m pip install --upgrade pip  
pip install -r requirements.txt

> If VS Code complains “import numpy could not be resolved,” ensure the **.venv** interpreter is selected (Ctrl/Cmd-Shift-P → “Python: Select Interpreter”).

## 2) Quick sanity checks

Run unit tests:

python -m pytest -q

You should see basic env/runner/baseline tests pass.

## 3) Run example experiments

Renewal toy (FSM baseline now; switch to `agent: haq` later):  
python experiments/run_experiment.py --config experiments/configs/toy_ren_haq_vs_fsm.yaml --out_dir outputs

Drifting bandit (UCB baseline):  
python experiments/run_experiment.py --config experiments/configs/bandit_ucb.yaml --out_dir outputs

Grid maze (greedy BFS baseline):  
python experiments/run_experiment.py --config experiments/configs/maze_bfs.yaml --out_dir outputs

Each run emits:

- `outputs/<task>_<agent>_seed<...>.steps.jsonl`
    
- `outputs/<task>_<agent>_seed<...>.episodes.jsonl`
    

## 4) Interpreting logs

See `docs/EVALUATION.md` for metric definitions. Minimal per-episode summaries are printed to stdout for quick inspection.

## 5) Next steps (where CO plugs in)

- Implement CO-core modules in `core/` (gauge, quotient, headers).
    
- Wire **HAQ** agent at `core/agents/agent_haq.py` (if not present).
    
- Update renewal config’s `agent: haq`, rerun, and compare AUReg/flip alignment/etc.
    
- Add ablations in `experiments/configs/` and update tests in `tests/`.
    

## 6) Reproducibility

Shared seeds live in `experiments/seeds.yaml`. Keep **precision float32**, report **FLOPs/step** and **memory bits** (including quotient tables) for budget parity.

For details on CO strictness, see:

- `docs/CO_STRICT_RULES.md`
    
- `docs/SPEC_CORE_A_TO_I.md`
    
- `docs/HEADERS.md`
