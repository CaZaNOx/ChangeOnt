# TheoryOfChange_main — Knowledge Base

Purpose
- Clean, theory-only KB that accumulates canonical statements, concept pages, and a derivation DAG without touching the legacy folders.
- Every theory-relevant point appears exactly once (deduped), with provenance, and is cross-linked where needed.
- Accessible to non-math readers via Philosophical Translations.

Structure
- `01_Statements/` — Atomic, canonical statements (organized by full names):
  - `FoundationalTruth/` (FT), `Definition/` (DF), `Derivation/` (DR), `Corollary/` (CR)
- `02_Concepts/` — Curated concept pages aggregating relevant statements; no chatty back-and-forth.
- `03_Derivation/` — DAG of statements (nodes) and dependencies (edges), plus a readable derivation narrative.
- `04_Anchors/` — Optional real-world/code references (not core theory, but linked).
- `99_Imports/` — Provenance mappings from source materials to canonical statements.
 - `symbols/` — One file per symbol (e.g., Δ, ⥤); machine index at `symbols/index.yaml`.

Meta
- `SCHEMA.md` — Statement + concept frontmatter fields and rules.
- `TAGS.md` — Controlled vocab (domain, layer, motif, operator, status).
- `SYMBOLS.md` — Single source of truth for symbols; links to original Symbol_Map and extends it.
- `INGESTION_CHECKLIST.md` — How to file new content and dedupe properly.
- `TEMPLATES/` — Ready-to-copy templates for statements and concepts.

Ground Rules
- Deduplicate: Enrich existing statements; don’t duplicate content.
- Provenance: Every item includes source references (file:line).
- No drift: Symbols and tags must be registered before use.
- DAG integrity: Statements reference only defined dependencies; no cycles.
- Reader-first: Every formal claim has a “Philosophical Translation (of formal claim)” — a plain-language restatement.
- Obsidian linking:
  - Use wiki links to refer to statements by path (e.g., `[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]`) or by note name where applicable.
  - Add Obsidian tags (e.g., `#type/FT #layer/foundations #domain/ontological #concept/ontology-of-change #symbol/Delta`).

Maintenance
- Backlinks and relationships (statements “Referenced By” + “Relationships”, symbols “Used In”):
  - Run `python3 tools/update_backlinks.py`
  - Note: Auto-generated sections are guarded by markers and will be replaced on each run:
    - `<!-- BEGIN:AUTOGEN:REFERENCED_BY --> ... <!-- END:AUTOGEN:REFERENCED_BY -->`
    - `<!-- BEGIN:AUTOGEN:RELATIONSHIPS --> ... <!-- END:AUTOGEN:RELATIONSHIPS -->`
    - `<!-- BEGIN:AUTOGEN:USED_IN --> ... <!-- END:AUTOGEN:USED_IN -->`
    Do not manually edit content between these markers.
- Validate structure and links (frontmatter, wiki links, symbol pages, graph IDs):
  - Run `python3 tools/validate_toc_main.py`
- Frontmatter linking (required):
  - concepts/parents/dependencies/successors/symbols_used must use wiki links, e.g.
    - `concepts: ["[[02_Concepts/C-ontology-of-change]]"]`
    - `parents: ["[[01_Statements/FoundationalTruth/S-FT-immediate-datum]]"]`
    - `symbols_used: ["[[01_Statements/SYMBOLS/Delta]]"]`
