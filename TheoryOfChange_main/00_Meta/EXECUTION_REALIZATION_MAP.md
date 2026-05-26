# Execution Realization Map

This note maps the **execution-relevant philosophical core** to the layer where each principle should be realized.

Working rule:
- Every execution-relevant philosophical principle must appear somewhere in the executable architecture.
- **Not every principle should become a standalone primitive.**
- The legitimate execution loci are:
  - **runtime invariant / update discipline**
  - **kernel substrate / field state**
  - **kernel primitive**
  - **element**
  - **runtime surface / support surface / header / translator boundary**

A principle is missing if it affects behavior but appears nowhere in those loci.
A principle is misplaced if it is forced into a primitive or element when it really belongs to substrate, invariant, or surface semantics.

## Canonical map

| Philosophical principle | Canonical theory anchors | Proper execution locus | Downstream implementation expectation | Current status |
|---|---|---|---|---|
| Ontological continuity / non-cessation | `[[01_Statements/00_Opening_Justification/008_S-FT-continuity-noncessation]]`, `[[01_Statements/Clarification/S-CL-ontological-continuity-vs-continuum]]` | runtime invariant / update discipline | no reset-from-stasis semantics; updates must propagate from an already-active unfolding | mostly indirect |
| Non-total-erasure / trace-retention | `[[01_Statements/02_Outer_Formation/002_S-DF-non-total-erasure]]`, `[[01_Statements/02_Outer_Formation/003_S-DF-trace-retention]]` | substrate + memory/trace support | retained prior structure must remain available to later comparison, continuity, and action | partial / proxy |
| Selective recurrence | `[[01_Statements/02_Outer_Formation/010_S-DF-selective-recurrence]]` | substrate + recurrence bookkeeping + summary signals | recurrence should be represented without assuming all return is the same kind | partial |
| Embedded stabilized layers | `[[01_Statements/Definition/S-DF-embedded-stabilized-layers]]` | metaheader / translator priors / substrate context | inherited stable embedding must be representable without smuggling hidden facts | partial |
| Border / localization | `[[01_Statements/02_Outer_Formation/009_S-DF-bounded-local-hold]]`, `[[01_Statements/02_Outer_Formation/015_S-DR-boundary-before-identity]]` | substrate + boundary contracts + local neighborhoods | only bounded local unfolding should be represented directly; no global god-view state | partial |
| Identity-through-change | `[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change]]` | identity path semantics, not one primitive alone | persistence must be tested through transformation, not static equality | partial |
| Similarity | `[[01_Statements/02_Outer_Formation/023_S-DF-similarity-operator]]` | foundational operator / primitive support | compare retained-vs-altered structure, not static geometric nearness | partial / proxy |
| Identity-admissibility | `[[01_Statements/02_Outer_Formation/024_S-DF-identity-admissibility]]` | substrate field + recognition logic | borders are tolerated regions before sharp thresholds | partial |
| Local reach | `[[01_Statements/02_Outer_Formation/006_S-DF-reach-relation]]`, `[[01_Statements/02_Outer_Formation/007_S-DF-localreach-zone]]` | substrate neighborhood structure + boundary contracts | local neighborhood and reachability must be represented before global geometry | partial |
| Local comparability field | `[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field]]`, `[[01_Statements/Definition/S-DF-metric-like-comparability-strengthening]]` | substrate field + primitive support | represent directional burden/comparison before full metric geometry | partial |
| Self-propagating selective retention | `[[01_Statements/Definition/S-DF-self-propagating-selective-retention]]` | substrate update law + economy signals | carry-forward must be selective, lossy in some respects, and stability-aware | weak / mostly implicit |
| Remaining transformation burden | `[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden]]` | branch-internal burden carriers + RelationSurface + RecursiveContinuationField + CollapseCertificate | represent continuation-relevant de-centering / anchored operative tension without reducing it to reward cost | active first-pass carriers; formula grounding incomplete |
| Operative difference | `[[01_Statements/02_Outer_Formation/018_S-DF-operative-difference]]` | substrate field + runtime comparison discipline | distinguish continuation-relevant difference from idle variation by admissibility and burden effects | explicit in theory-main; runtime partial |
| Operative invariant | `[[01_Statements/02_Outer_Formation/019_S-DF-operative-invariant]]` | substrate field + invariant-selector discipline | preserve what currently matters for admissible continuation, not every recurring feature equally | explicit in theory-main; runtime partial |
| Regime signature | `[[01_Statements/02_Outer_Formation/020_S-DF-regime-signature]]` | substrate regime state + header surface | represent local pattern of operative invariants, burden accumulation, admissibility degradation, openness/coherence, and history dependence | explicit in theory-main; runtime partial |
| Minimal adequate representation | `[[01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention]]` | retention/compression discipline + representation policy | retain only the least structure sufficient for operative continuation in the current regime | explicit in theory-main; runtime partial |
| Thin collapse law | `[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law]]` | header/action surface + representation collapse policy | recover thin classical special cases only when regime signature earns the collapse | explicit in theory-main; runtime partial |
| Regime-shape variation | `[[01_Statements/Definition/S-DF-regime-shape-variation]]` | header/metaheader/surface layer + substrate context | local mode of unfolding must be representable as a changing regime-shape, not just a fixed backdrop | partial |
| Kernel substrate as bounded local unfolding | `[[01_Statements/02_Outer_Formation/017_S-DF-bounded-local-unfolding-operative-substrate]]` | substrate (foundational) | code must operate on bounded local unfolding, not a smuggled ready-made world-state | named clearly; not yet fully exploited |
| Bend | `[[01_Statements/Definition/S-DF-prm-bend-metric]]` | kernel primitive | directional deformation burden handle | active proxy |
| Gauge | `[[01_Statements/Definition/S-DF-prm-gauge]]`, `[[01_Statements/Definition/S-DF-gauge-alignment-field]]` | kernel primitive | transport/alignment across local comparison frames | active proxy |
| ReID | `[[01_Statements/Definition/S-DF-prm-reid-kernel]]` | kernel primitive | admissible continuity recognition over transformed local structure | partial |
| EC | `[[01_Statements/Definition/S-DF-elm-ec-identity]]` | element | continuity/fracture/admissibility bundle | active |
| EI | `[[01_Statements/Definition/S-DF-elm-ei-change-operators]]` | element | transformation/motif/composition bundle | active |
| Runtime publication and final commitment | `[[00_Meta/CANONICAL_CORE_AND_INVESTIGATION_PERIPHERY]]`, `[[01_Statements/Definition/S-DF-candidate-surface]]`, `[[01_Statements/Definition/S-DF-commitment-surface]]` | runtime surfaces, not ontology core | CandidateSurface publishes intake rows; CommitmentSurface expresses certificate-gated earned collapse; neither is a hidden policy head | active first-pass surfaces |

## Periphery handling rule

The following remain execution-relevant but should **not** be treated as canonical philosophical defaults:
- `[[01_Statements/Definition/S-DF-prm-mdl-compressibility]]`
- `[[01_Statements/Definition/S-DF-prm-residuation]]`
- `[[01_Statements/Definition/S-DF-prm-loopiness]]`
- `[[01_Statements/Definition/S-DF-elm-ef-router]]`
- `[[01_Statements/Definition/S-DF-hdr-id]]`

For these nodes the philosophical layer should state:
1. the deeper ontological need,
2. the candidate formalization or support role,
3. and whether the code is testing it rather than canonizing it.

## Downstream rule

The kernel docs must mirror this map.
- If philosophy treats something as a **deeper need**, docs must name that need first.
- If philosophy treats something as a **candidate formalization**, docs must not silently present it as the only or final truth.
- If philosophy treats something as a **surface**, docs must not present it as an ontology mechanism.


## Code-location rule (2026-04-19)

Execution-relevant philosophy must map to one of these code loci only:
- boundary
- placement
- kernel primitive
- kernel element
- runtime surface
- runtime support

Support surfaces such as candidate publication and commitment are not kernel elements and must not be stored under `core/elements/`. Runtime support utilities such as buses, visit trackers, n-gram memory, and budget ledgers are not primitives and must not be stored under `core/primitives/`.
