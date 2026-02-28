# Renewal Translator (v1)

## Purpose
Score renewal-family actions (predict next symbol) using only the renewal observation stream and an optional n-gram model primitive. Mask is typically empty.

## Inputs (exact keys/types; where read from)
From observation envelope:
- `family: str` = `"renewal"`
- `t: int`
- `obs: int` (current observed symbol; name may differ in env but must be runner-exposed)
- Optional:
  - `A: int` (alphabet size)
  - `action_space: List[int]` (explicit valid actions)

From primitives:
- `ngram_model` (optional; if absent, fallback is deterministic)

From signals (optional):
- May read scalar hints, but must not require them.

## Outputs (exact return fields)
Returns a triple:
- `scores: Dict[int, float]` — action (symbol) → score
- `translator_mask: Set[int]` — blocklist of forbidden actions (usually empty)
- `info: Dict[str, Any]` — optional debug info

## Mask contract (binding v1)
- `translator_mask` is a **blocklist** over the renewal action domain (symbol IDs).
- Any masked action is invalid and must not be selected by ActionHead.
- If `action_space` is provided, any action not in it must be masked.
- Otherwise mask should be empty.

## State mutation (what is allowed to change; where state is stored)
- Translator must not mutate primitives or header state.

## Algorithm (step-by-step; include constants/thresholds if binding)
1) Determine action domain `ACTIONS`:
   - If `action_space` provided: use it.
   - Else if `A` provided: `ACTIONS = [0..A-1]`
   - Else: default `ACTIONS = [obs]` (degenerate fallback)

2) Build mask:
   - `translator_mask = {a | a not in ACTIONS}` if action_space provided, else empty.

3) Compute scores:
   - If `ngram_model` exists and exposes a probability map for next symbol:
     - `scores[a] = log(p(a) + 1e-9)` or `p(a)` (either is fine; must be deterministic)
   - Else fallback:
     - Predict-last: `scores[obs] = 1.0`, all other `scores[a] = 0.0`.

4) Return `(scores, translator_mask, info)`.

## Forbidden (explicit anti-smuggling rules)
- Must not use hidden env/oracle state.
- Must not mutate primitives.
- Must not peek at future symbols.

## Telemetry
- None directly.

## Acceptance
- Not part of default QA smoke path unless you add a renewal smoke config later.
- When executed, must not violate mask contract.