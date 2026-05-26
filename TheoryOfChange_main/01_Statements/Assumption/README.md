# Assumptions (AS)

Scope
- Methodological or modeling assumptions used provisionally to enable progress (e.g., language, logic, minimality), with clear plans to replace them by derived theory.

Conventions
- Frontmatter `type: AS` and wiki links to the FT/DF/DR/CR they support.
- Keep concise; state scope and deprecation path (which statements replace the assumption over time).

Graph policy
- Assumptions are not first-class nodes in the derivation DAG. Link from AS → DF/FT in body/relationships only.

Maintenance
- After updates, run `python3 tools/update_backlinks.py` and `python3 tools/validate_toc_main.py`.

