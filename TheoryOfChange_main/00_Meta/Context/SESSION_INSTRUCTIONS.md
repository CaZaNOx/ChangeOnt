---
title: Session Instructions — Canon for Processing Chats and Maintaining Rigor
status: evolving
tags: [meta, context, rigor]
---
# Session Instructions — Canon for Processing Chats and Maintaining Rigor

Processing AI Chats
- Deep‑read each chat; flag only theory‑bearing sections with file:line pointers.
- For each flagged item decide: Covered | Needs Clarification/Corollary (CL/CR) | Hypothesis (HYP) to Speculations.
- Promote only when derivable from existing FT/DF/DR (with explicit parents/dependencies); otherwise record as HYP with a concrete test sketch.
- Avoid long raw excerpts; produce actionable maps (pointers + decisions).

Scope and Source Policy
- Do not copy full chat logs into TheoryOfChange_main. We store only theory‑relevant content as formal statements (DF/DR/CR/CL) and hypotheses (HYP) in the relevant folders.
- Keep curated mapping docs for each chat under 00_Meta/Context (e.g., AI_1_mapping.md, AI_2_mapping.md) with precise ranges and status.

Artifacts and Locations
- Mapping docs: 00_Meta/Context/AI_X_mapping.md (pointers + status + targets).
- Formal statements: 01_Statements/* (Definition, Derivation, Corollary, Clarification, etc.).
- Hypotheses/experiments: 05_Speculations/HYPOTHESES/* with a test sketch.
- Derivation graph: 03_Derivation/graph.yaml — add nodes and edges for every new statement.
- State pointer: 00_Meta/Context/state.json — track last processed chat + line pointer(s).

Promotion Rules (CL/CR/DF/HYP)
- CL (Clarification): use to scope wording, map metaphors to formal constructs, and align probability/time/consciousness phrasing to SRL/Evaluation/RTV/Breath.
- CR (Corollary): promote only when clearly derivable from existing parents; include parents/dependencies, symbols_used, and sources (file:line).
- DF (Definition): introduce a concept only if necessary to operationalize repeated motifs (e.g., Intersubject Translation Resonance). Provide philosophical and formal handles.
- HYP: record exploratory/diagnostic ideas with a minimal test protocol; do not add to the graph.

File Conventions (Obsidian‑friendly)
- Frontmatter: id, type, title, concepts (Obsidian links), dependencies, parents, successors, symbols_used, sources, tags.
- Body: include a short philosophical translation for formal claims. Guarded auto‑sections with sentinels are handled by tools.
- Tags: use both structured frontmatter tags and bottom hash‑tags for discoverability (e.g., #type/CR, #layer/validation).

Linking & Symbols
- Use path‑style Obsidian wikilinks (e.g., [[01_Statements/Definition/S-DF-rtv-operator]]).
- symbols_used must point to one‑per‑file symbol pages under 01_Statements/SYMBOLS/.
- Prefer path‑style symbol links; short‑note symbol links are recognized by the updater.

Graph Policy
- Every new DF/DR/CR/CL must have a node in 03_Derivation/graph.yaml with an id matching the statement’s id.
- Add minimally sufficient edges from nearest parents; do not over‑connect.

Validation Gates (run in order)
- Update backlinks/relationships: `python3 tools/update_backlinks.py`
- Validate structure/links: `python3 tools/validate_toc_main.py`
- Advisory linter: `python3 tools/lint_drift_terms.py` (fix by adding CL references rather than rewriting theory content).

Drift Guardrails
- Probability language → map to SRL/Evaluation Surface.
- Time talk → breath/RTV/σ(ε) phenomenology; avoid physical time claims unless bridged.
- Attention → recursive prioritization, not spotlight.
- Consciousness → scope via Cᴸ locks and proto‑criteria.

Working Protocol (per chat)
1) Deep‑read map: create/update 00_Meta/Context/AI_X_mapping.md with ranges, status, and targets.
2) Batch‑promote: add CL/CR/DF/HYP according to mapping; wire graph nodes/edges.
3) Run tools in the Validation Gates section.
4) Update 00_Meta/Context/state.json with last processed line and notes.

Current Status Snapshot (for continuity)
- AI_1–AI_3: mappings finalized, all promoted CL/CR/DF/HYP wired into `03_Derivation/graph.yaml` and documented in the respective mapping files.
- AI_4–AI_20: runs are now tracked centrally through `00_Meta/Context/AI_Leads_Master.md`; each entry identifies the chat, block range, and why it still needs review. This master list is the single source of truth for “still interesting” content that survives the first shallow scan.
- New statements/hypotheses already committed (e.g., `S-CL-act-relative-detectability`, `S-CL-arrow-of-time-memory-irreversibility`, `S-DF-actor`, `S-DR-breath-knot-stabilization-topology`, `HYP-Goal-Emergence-From-Feedback`) cover the main motifs unearthed so far.
- Next focus: finish the AI_15–AI_20 block passes (flag → decide → promote/prune → graph) and prune their ranges from the master list immediately upon resolution.

Master Leads Workflow
- Treat `AI_Leads_Master.md` as the batching log: read each range in context, flag whether it adds clarification, derivation, definition, or hypothesis, then either prune the lead or schedule a promotion.
- Use the per-chat files in `TheoryOfChange/00_Meta/AI_RecursiveChats*` for sourcing; point to the slim copy when the full log contains redundancies.
- Record decisions in the master file (status columns) so future passes know whether a range still needs review or is already promoted/covered.

Graph & Statement Hygiene
- After promoting a CL/CR/DF/DR, add a corresponding node to `03_Derivation/graph.yaml` (matching the statement id) and draw edges to the most immediate parents. Run `python3 tools/graph_sweep_suggest.py` to catch missing linkages, then rerun `python3 tools/update_backlinks.py`.
- Hypotheses remain in `05_Speculations/HYPOTHESES/` and are excluded from the DAG; document experiment sketches and drift expectations in their bodies.
- Keep `01_Statements/SYMBOLS/` synchronized (add new symbol pages when introduced, update `symbols_used` in each statement).

Rigor and Anti‑Drift
- No unjustified theory bloat; no smoothing inconsistencies — flag them.
- Map probabilistic wording to SRL/Evaluation Surface; time talk to Breath/RTV/σ(ε) phenomenology; scope consciousness via Cᴸ/proto‑locks; reaffirm change as foundational.
- Use the drift linter: `python3 tools/lint_drift_terms.py` and fix/clarify any findings.

Structure & Linking
- Every CL/CR/DF carries Obsidian links to parents/dependencies/symbols and sources (file:line).
- Symbols one‑per‑file in `01_Statements/SYMBOLS/`; declare `symbols_used:` in statements.
- Backlinks: `python3 tools/update_backlinks.py`; Validate: `python3 tools/validate_toc_main.py`.

Speculations
- Exploratory/implementation items live under `05_Speculations/HYPOTHESES/` with test sketches.
- Do not promote speculative content without derivations/benchmarks.

Working Protocol
- For each chat: (1) Flag map; (2) Batch‑add CL/CR/HYP as decided; (3) Run linter + validator; (4) Record state.
- For spiral/phenomenology motifs: add clarifications to avoid importing classical assumptions (e.g., eternal recurrence; absolute time).
