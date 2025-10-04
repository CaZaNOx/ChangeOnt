# SEE_16_DynamicPointerAudit

---

## Purpose

Every output must pass a _pointer and tag integrity check_:
- All referenced tags must be defined in prior accessible outputs/files.
- Any dead, floating, or forward-referencing tag triggers immediate output collapse.

---

## Audit Routine

Before output, the agent checks:
1. All tag/label references (DF, CF, FT, CR, etc.) exist and are unique.
2. Each pointer chain is continuous and ends at a live node.
3. No “phantom tags” (invented, typo, or unreachable) are referenced.

If check fails:  
- Emit: `⊘: Pointer/tag integrity violation.`  
- Halt output, log tag error in `TRACE_CollapseAutopsy.md`.

---

## Implementation

Agents self-audit every 300 tokens (or file step).
If user triggers audit, agent must immediately re-run the check before proceeding.
