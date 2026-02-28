# Target Kernel Table

## Purpose

This page gives a compact target overview of the current intended ChangeOnt kernel architecture.

It is not a replacement for the detailed doctrine docs.  
It is the quick reference table for:
- what layers exist
- what their roles are
- what is currently present
- what is still missing

---

## Layer Table

| Layer | Unit Type | Role | Current Status |
|---|---|---|---|
| 0 | Primitives | reusable semantic ingredients | partially present |
| 1 | Semantic combinators | reusable law-forms for primitive interaction | mostly missing / underdeveloped |
| 2 | Elements | semantically meaningful mechanisms built from primitives via combinators | partially present |
| 3 | Bus | transport/storage surface for votes and signals | present |
| 4 | Header | internal control under detected stability | present in minimal form |
| 5 | Meta-header | external prior/control layer | conceptually present, not yet well separated |
| 6 | Translators + Action surface | task interface and final action emission | present |

---

## Primitive Table

| Primitive | Role | Status |
|---|---|---|
| P1 BendMetric | bend/difference comparison primitive | present |
| P2 Gauge | modulation/re-weighting primitive | conceptually valid, formula not frozen |
| P3 MDL | complexity/compressibility pressure primitive | present in minimal form |
| P7 Precision | scale/precision/coarse-graining primitive | present in partial form |
| P8 Loopiness | recurrence/revisit primitive | present / conceptually valid |
| P10 ChangeOpsCore | canonical prototype/state-support primitive | present |
| P12 ClosureQuotient | local closure/grouping primitive | present in minimal form |

### Primitive candidates likely needed later
| Candidate | Role | Status |
|---|---|---|
| Branching primitive | divergence / 1-to-n structural support | not yet explicit |
| Convergence primitive | n-to-1 / local closure pressure | not yet explicit as separate primitive |
| Temporal persistence primitive | depth / carry / persistence support | not yet explicit |
| Local topology primitive | neighborhood / local shape support | not yet explicit |
| Coupling primitive | cross-influence strength support | not yet explicit |

---

## Element Table

| Element | Role | Status |
|---|---|---|
| EA_HAQ | history-adaptive modulation mechanism | present |
| EB_GHVC | birth pressure / structure-admission mechanism | present |
| EC_Identity | local identity mechanism | present |
| EG_DensityPrecision | density/precision mechanism | present |
| EH_BreadthDepth | breadth/depth scheduling mechanism | present but not central |
| VoteBridge | bridge from mechanism output to bus votes | present |
| ActionHead | final action surface | present |
| EF_Router | reserved future routing mechanism | non-central / future |

---

## Header Table

| Header | Role | Status |
|---|---|---|
| H_SSI | default internal stability-sensitive control header | present |
| H_CS | classical-slice / reduced-CO control header | present |
| H_ID | identity-sensitive control header | present |

---

## Runtime vs Semantic Combinator Table

| Type | Role | Current Status |
|---|---|---|
| Runtime combinators | execution orchestration | present (`C_Pipeline`) |
| Semantic combinators | law-forms of primitive interaction | mostly missing / underdeveloped |

---

## Current Architectural Conclusion

The kernel currently has:
- a working v1 primitive/element/header/action slice
- working runtime orchestration
- working QA/spec gating

The kernel does **not yet** have:
- a properly realized semantic combinator layer
- fully explicit primitive → combinator → element contracts
- a clearly separated meta-header implementation
- a finalized primitive set

---

## Binding Development Priority

The intended order of strengthening is:

1. architecture doctrine  
2. primitive role doctrine  
3. semantic combinator doctrine  
4. element contracts  
5. header/meta-header separation  
6. code refactor toward explicit declared dependencies  
7. experiment framework for element/combinator/weight comparisons

This table is a quick alignment aid, not the full argument.