# Maze Translator (v1)

## Purpose
Score maze actions (moves) using only runner-exposed maze state (pos/goal/grid geometry) and return a **blocklist mask** for invalid moves (walls/out-of-bounds). May incorporate CO hints (density/novelty) as soft modifiers.

## Inputs (exact keys/types; where read from)
From observation envelope (runner-exposed):
- `family: str` = `"maze"`
- `t: int`
- `pos: (int,int)` or `[int,int]` (required)
- `goal: (int,int)` or `[int,int]` (required)
- `width: int`, `height: int` (required if grid-based)
- Optional:
  - `grid: List[List[int]]` (if present: wall layout; exact encoding is env-defined)
  - `action_space: List[str]` (e.g., `["UP","DOWN","LEFT","RIGHT"]`)

From signals (optional hints):
- `signals.get("EG_DensityPrecision.visit_density")` (float)
- `signals.get("EA_HAQ.novelty")` (float)

Important:
- Translator must be well-defined even if signals are missing (treat missing as 0).

## Outputs (exact return fields)
Returns a triple:
- `scores: Dict[str, float]` — mapping action → score
- `translator_mask: Set[str]` — blocklist of forbidden actions
- `info: Dict[str, Any]` — optional debug info

## Mask contract (binding v1)
- `translator_mask` is a **blocklist** over the **global maze action domain** (same action strings ActionHead uses).
- Any action in `translator_mask` is invalid and must not be selected by ActionHead (even after blending).
- Maze mask must include **all** invalid actions deterministically computed from:
  - out-of-bounds moves
  - wall collisions (if grid/spec provides walls)
- Maze: mask must be computed purely from provided `grid/width/height/pos` (no oracle).

## State mutation (what is allowed to change; where state is stored)
- Translator must not mutate primitives or header state.

## Algorithm (step-by-step; include constants/thresholds if binding)
v1 scoring is deterministic and goal-directed, with optional CO hint penalties/bonuses.

1) Determine action set `A`:
   - If `action_space` provided: use it.
   - Else default: `["UP","DOWN","LEFT","RIGHT"]`.

2) For each action `a in A`, compute candidate next position `pos'`:
   - UP: (r-1,c), DOWN: (r+1,c), LEFT: (r,c-1), RIGHT: (r,c+1).

3) Build mask:
   - If `pos'` is out of bounds → mask `a`.
   - If `grid` is provided and `pos'` is a wall cell → mask `a`.
   - Otherwise action is allowed.

4) Base score for allowed actions:
   - Let `d0 = manhattan(pos, goal)`.
   - Let `d1 = manhattan(pos', goal)`.
   - Improvement term: `imp = d0 - d1` (positive if moving closer).
   - Base score: `score = imp`.

5) Optional CO hints (soft modifiers; must be bounded and default to 0):
   - `density = signals.get("EG_DensityPrecision.visit_density", 0.0)`
   - `novelty = signals.get("EA_HAQ.novelty", 0.0)`
   - Apply small penalties/bonuses:
     - `score -= 0.1 * density`
     - `score += 0.1 * novelty`
   (Constants 0.1 are v1 defaults; may be parameterized later via SPEC_GAPS.)

6) Return `(scores, translator_mask, info)` where:
   - `scores` includes only allowed actions (or includes masked actions with very low score; either is acceptable as long as mask is correct).

## Forbidden (explicit anti-smuggling rules)
- Must not use hidden env/oracle state.
- Must not mutate environment or primitives.
- Must not decide the final action; ActionHead decides.

## Telemetry (exact metrics.jsonl / co_debug fields and signals dict keys)
- Translator does not emit telemetry directly.
- Mask correctness may be checked by QA when mask fields are present.

## Acceptance (exact reviewer procedure)
- Run `ChangeOntCode/outputs/verify/configs/qa_maze.yaml`.
- Ensure at least one `co_debug` line exists.
- `bash ChangeOntCode/tools/qa.sh` must pass `mask_semantics`.
- Additionally: grep a `co_debug` line that contains `translator_mask` or mask debug (if enabled) and confirm it blocks walls/out-of-bounds.