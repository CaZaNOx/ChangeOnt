# Experiment Doctrine Binding

This page freezes the minimum binding experiment surface required for a done-state CO investigation harness.

## Required experiment classes

The harness must support, as first-class runnable config patterns:
- element isolation
- element combinations
- semantic combinator comparisons
- header vs meta-header prior comparisons
- weight/group/final-fusion sweeps

## Minimum supported comparisons

### Element isolation
- EA-only
- EB-only
- EC-only

### Element combinations
- EA+EB
- full baseline `CO_full`

### Prior comparisons
- header-mode variation
- meta-header prior variation

### Semantic combinator comparisons
- at least one semantic override path must be runnable from config

## Binding rule

A run only counts as supporting the experiment doctrine if the config differences are real in runtime and visible in manifests/build metadata.
