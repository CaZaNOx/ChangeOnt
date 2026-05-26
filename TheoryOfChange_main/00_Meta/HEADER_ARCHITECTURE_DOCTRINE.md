# Header Architecture Doctrine

Headers are a weird case because they sit between ontology and embedded access.

The project is **not** trying to choose arbitrary control layers. It is trying to discover the mechanisms by which change unfolds, stabilizes, and reopens — while also admitting that any real problem is encountered from inside many already-stabilized layers of change.

A local solver never encounters bare undifferentiated change. It encounters change through inherited collapse layers:
- physics already stabilized enough for chemistry;
- chemistry already stabilized enough for biology;
- biology already stabilized enough for nervous systems;
- nervous systems already stabilized enough for culture, games, institutions, and conventions.

The header stack is therefore the current representation of two coupled facts:
1. there is a **real ontological mechanism** by which unfolding hardens, stabilizes, becomes brittle, and locally behaves classically;
2. the current problem usually lives **inside prior stabilizations** that can honestly be treated as inherited structure.

## 1. Metaheader — inherited stabilized embedding structure
Metaheader encodes slow or effectively fixed structural facts of the embedding layer that any honest solver may rely on.

Examples:
- board size or action schema;
- rule persistence across one game or episode;
- fixed legal move grammar;
- persistent constraints of a problem family;
- known low or high plausibility of ontological mutation during one run.

Metaheader is not just metadata. It is the current representation of **prior collapses already sedimented into the local task space**.

## 2. Regime header — live collapse vs reopening estimate
The regime header is the live estimate of how the current local field is behaving **within** that inherited embedding.

It tracks things like:
- current dynamicity or brittleness;
- operative-invariant stability;
- burden accumulation and admissibility degradation;
- reopening pressure;
- how much existing closure may be trusted;
- how much monitoring, reevaluation, or tolerance widening is warranted.

Ontologically, this role is closer to a regime-signature / collapse-tracking process than to a static box. "Header" is therefore partly a representational interface for readers and implementation rather than the deepest ontological category.

## 3. Algebra mode — current collapse-adequate composition semantics
Algebra mode is the current representation of how composition should be carried out if the space is being treated as more classical, more path-sensitive, more spread-bearing, or more non-Boolean.

This includes layers such as:
- path algebra (`classical` vs `minplus` or related path-sensitive forms);
- number arithmetic (`classic` vs `spread` or bounded relational forms);
- logic (`boolean` vs graded/quantale-like forms).

The point is not free choice. The point is that **classical composition should emerge as a special collapse of a broader change-native structure**, and the local solver must represent which collapse regime it is currently approximating.

## Order of dependence
- inherited stabilized embedding constrains plausible regimes;
- regime header estimates current collapse vs reopening inside that embedding by summarizing operative invariants, burden/admissibility pressure, and history dependence;
- algebra mode expresses the composition semantics currently adequate to that regime;
- primitives/elements then operate under that approximation of unfolding.

## Current implementation note
The current runtime stores much of this inside a unified header stack. That is acceptable as an operational approximation, but canonically the project should keep distinct:
- inherited stabilized embedding structure,
- live regime estimation,
- current algebra/composition semantics.
