# Spec Template Rules

## Purpose

This page defines the mandatory writing rules for all binding kernel spec files.

It exists to prevent drift, ambiguity, and accidental smuggling of assumptions into the docs.

All future primitive, element, header, translator, and related kernel spec files must follow these rules.

---

## Core Rule

A binding spec file must say **what role something has**, **what it may consume**, **what it may produce**, **what it may mutate**, and **what it must not do**.

A spec file must not merely sound plausible.  
It must constrain implementation.

---

## What a binding spec file must do

A binding spec file must:

1. define the unit's architectural role
2. distinguish the unit from neighboring layers
3. state what inputs are allowed
4. state what outputs are allowed
5. state what state mutation is allowed
6. state what is forbidden
7. state current status clearly:
   - binding now
   - partial / provisional
   - future / reserved

---

## What a binding spec file must not do

A binding spec file must not:

- mix multiple layers into one role
- silently redefine another unit’s responsibility
- use vague words like “handles”, “does stuff”, “works with” without saying how
- claim final truth where only provisional implementation exists
- smuggle task-specific behavior into ontology-level docs
- pretend missing functionality already exists

---

## Required Status Language

Every spec file must make clear which of these applies:

### Binding
The role and contract are fixed and implementation must conform.

### Provisional
The role is justified and retained, but exact formulas/algorithms are not yet fully frozen.

### Future / Reserved
The role is conceptually acknowledged, but not currently required in the canonical v1 kernel.

These labels must be used honestly.

---

## Layer Separation Rule

Every spec must clearly distinguish whether the unit is:

- primitive
- semantic combinator
- element
- bus/infrastructure
- header
- meta-header
- translator
- action surface
- runtime combinator

If the file blurs these categories, it is wrong.

---

## No Hidden Promotion Rule

A unit must not be silently promoted into a higher-level role.

Examples:
- a primitive must not quietly become an element
- a header must not quietly become ontology
- ActionHead must not quietly become a semantic mechanism
- a translator must not quietly become ontology logic

If such a change is intended, it must be explicit in docs.

---

## Allowed Uncertainty

The docs are allowed to say:
- exact law not yet frozen
- current v1 operationalization is minimal
- future richer version may exist

The docs are **not** allowed to say:
- everything is final when it isn’t
- this is just implementation detail when it carries philosophical weight
- this is philosophically grounded when it is actually just a convenience hack

---

## Preferred Writing Style

Binding docs should be:
- direct
- modular
- explicit
- non-poetic
- non-handwavy

They should sound like:
- architecture doctrine
- product/spec language
- research discipline

They should not sound like:
- loose brainstorming
- metaphysical slogans without contracts
- implementation gossip

---

## Reviewer Rule

A reviewer should be able to ask of every spec file:

- What is this unit?
- What layer is it in?
- Why does it exist?
- What can it read?
- What can it write?
- What can it change?
- What must it not do?
- Is it binding, provisional, or future?

If the file does not answer these, it is incomplete.