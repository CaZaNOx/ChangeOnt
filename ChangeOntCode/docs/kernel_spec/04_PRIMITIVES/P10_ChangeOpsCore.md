# P10 ChangeOpsCore
Current classification: **Provisional**

Architecturally justified shared persistence surface, but more runtime-support than settled ontological core.

## What this primitive is
P10 is the canonical shared persistence surface for reusable local structural units discovered by change-sensitive mechanisms. In plainer terms: when the kernel admits a prototype-like local pattern that must survive across steps and be shared across mechanisms, P10 is the place where it lives.

## Why this primitive exists
If change can yield reusable motifs, prototypes, or locally stable structural units, the runtime needs one canonical place to keep them. Otherwise:
- each element grows its own hidden store,
- the same structure is duplicated under different names,
- and the architecture loses both transparency and parity.

P10 exists to prevent that fragmentation.

## What P10 is not
P10 is not:
- the birth mechanism itself,
- the merge decision itself,
- an element,
- or an action policy.

It is the shared persistence substrate for the outputs of those mechanisms.

## Inputs and outputs
**Inputs:**
- accepted birth payloads,
- trace-derived prototype candidates,
- merge/split commands from consuming mechanisms.

**Outputs:**
- canonical prototype store,
- prototype count,
- append/merge/split operations,
- stable shared access surface for downstream users.

## Invariants
1. **Single canonical store:** prototype-like persistent units must not be silently duplicated across hidden element-local stores.
2. **Mutation transparency:** additions, merges, and splits should be attributable to explicit mechanism outputs.
3. **Reuse over reinvention:** downstream consumers should read from the shared store rather than recreating equivalent hidden versions.

## Why this matters philosophically
P10 is not itself a deep ontological primitive. It is a runtime primitive in the engineering sense: the minimum shared persistence surface needed if later change-derived structures are to be real for the kernel rather than fleeting one-step conveniences.

## Current implementation status
Architecturally justified and worth keeping. The name may later be refined, but the role is valid.