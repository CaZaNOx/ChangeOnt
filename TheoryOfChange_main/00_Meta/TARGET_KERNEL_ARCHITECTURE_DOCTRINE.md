# Target Kernel Architecture Doctrine

Status: active bridge doctrine from `_main` concepts to the current kernel-doc target.  
Last live-read correction: 2026-05-15.  
Claim boundary: operational target doctrine, not empirical proof.

This file states the current target architecture for the solver side of the project. It is not a replacement for Layer 1. It is a bridge from the first-layer ontology and primitive/element admissions into the executable kernel loop.

## What the kernel is meant to be

The kernel is not meant to be:

- a family-specific heuristic stack;
- a policy router hidden behind translation;
- a passive evaluator of candidates whose geometry is already solved at the adapter boundary;
- a generic planner or fallback selector with CO vocabulary attached.

It is meant to be:

- a change-first structured runtime;
- operating on lawful public problem structure;
- preserving continuation-relevant burden, relation, grey, quotient, and collapse structure until compression is earned.

## Current target law

The current target law is:

```text
public problem structure is not enough for commitment until the kernel has formed
continuation identity, burden operations, relation topology, field state, and an
earned-collapse certificate.
```

That means candidate rows, local scores, legal actions, and placement controls may shape the runtime, but they may not already contain the final policy verdict.

## Canonical execution loop

The active runtime target is:

```text
0. Problem state / observation
1. Boundary / Adapter
2. CandidateSurface
3. Continuation Identity Construction
4. Burden Interpretation
5. Burden Operation Typing
6. RelationSurface
7. RecursiveContinuationField
8. CollapseCertificate
9. CommitmentSurface / Readout
10. Environment update / next loop
```

This is the same target formalized operationally in:

```text
ChangeOntCode/docs/kernel_spec/01B_TARGET_ARCHITECTURE_CONTRACT.md
ChangeOntCode/docs/kernel_spec/102_DOCS_CONSOLIDATION_AND_IMPLEMENTATION_AUDIT_GATE.md
```

## Stage meanings

### 1. Boundary / Adapter

The boundary exposes lawful public structure:

- current public observation;
- legal/admissible candidate expressions;
- task or continuation anchor;
- hard constraints and visible costs;
- hidden/public distinction;
- public burden/effect facts.

It may not expose optimality, hidden-state policy, shortest-path answers from unavailable topology, baseline values, threshold verdicts, or post-hoc benchmark tuning.

### 2. CandidateSurface

CandidateSurface publishes candidate rows as thin operational carriers. A candidate row may include an action expression because the environment eventually needs an action, but candidate row ≠ continuation branch ≠ final decision.

### 3. Continuation Identity Construction

The kernel derives branch identity from retained continuation-pressure signatures. Identity precedence is:

```text
continuation_id → branch_id → candidate_id → action
```

Action is the last-resort interface alias, not the default branch identity.

### 4. Burden Interpretation

Public facts are interpreted through the continuation anchor. Change-field asymmetry becomes tension; tension becomes burden only when it matters for continuation, stabilization, transformation, or collapse.

### 5. Burden Operation Typing

The kernel records what each branch does with burden: carry, amplify, expose, buffer, mask/postpone, relieve, cancel, transfer, transform, threshold, or phase-shift.

### 6. RelationSurface

RelationSurface derives typed relations from lawful public burden/effect facts. It distinguishes structural relations from weak procedural decision-slot competition. Weak competition because only one action can be emitted now is not the same as strong continuation rivalry.

### 7. RecursiveContinuationField

RCF updates debt, relief support, grey pressure, recursion demand, collapse readiness, quotient/equivalence markers, and viability from branch-internal operations and relation topology. RCF is a mechanism bundle, not a root primitive.

### 8. CollapseCertificate

CollapseCertificate checks whether compression into one branch is earned. It preserves reasons such as unresolved rivalry, quotient-resolved rivalry, hiddenness, burden blockers, relief/cancellation support, grey structure, recursion demand, fail-closed status, and certificate gates.

### 9. CommitmentSurface / Readout

CommitmentSurface expresses the certified branch collapse as a native action. It must respect certificate gates and may not rescue the runtime with simple argmax, first-legal, greedy reward, uniform, or baseline-policy selection.

### 10. Environment update / next loop

The environment returns the next observation; only then may the next bounded local closure be formed.

## What the architecture must keep separate

The target architecture must keep separate:

- ontology / `_main` conceptual chain;
- operational kernel docs;
- code implementation;
- diagnostics and structural traces;
- empirical reward evidence;
- future conceptual research.

Inside the runtime it must also keep separate:

- public facts from policy advice;
- native action from continuation branch;
- branch-internal burden operations from cross-branch relations;
- weak procedural competition from strong rivalry;
- scalar summaries from the richer structure they collapse;
- final readout from baseline comparison code.

## Primitive and element role inside this architecture

Only change is the deepest ontological primitive.

Later kernel primitives are downstream reusable handles, not coequal deepest primitives. In the current kernel phase they include operational distinctions such as:

- bend / deformation of continuation possibility;
- gauge or HAQ-like tolerance;
- temporal retention;
- identity-through-change / ReID;
- remaining transformation burden;
- change operators;
- closure / quotient;
- thin collapse.

Runtime surfaces instantiate and carry these roles. They are not deep ontology elements.

## Current honest status

The current docs specify a coherent implementation target and the code contains first-pass carriers for the active loop. Structural diagnostics can pass on tested cases. This does not prove empirical usefulness, RCF novelty, final formula grounding, or consciousness claims.

Current open debts include:

- full formula/coefficient grounding;
- quotient/equivalence tolerance calibration;
- recursion scheduler and budget policy;
- multi-step continuation identity;
- known-algorithm comparison;
- controlled empirical validation.

## Canonical code-layer doctrine

Canonical code locations for the active path are:

```text
agents/co/boundary/
agents/co/adapters/
agents/co/placement/
agents/co/core/contracts/
agents/co/runtime/surfaces/
agents/co/runtime/support/
agents/co/integration/
agents/co/tests/
```

A new problem family should require edits only in environment/adapter/boundary registration unless a genuine general kernel gap is found. It should not require family-specific edits in kernel primitives, runtime surfaces, or final readout.
