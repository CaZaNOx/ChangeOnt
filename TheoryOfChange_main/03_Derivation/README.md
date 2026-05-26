# 03_Derivation — DAG and Narrative

Files
- `graph.yaml` — nodes (statements) and edges (dependencies).
- `graph.mmd` — full Mermaid snapshot of the graph.
- `graph_first_layer.mmd` — filtered Mermaid snapshot of the canonical first-layer route.
- `Derivation.md` — curated story walking through the DAG.

Checks
- All referenced statements exist.
- Graph is acyclic.
- Foundations are reachable; speculative islands are labeled.

Maintenance
- Validate graph node IDs against statements: `python3 tools/validate_toc_main.py`
- Backlinks updater does not modify the graph; maintain edges explicitly in `graph.yaml`.
