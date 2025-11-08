# 01_Statements — Atomic Canonical Units

Rules
- One statement per file; file is the canonical home.
- Use the template; include provenance, parents/successors, and all derivations.
- Do not artificially shorten: include full philosophical justification and formal/logical derivation. Link or embed proofs.
- Every symbol in `symbols_used` must exist in `00_Meta/SYMBOLS.index.yaml` and have its own definition file.

Naming
- `S-<TYPE>-<slug>.md` (e.g., `S-FT-immediate-datum.md`).
- Stable `id` in frontmatter (e.g., `stmt.immediate-datum`).

See `../00_Meta/SCHEMA.md` for fields and examples.

Templates
- Statement template: `../00_Meta/TEMPLATES/STATEMENT.md`
- Concept template: `../00_Meta/TEMPLATES/CONCEPT.md`

Reading for non-math audiences
- Every statement includes a "Philosophical Translation (of formal claim)" section to restate math/logic in plain language.

Folder layout
- `FT/` foundational truths, `DF/` definitions, `DR/` derivations, `CR/` corollaries.
- `SYMBOLS/` per-symbol pages and `index.yaml`.

Frontmatter conventions (must be wiki links and real tags)
- Link fields: `concepts`, `parents`, `dependencies`, `successors`, `symbols_used` use wiki links, e.g.
  - `concepts: ["[[02_Concepts/C-ontology-of-change]]"]`
  - `symbols_used: ["[[01_Statements/SYMBOLS/Delta]]"]`
- Tags: `tags: [foundations, ontological, stable, "type/FT", "symbol/Delta", "concept/ontology-of-change"]`

-Backlinks and validation
- Update backlinks (statements “Referenced By” + “Relationships”, symbols “Used In”): `python3 tools/update_backlinks.py`
- Validate links and structure: `python3 tools/validate_toc_main.py`
