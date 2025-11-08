# Ingestion & Merge Checklist

Goal: file new theory content without duplication or drift.

1) Identify unit(s)
- Extract atomic statements (FT/DF/DR/CR/CF/AS/CL) and their claims.
- Note provenance (file:line). Capture math/pseudocode if present.

2) Map or create
- Search `01_Statements/` for an existing matching statement.
  - If found, enrich: add sources, proofs, math, pseudocode.
  - If new nuance: add a new statement (often CR/DR) and link via `dependencies`.
- If none, create a new statement file using the template.

3) Symbols
- Ensure all symbols used are registered in `00_Meta/SYMBOLS.md`.
- If new, add entry (definition, scope, examples) before using in statements.

4) Concepts
- Add or update the relevant page in `02_Concepts/`:
  - Link canonical statements (no duplication).
  - Add cross-refs to related concepts.
  - Append open items (godel holes, missing operators, contradictions).

5) Derivation DAG
- Update `03_Derivation/graph.yaml` with nodes/edges.
- Validate: no cycles, dependencies exist, foundations are reachable.

6) Tags & Status
- Assign controlled tags (`TAGS.md`) and status (stable/draft/open/speculative).

7) Commit notes
- Summarize: new statements added, enriched statements, symbols updated, DAG edges.

