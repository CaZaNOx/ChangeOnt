# CO Math Alignment and Critique

**Status: critique / exploratory constraint, not a current implementation override.**

This file records mathematical directions and risks that constrain future claims. It does not replace the active runtime loop.

This note records the main mathematical direction found in the project and the main criticisms that should constrain implementation claims.

## 1. Strong alignments in the project material

Across the theory and kernel docs, the strongest aligned math directions are:
- **derived rather than assumed geometry**: metric/comparability emerges from LocalReach + similarity rather than being assumed primitive;
- **topology from reach/neighborhood structure**: LocalReach is the substrate before metric;
- **path algebra over ring algebra**: choice and sequence are distinct; non-invertibility is default;
- **graded / quantale-style logic**: evidence composition and residuation are more appropriate than Boolean flatness in many CO contexts;
- **quotienting / closure / gauge** as typed operators for identity under tolerated deformation;
- **local rather than global formal guarantees**: many structures are local, resolution-dependent, and earned only when the field supports them.

## 2. Stronger than the code currently is

The project’s math story is currently stronger than the code in at least three ways:
- the theory treats topology, quotienting, and gauge as structurally primary, while the code still often works with flat local scores;
- the theory distinguishes path logic from Markov/local score logic more sharply than the current runtime does;
- the theory’s math is change-first, but the code still lets classical/state-local scaffolds carry too much of the actual solving power.

## 3. Main critique points

### 3.1 “Metric” is sometimes asserted too early
Several statements correctly say metric comparability is derived. That discipline must be preserved.

If a current implementation just names some score a “distance,” that does not yet earn metric language. At best it may have earned:
- similarity;
- pseudometric;
- quasi-metric;
- local ordering.

### 3.2 Manifold language is often still metaphorical
The manifold notes are useful, but many uses remain explanatory rather than operational.

Until the project specifies:
- charts / coordinates;
- transition conditions;
- what carries smooth structure;
- and what empirical invariants justify that language,

“manifold” should remain a cautious model, not a free default claim.

### 3.3 Quantale / semiring language is promising but not yet fully earned
The project is right to reject ring-like flattening and to distinguish choice from sequence.

But it should avoid pretending one final universal algebra has already been found. The current healthiest stance is:
- typed roles first;
- local laws second;
- full algebraic unification only after those laws are live and falsifiable.

### 3.4 Loopiness needs a tighter definition
The project contains both:
- topological loopiness / cycle richness;
- motif recurrence / recurrent compressibility;
- attractor recurrence not reducible to literal loops.

These must not be conflated. Otherwise the code will reward or punish recurrence for the wrong reason.

### 3.5 Attractor language also needs discipline
Attractors may be:
- explicit fixed basins;
- symbolic or quotient-space recurrences;
- graded betterment fields;
- shifting or uncertain goals.

The code should therefore avoid treating every task as “fixed target minimum” unless the task genuinely supplies that structure.

## 4. Implementation consequence

The clean implementation consequence is:
- translators expose observable structure;
- kernel earns its own effective geometry;
- metrics, closure, quotienting, and gauge are treated as typed, auditable operators;
- claims of manifold/metric/algebraic structure are made only when the implementation has actually earned them.
