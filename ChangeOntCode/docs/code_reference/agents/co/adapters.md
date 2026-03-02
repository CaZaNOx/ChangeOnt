# docs/code_reference/agents/co/adapters.md

# CO Adapters

## Purpose

The adapter layer is the runner-facing interface for CO.

Adapters are responsible for:
- receiving family-local runner input,
- invoking translator/kernel-facing logic,
- preserving the select/update loop,
- and returning concrete action-relevant information back to the runner.

They are the immediate bridge between:
- family runners
and
- the CO kernel runtime path.

---

## Why this layer exists

The CO kernel should not be directly coupled to:
- maze-specific action formats,
- bandit-specific reward bookkeeping,
- renewal-specific sequence/event shapes.

Adapters isolate the family-specific execution loop from the kernel’s internal representation and contracts.

---

## Canonical responsibilities

**Binding**

Every adapter must do all of the following:

1. receive family-local observation/input from a runner
2. call the appropriate translation/kernel path for selection
3. return an action or action-relevant structure to the runner
4. receive feedback after environment execution
5. translate or package update-relevant information back into the kernel update path
6. preserve structural continuity across the select → act → feedback → update loop

---

## Main files

### `bandit_adapter.py`
Bandit-family CO adapter.

#### Expected role
- shape bandit-local runner information into kernel-facing select calls
- return an arm/action choice
- receive reward/feedback and propagate update information to the kernel

#### Why needed
Bandit tasks expose a specific local structure:
- arm selection
- reward
- counts/statistics
- usually no spatial branch graph

The adapter must bridge that into the CO internal path-space form without silently reducing CO to bandit-native state assumptions.

#### Current target-state requirement
The bandit adapter must preserve enough structural context that:
- primitives/elements are not starved,
- update logic is not reduced to shallow reward-only bookkeeping,
- and translator/primitive mismatches are not hidden.

---

### `maze_adapter.py`
Maze-family CO adapter.

#### Expected role
- shape maze-local observation into kernel-facing selection input
- return a concrete move/action
- receive movement result / terminality / local feedback
- feed structurally relevant update information back to the kernel

#### Why needed
Maze tasks are structurally richer:
- local branching
- revisitation
- path geometry
- obstacles / constraints
- goal-directed continuation bias

This family is especially important for CO because many path-structural concepts are easier to express here than in bandit.

#### Current target-state requirement
The maze adapter must:
- preserve enough path/branch structure,
- prevent trivial oscillatory failure loops where possible,
- and not reduce the update path to thin “t+1” style payloads.

---

### `renewal_adapter.py`
Renewal-family CO adapter.

#### Expected role
- shape sequence/event-local information into kernel selection input
- return the next predicted symbol/action class or equivalent concrete action
- translate resulting feedback into update-relevant kernel information

#### Why needed
Renewal tasks emphasize:
- recurrence
- structure in unfolding sequences
- return/diversity
- closure and compressibility signals

This makes them important for testing sequence-sensitive CO mechanisms.

#### Current target-state requirement
The renewal adapter must:
- preserve enough sequential structure for recurrence-sensitive mechanisms,
- not collapse to shallow “last symbol only” behavior unless justified by regime/classical collapse,
- and expose enough information for honest comparison with renewal STOA baselines.

---

### `probes.py`
Probe-related helper logic for adapters.

#### Expected role
A place for adapter-side probe extraction or structured family-local signal preparation.

#### Status
- **Recommended canonical support location** if probes are used in runtime
- **Experimental** if probes are not yet fully canonicalized

---

## Contracts

### Select contract
**Binding**

During selection, the adapter must:
- package family-local observation into a translator/kernel-relevant form,
- call the active CO runtime path,
- and return action-relevant output to the runner.

### Update contract
**Binding**

During update, the adapter must:
- preserve enough continuity from the previous select call and resulting environment feedback,
- avoid starving the kernel of structure,
- and update through the documented kernel update path.

---

## Current misalignment checks

The adapter layer is misaligned if:

- it bypasses the canonical kernel contracts,
- it sends only trivial update payloads that erase meaningful structure,
- it silently reduces CO to family-local action heuristics,
- or it makes some elements appear active while denying them the information they require.

---

## Status summary

- Adapters are **Binding runtime infrastructure**
- richer probe handling remains **Recommended starting point** unless fully frozen
- any family adapter that starves the kernel while pretending to support rich mechanisms is a real misalignment