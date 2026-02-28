# Spec Gaps (Docs vs Code)

This page tracks missing or aspirational features referenced by docs that are not present in the codebase. **Do not implement features just because they appear here**; treat them as planned gaps.

## Missing files referenced by older docs (examples)
The following paths are referenced in some annex/reference docs but do not exist in the codebase (as of current snapshot):
- `core/headers/collapse.py`
- `core/headers/meta_flip.py`
- `core/quotient/equivalence.py`
- `core/quotient/infimum_lift.py`
- `evaluation/invariance_test.py`
- `tests/test_lift.py`
- `tests/test_logic.py`

## Moved paths (docs need redirects)
Some older docs reference outdated paths. Use the canonical paths:
- Registry: `agents/co/registries/registry.yaml`
- CO builder: `agents/co/integration/core_builder.py`
- Translators: `agents/co/integration/translators/`

## Duplicates (archived)
The following docs are historical/legacy and should remain under `annex/history/`:
- `Master.md`
- `grouped.md`
- `FREEZE_*` docs

## Policy
- Binding truth lives in spine pages only.
- Annex docs may contain aspirational specs; treat them as reference/history unless explicitly upgraded into binding spec.
