# 01_Statements — Atomic Canonical Units in Route-First Order

Rules
- One statement per file; each file remains the canonical home of one claim.
- Use the statement template fully: claim, translation, justification, derivation, formalization, clarifications, and next steps.
- Do not artificially shorten or pad. A simple derivation may be short; a complex one should be fully spelled out.
- Every attacked rival concept must be explicitly formulated strongly enough to avoid strawman drift.
- Every symbol in `symbols_used` must exist in `01_Statements/SYMBOLS/` and be clearly defined.

Naming
- Files keep their stable statement IDs in the filename, e.g. `00_Opening_Justification/006_S-FT-immediate-datum.md`.
- Numeric prefixes indicate canonical reading order within a route, e.g. `00_Opening_Justification/006_S-FT-immediate-datum.md`.
- The stable `id` in frontmatter remains the long-term identity anchor.

Route-first organization
The canonical human reading order is now organized by argument route rather than by statement kind.

Current canonical route folders:
- `00_Opening_Justification/` — Layer 0 opening: shared critical ground, epistemic undeniability, rival critique, and handoff.
- `01_Change_Clarification/` — first clarification of what “change” means before heavier derivation.

inactive type folders (`FoundationalTruth`, `Definition`, `Derivation`, `Clarification`, etc.) still exist for material not yet migrated, but new canonical reading should follow the route folders.

Preserving rigor
- Statement kind is preserved in the filename and frontmatter (`type: FT|DF|DR|CL|...`).
- Route position is expressed by folder placement and numeric prefix.
- Cross-route relevance belongs in links and concept pages, not by duplicating files.

Templates and schema
- Statement template: `../00_Meta/TEMPLATES/STATEMENT.md`
- Concept template: `../00_Meta/SCHEMA.md`
- Schema: `../00_Meta/SCHEMA.md`

Validation
- Update backlinks: `python3 tools/update_backlinks.py`
- Validate links and structure: `python3 tools/validate_toc_main.py`
