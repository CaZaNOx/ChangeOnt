## Goal
- Maintain a pure theory knowledge graph in `TheoryOfChange_main` (no process/gating/AI-instruction noise).
- Every statement file must follow `00_Meta/TEMPLATES/STATEMENT.md` with full frontmatter and content:
  - id/type/title/aliases
  - concepts/dependencies/parents/successors/symbols_used/sources/flags/tags/status
  - Sections: Claim (formal), Philosophical Translation, Philosophical Justification, Explanation (informal), Derivation (Philosophical), Derivation (Formal), Proofs/Corollaries References, Clarifications/Further Context, Next Steps.
  - Populate `symbols_used` when symbols appear; add parents/successors/deps so graph is connected.
- End state: connected, gap-free theory graph; a reader can traverse from root and get complete, non-duplicated theory, with no process chatter or AI slop.

## Scope Rules
- Keep only theory in `_main`. Process/AI-instruction/gating files belong in `00_Meta/Overhead/Process` (not in statements graph).
- If a file is meta/process, relocate it here; otherwise, rewrite to full template.
- Do not do tag-only tweaks; fill all required sections with substantive content.

## Execution Discipline
- Work in large batches; no per-file prompting.
- After batch edits, run `tools/update_backlinks.py` and `tools/validate_toc_main.py` once, then log progress.
- If validation fails, fix references immediately; do not leave broken graph.

## Quality Bar
- No empty `symbols_used` when symbols appear.
- No missing parents/successors where links are clear.
- No AI slop: avoid vague phrasing; include justifications and clarifications; remove duplicates/process notes from theory.
- Onboarding: any new AI picking up this work must read this file and adhere strictly; sloppy or tag-only edits are unacceptable and block progress.
