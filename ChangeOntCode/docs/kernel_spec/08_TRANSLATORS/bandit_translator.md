# Bandit Translator (v1)

## Purpose
Produce per-arm action scores for bandit-family tasks using only bandit-visible statistics, and optionally return a blocklist mask (typically empty).

## Inputs (exact keys/types; where read from)
From observation envelope:
- `family: str` = `"bandit"`
- `t: int`
- `n_arms: int` (required)
- Optional: `action_space: List[int]` (if provided, defines the valid arm IDs)

From primitives:
- `bandit_stats` (canonical primitive name in current code/config; if absent, translator must still return a valid score map)
  - Must contain per-arm counts and mean rewards (exact internal structure is code-defined, but it must be derivable solely from bandit feedback).

From signals (optional hints; never required):
- May read `signals["EB_GHVC.pressure"]` / `signals["EA_HAQ.novelty"]` etc. as soft modifiers, but must remain well-defined if missing.

## Outputs (exact return fields)
Returns a triple:
- `scores: Dict[int, float]` — mapping arm_id → score
- `translator_mask: Set[int]` — blocklist of forbidden arm_ids (usually empty)
- `info: Dict[str, Any]` — optional debug info (may be empty)

## Mask contract (binding v1)
- `translator_mask` is a **blocklist** over the **global bandit action domain** (arm IDs).
- Any arm in `translator_mask` is invalid and must not be selected by ActionHead (even under classical fallback).
- For standard bandits, all arms `0..n_arms-1` are valid, so the mask should be empty.
- If `action_space` is provided, any arm not in `action_space` must be masked.

## State mutation (what is allowed to change; where state is stored)
- Translator must not mutate primitives or header state.
- Bandit stats updates occur in runner/agent update paths, not inside translator.

## Algorithm (step-by-step; include constants/thresholds if binding)
v1 scoring rule is intentionally simple and implementation-flexible, but must be **deterministic** given inputs.

1) Determine valid arms:
   - If `action_space` provided: `A = action_space`
   - Else: `A = [0, 1, ..., n_arms-1]`

2) Build mask:
   - `translator_mask = {a | a not in A}` (usually empty)

3) Compute a score for each `a in A` using available stats:
   - If `bandit_stats` provides (count[a], mean[a]):
     - Score may be UCB-style: `mean[a] + bonus(count[a], t)`
     - Bonus must be defined even when count[a]==0 (treat unseen as high bonus).
   - If stats missing:
     - Use fallback uniform scores: `scores[a] = 0.0` for all a in A.

4) Return `(scores, translator_mask, info)`.

## Forbidden (explicit anti-smuggling rules)
- Must not use hidden environment state (no oracle reads).
- Must not invent additional rewards or peek at true arm probabilities.
- Must not write to `co_bus` (translator is pure scoring + mask).

## Telemetry (exact metrics.jsonl / co_debug fields and signals dict keys)
- Translator does not emit telemetry directly.
- ActionHead may log mask debug fields if enabled.

## Acceptance (exact reviewer procedure)
- Run `ChangeOntCode/outputs/verify/configs/qa_bandit.yaml`.
- Ensure at least one `co_debug` line exists.
- `bash ChangeOntCode/tools/qa.sh` must pass (mask semantics should pass trivially for bandit).