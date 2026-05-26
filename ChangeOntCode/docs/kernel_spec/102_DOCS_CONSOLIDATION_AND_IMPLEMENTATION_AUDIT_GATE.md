# 102. Docs Consolidation and Implementation Audit Gate

Status: canonical docs-coherence and code-audit gate.  
Date: 2026-05-06  
Claim boundary: documentation target state; not runtime validation or benchmark evidence.

## Purpose

This file consolidates the active documentation state so the next phase can be a code-vs-doc audit rather than another round of conceptual drift. It defines:

```text
which docs are canonical;
which concepts are target-closed;
which concepts remain formal/empirical/open;
what code must demonstrate before architecture acceptance.
```

It is intentionally not another theory essay. It is the control map for moving from docs to implementation verification.

## Canonical reading order for current kernel work

For the current CO-kernel architecture, use the route in `TheoryOfChange_main/00_Meta/CANONICAL_REFERENCE_STACK.md`. Within `ChangeOntCode/docs/kernel_spec/`, the implementation-audit stack is:

```text
1. 00A_DOCS_READING_GUIDE.md
2. 01B_TARGET_ARCHITECTURE_CONTRACT.md
3. 17_COMPONENT_CLASSIFICATION.md
4. 96_CONCEPTUAL_CLOSURE_LEDGER.md
5. 95_KERNEL_STRUCTURE_CARRIER_ALIGNMENT.md
6. 102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
7. 03C_IMPLEMENTATION_FIDELITY_STATUS.md
8. Concept-specific target docs:
   - 84 / 86 for burden
   - 99 for relation algebra
   - 97 for quotient/equivalence
   - 98 for recursion demand
   - 91 for earned collapse
   - 100 for shape/formula/evidence status
   - 101 for algorithm comparison and consciousness boundary
   - 103 for dynamic shape field target contract
   - 104 for dynamic shape update microcase expectations
```

The files above are the active target-state docs. Any remaining document that conflicts with this chain must be corrected or removed before implementation-audit work proceeds.

## Active execution-loop target

The active kernel execution loop is:

```text
0. Problem state / observation
1. Boundary / Adapter
2. Candidate Surface
3. Continuation Identity Construction
4. Burden Interpretation
5. Burden Operation Typing
6. Relation Surface
7. Recursive Continuation Field
8. Collapse Certificate
9. Commitment Surface / Readout
10. Environment update / next loop
```

This is the positive current target: explicit burden, relation, field, certificate, and commitment carriers are required in the evidence-bearing path.

## Layer boundary

```text
Boundary / Adapter:
  exposes public transformation grammar, legal actions, observations, task anchor, hidden/public distinction, and public_effect facts.
  It must not rank, solve, choose, or leak hidden policy.

Kernel:
  constructs continuation identities, branch-internal burden operations, cross-branch relations, field state, quotient/grey/recursion structure, and earned-collapse certificates.

Readout:
  expresses an earned collapse as a native action. It must not rescue the kernel with first-legal, greedy, uniform, or non-CO rescue selector behavior.

Experiment:
  tests whether the implementation behaves as the docs specify. Reward/performance is interpretable only after boundary, relation, certificate, formula, and fail-closed audits pass.
```

## Canonical component classification

```text
Core primitives / operations:
  Bend
  Gauge / HAQ tolerance
  Temporal Retention
  ReID / Identity-through-change
  Remaining Transformation Burden
  Change Operators
  Closure / Quotient
  Thin Collapse

Mechanism bundle:
  Recursive Continuation Field

Runtime surfaces:
  CandidateSurface
  RelationSurface
  CollapseCertificate
  CommitmentSurface
  ContinuationState

Boundary / translation:
  adapters
  problem contracts
  observation/action mapping
  public_effect publication

Investigatory or secondary:
  MDL/compressibility
  loopiness
  creative option birth / variable birth
  dissociation-style cascades
  full CO-math formalization
  consciousness bridge
```

Runtime surfaces are not deep ontology elements. They are implementation carriers for primitive/element operations.

## Status of concepts

### Target-closed for current implementation audit

These are closed enough that code should be audited against them:

```text
kernel boundary;
branch is not action;
burden core definition;
public fact vs policy advice;
RelationSurface is kernel-side;
branch-internal burden operations are first-class carriers;
weak decision-slot competition is not strong rivalry;
grey preservation is not indecision;
thin collapse is not argmax;
no non-CO rescue selector in evidence-bearing CO runs;
consciousness is out of current evidence scope.
```

### Target-specified but still formally/empirically open

These have target-state docs, but still require formal refinement or empirical validation:

```text
complete burden operation composition laws;
minimal/compositional relation algebra;
exact quotient/equivalence tolerance;
recursion scheduler and budget distinct from search/lookahead;
six-question prior minimality, independence, and sufficiency;
persistent dynamic shape/coarseness field implementation and update law;
full formula ledger and coefficient calibration;
dynamic shape update formula ledger entries;
full RCF comparison against known algorithms;
meaning/consciousness theory beyond continuation relevance.
```

These open items do not block a code-vs-doc audit. They do block final paper claims if presented as solved.

## Implementation audit gate

The docs are coherent enough to proceed to implementation audit only if the following can be checked file by file:

```text
1. Every active code path has a canonical doc target.
2. No active code path performs undocumented policy ranking, hidden solver logic, or non-CO rescue selector.
3. Candidate/action labels are not treated as branch identity unless no stronger identity carrier exists and the degenerate condition is logged.
4. Public effects are classified as public grammar, not policy advice.
5. Branch-internal burden operations survive even when no cross-branch relation is derived.
6. Cross-branch relations are typed and derived from public burden/effect facts.
7. Weak decision-slot competition is telemetry/procedural context, not a collapse blocker.
8. RCF field changes are traceable to burden operations and/or relation topology.
9. CollapseCertificate preserves structured reasons, not only scalar scores.
10. CommitmentSurface respects certificate gates and does not choose by simple argmax or rescue selection.
11. Every readout-affecting scalar has at least a ledger entry or is marked provisional/non-paper-safe.
12. Tests/diagnostics exist for the corresponding carrier.
```

## What to do when code conflicts with docs

When an implementation file conflicts with the target docs, choose one of four outcomes:

```text
patch code to match docs;
update docs if the code reveals a valid conceptual correction;
mark the path investigatory/non-evidence-bearing;
remove or quarantine inactive residue.
```

Do not leave undocumented mismatches in the active path.

## What not to do

```text
do not add another meta-file when an existing canonical doc can be updated;
do not promote investigatory mechanisms because they exist in code;
do not treat status/audit files as conceptual definitions;
do not use performance to justify undocumented kernel behavior;
do not claim final mathematical or consciousness conclusions from current kernel traces.
```

## Definition of docs-complete-enough

The docs are complete enough for the next implementation phase when:

```text
the execution loop is explicit;
component classifications are explicit;
open conceptual/formal/empirical items are marked;
inactive terms are marked as inactive or aliases;
every active mechanism has a canonical target doc;
and the implementation audit can be performed without asking what the code is supposed to mean.
```

This file declares that target after the 2026-05-06 consolidation pass, with the remaining open items scoped rather than hidden.


## 2026-05-18 dynamic-shape clarification

After `022A_S-DR-shape-space-directed-unfolding-from-change`, the canonical docs distinguish:

```text
shape-as-such: invariant fact of structured continuation;
problem-shape prior: fixed public six-question regime descriptor;
local shape-state: future dynamic relational-gauge/coarseness state;
current implementation: static prior + local shape-gauged readout, not persistent DynamicShapeField.
```

`103_DYNAMIC_SHAPE_FIELD_CONTRACT.md` and `104_DYNAMIC_SHAPE_UPDATE_MICROCASE_EXPECTATIONS.md` define the future target and pre-implementation gates. They do not authorize changing runtime shape state until the contract is implemented and tested.
