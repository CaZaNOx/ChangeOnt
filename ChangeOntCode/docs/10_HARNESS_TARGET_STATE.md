# Harness Target State

This file states the desired final state of the harness.

## 1. Purpose

The final harness should be:

- clean
- canonical
- faithful
- honest
- investigatory
- extensible

It should not merely “launch things.”  
It should make the project’s claims testable in an honest way.

## 2. Clean

A clean harness means:
- no confusing duplicate runtime truths
- no misleading config behavior
- no unclear file roles
- no silent artifact failures
- no mislabeled outputs

## 3. Canonical

A canonical harness means:
- one documented target execution model
- one documented artifact contract
- one documented config interpretation
- no hidden legacy behavior acting as coequal truth

## 4. Faithful

A faithful harness means:
- it does not distort the intended kernel architecture
- it supports the correct boundary roles for environment/runner/translator/kernel
- it respects the documented CO contracts

## 5. Honest

An honest harness means:
- it compares CO and STOA truthfully
- it does not silently drop intended CO runs
- it does not mislabel outputs
- it does not present semantically broken summaries as valid
- it only earns the phrase “CO-honest implementation” once code aligns with docs

## 6. Investigatory

An investigatory harness means:
- it supports `CO_full`
- it supports reduced and variant CO configurations
- it supports honest sweeps of:
  - primitive roles
  - element variants
  - combinators
  - weights
  - thresholds
  - interactions
- it supports analysis of how CO commitments behave across families

## 7. Extensible

An extensible harness means:
- new environments can be added by adding:
  - environment
  - runner support
  - translator support
  - config
  - docs
- new primitives and elements can be added without architectural drift
- the same suite structure can absorb those additions coherently

## 8. Docs-to-code requirement

The harness target state is only useful if it is captured clearly enough in docs that:
- code misalignment is visible
- implementation can proceed against the docs
- and future changes can be judged against a stable documented should-state

That is the standard this project should enforce.