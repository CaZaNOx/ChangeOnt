# 02_Concepts — Curated Homes

Purpose
- Aggregate canonical statements under clear themes.
- Provide human-readable overviews and link to the derivation DAG.

Structure (per concept)
---
id: concept.<slug>
title: <name>
tags: [motif:..., operator:..., domain:..., layer:...]
status: stable|evolving|draft
---
Overview:
...

Canonical statements:
- stmt.<id> (FT)

Dependencies:
- From: concept.<slug>
- To: concept.<slug>

Open items:
- godel_hole: ...

Conventions
- Add H1 title at top (same as `title`), and prefer frontmatter tags like `concept/<slug>`, `foundations`, `ontological`.
- Link statements via wiki links, e.g. `[[S-FT-immediate-datum]]`.
- Optionally add a “Referenced By” section listing statements/concepts that link here.

Maintenance
- Validate links and tags: `python3 tools/validate_toc_main.py`
