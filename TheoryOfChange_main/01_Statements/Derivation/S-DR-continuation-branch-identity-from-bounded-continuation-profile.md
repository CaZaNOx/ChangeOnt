---
id: stmt.continuation-branch-identity-from-bounded-continuation-profile
type: DR
aliases:
- S-DR-continuation-branch-identity-from-bounded-continuation-profile
- ContinuationBranchIdentity
- BranchIdentity
- LiveContinuationBranch
title: Continuation branch identity from bounded continuation-profile
concepts:
- '[[02_Concepts/C-identity-change]]'
- '[[02_Concepts/C-change-trace-invariants]]'
dependencies:
- '[[01_Statements/02_Outer_Formation/012_S-DF-continuation-admissibility.md]]'
- '[[01_Statements/02_Outer_Formation/013_S-DF-local-comparability-field.md]]'
- '[[01_Statements/02_Outer_Formation/014_S-DF-remaining-transformation-burden.md]]'
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
- '[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md]]'
- '[[01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md]]'
- '[[01_Statements/02_Outer_Formation/022_S-DF-thin-collapse-law.md]]'
parents:
- '[[01_Statements/02_Outer_Formation/016A_S-DF-bounded-continuation-profile.md]]'
- '[[01_Statements/02_Outer_Formation/016_S-DF-identity-through-change.md]]'
- '[[01_Statements/02_Outer_Formation/021_S-DF-minimal-adequate-retention.md]]'
successors:
- '[[ChangeOntCode/docs/kernel_spec/17_COMPONENT_CLASSIFICATION.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/47_RECURSIVE_CONTINUATION_FIELD.md]]'
- '[[../ChangeOntCode/docs/kernel_spec/76_CONTINUATION_IDENTITY_AND_RELATION_PUBLICATION_CONTRACT.md]]'
symbols_used: []
sources:
- path: chat/2026-05-06 user requirement that code must follow _main -> docs -> code, and that branch/action distinctions must be conceptually grounded before implementation.
flags: []
tags:
- layer/foundations
- domain/operational
- type/DR
- route/outer
- concept/identity
- concept/continuation
- concept/kernel-bridge
- status/canonical-scaffold
status: canonical-scaffold
---
# Continuation branch identity from bounded continuation-profile

## Claim (formal)
A continuation branch is the minimally retained identity of a live admissible continuation under unresolved change. It is derived when a bounded continuation-profile can remain answerable to identity-through-change while still carrying unresolved transformation burden that has not yet lawfully collapsed into a single action, state, or object.

Formally, a branch is not identical to a one-step native action. It is a retained continuation identity: the least structure needed to keep a live possible way-of-continuing distinct while its support, burden, rivalry, equivalence, or collapse-readiness remains unresolved.

## Philosophical Translation (of formal claim)
When change is still unfolding, the system may have several live ways of continuing. These live ways are not merely the next moves available at the interface. A next move can express a branch, but the branch is the continuing line of meaning or burden that the move belongs to. The branch is what remains answerable through change before final collapse is justified.

## Philosophical Justification
The earlier chain already establishes bounded continuation-profile and identity-through-change. A bounded continuation-profile is not a static object; it is a way a local line continues while remaining answerable to a recurrent profile. Identity-through-change then says sameness must be understood as continuation under transformation, not frozen equality.

Once remaining transformation burden is admitted, a live continuation can preserve support while still owing unresolved deformation. Minimal adequate retention then requires retaining enough structure to track that unresolved continuation without retaining everything. Thin collapse law forbids collapsing this richer structure into a thinner action/state summary until the unresolved structure no longer matters. Therefore, when multiple admissible continuations remain live, each must be retained by a branch identity rather than by a bare action label.

## Explanation (informal)
A branch is the runtime descendant of identity-through-change. It says: “this way of continuing is still live enough that we must keep track of it.” It is thinner than a full simulated future, but richer than an action name.

Examples:

- In maintenance, `RUN` may express stable-operation continuation, hidden-risk continuation, or debt-postponement continuation depending on the public continuation profile. The action label alone is not the branch.
- In a maze, `move east` may express goal-approach, detour, frontier-probe, or dead-end-confirmation continuation. The movement alone is not the branch.
- In bandit, selecting an arm may express exploitation of a stable supported option or sampling to resolve uncertainty. The arm-pull alone is not the branch.

## Derivation (Philosophical)
1. A bounded continuation-profile gives a local line something it remains answerable to across transformation.
2. Identity-through-change forbids treating identity as frozen sameness and instead makes identity depend on supportable continuation.
3. Remaining transformation burden means a continuation can remain locally supported while still unresolved.
4. Minimal adequate retention requires keeping only the structure that still matters for continuation.
5. Thin collapse law allows thinning only when richer live structure no longer changes admissible continuation.
6. Therefore, while unresolved continuation structure still matters, the system must retain branch identities: live continuation hypotheses distinct enough to carry support, burden, debt, rivalry, relief, equivalence, and collapse-readiness.

## Derivation (Formal/Logical/Mathematical)
```text
Let P be a bounded continuation-profile.
Let C_i be an admissible possible continuation under P.
Let B(C_i) be the unresolved transformation burden carried by C_i.
Let R(C_i, C_j) be any live relation that affects admissible continuation
  (rivalry, relief, cancellation, quotient/equivalence, shared evidence, etc.).

A continuation branch Br_i exists when:
1. C_i remains admissible under P,
2. C_i is distinguishable from other live continuations under local comparability,
3. B(C_i) or R(C_i, C_j) remains relevant to future admissible continuation,
4. collapsing C_i into a thinner action/state label would lose operative structure.

Then Br_i is the minimally adequate retained identity of C_i.

If condition (3) fails and thinner retention preserves all operative continuation,
then Br_i may lawfully thin/collapse under thin collapse law.
```

## Operational inheritance
A kernel implementation that inherits this derivation must satisfy these constraints:

1. A branch identifier should name a continuation identity where one is available.
2. Native action labels are interface expressions, not default branch identities.
3. If both `continuation_id` / `branch_id` and `action` are present, the continuation identity has authority over the action label for field interaction.
4. Action labels may be used only as a last-resort provisional identity when no continuation identity has yet been derived.
5. Runs in which branches remain action labels must be reported as provisional continuation-field tests, not full tests of branch-identity doctrine.

## Anti-smuggling boundary
This derivation does not permit the adapter or kernel to invent branch identities from hidden optimal policies. A branch identity must be traceable to public continuation structure: burden type, admissibility, public effect, shared evidence, residual profile, relation scope, or history generated from public observations.

Forbidden branch identities include:

- “best action now,”
- “optimal replacement threshold,”
- “shortest hidden route,”
- “DP-preferred continuation,”
- any branch label derived from hidden simulator state or benchmark outcome.

## Clarifications / Further Context
- A branch is not a metaphysical object. It is a minimal retention structure needed while live continuation remains unresolved.
- A branch can be expressed by multiple actions over time.
- A single action can express different branches in different field contexts.
- Several branches can quotient/merge if their residual continuation profiles become same-enough under active tolerance.
- Branch identity is a precondition for a serious recursive continuation field. Without it, the field risks becoming action-score deformation.

## Counterfactuals
- If branch identity is collapsed to action label by default, the kernel cannot distinguish stable operation from debt-postponement when both use the same action.
- If branch identity is richer than necessary, the kernel retains nonoperative bloat and violates minimal adequate retention.
- If branch identity is inferred from hidden optimality, the translator boundary is violated.

## Next Steps in Chain
- Implementing docs must define how public candidate facts can justify branch identities and branch relations.
- Kernel docs should bind this derivation in a continuation identity and relation-publication contract.
- Code should only be patched after the docs specify the operational schema.

## Tags
#type/DR #layer/foundations #domain/operational #route/outer #concept/identity #concept/continuation #concept/kernel-bridge #status/canonical-scaffold
