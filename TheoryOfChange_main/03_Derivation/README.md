# 03_Derivation — DAG and Narrative

Files
- `graph.yaml` — nodes (statements) and edges (dependencies).
- `Derivation.md` — curated story walking through the DAG.

Checks
- All referenced statements exist.
- Graph is acyclic.
- Foundations are reachable; speculative islands are labeled.

Maintenance
- Validate graph node IDs against statements: `python3 tools/validate_toc_main.py`
- Backlinks updater does not modify the graph; maintain edges explicitly in `graph.yaml`.
