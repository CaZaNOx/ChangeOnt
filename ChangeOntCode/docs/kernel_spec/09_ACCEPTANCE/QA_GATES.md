# QA Gates

## Mandatory Gate
- `ChangeOntCode/tools/qa.sh` must pass before merge.
- `ChangeOntCode/tools/spec_gate.sh` must pass before merge.

## What QA Checks
- Header record existence
- Header update source (when present)
- Required signals keys
- Identity variation and last_d positive
- GHVC birth suggest + birth_count change
- Mask semantics
- Exactly one co_debug per t

## What SPEC_GATE checks
- Static grep: fails if any of these appear in ChangeOntCode/agents/co:
  - `primitives["P10"]`, `primitives["P12"]`, `identity_mem`, `update_from_primitives`
- Runtime mask rule: if translator_mask present and non-empty, action must not be in translator_mask unless translator_mask_blocks_all == 1.
