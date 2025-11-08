# Speculations

Purpose
- Hold exploratory ideas that are not (yet) sufficiently justified to live in the core theory folders.
- Keep originals alongside concise, cross‑linked summaries.

Structure
- `ORIGINALS/` — Direct copies from `TheoryOfChange/03_Specualtions/` (unchanged).
- `SUMMARIES/` — Concise cross‑linked summaries with:
  - `links_core`: pointers to relevant FT/DF/DR/CR
  - `candidate_moves`: suggested promotions (e.g., CR/CL) when justified

Policy
- Do not move speculative content into core until it’s supported by existing statements or a minimally formal derivation.
- When promoting, add a new FT/DF/DR/CR file and keep the speculation here for historical context.

Maintenance
- After promotions, run `python3 tools/update_backlinks.py` and `python3 tools/validate_toc_main.py`.
