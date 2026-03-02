# Developer Guide

This file explains how development should proceed under the docs → code pipeline.

## 1. Development rule

Development should proceed against the documented target state.

Do not use the current code alone as the source of truth when it conflicts with the docs.

## 2. Docs-first or docs-in-lockstep rule

When adding or changing major functionality, do one of the following:
- update docs first
- or update docs in lockstep with code

Do not let code drift into undocumented behavior.

## 3. Adding a new environment

To add a new environment family or environment variant, the following must be updated:

1. environment code
2. family runner support
3. translator boundary support
4. config surfaces
5. docs:
   - environment docs
   - runner docs if needed
   - translator docs if needed
   - coverage checklist if new folder/subsystem is introduced

The final result should be a plug-in style extension, not an ad hoc special-case branch.

## 4. Adding a new primitive

To add a new primitive:
1. define its conceptual role
2. define its runtime interface
3. define which elements may consume it
4. classify it:
   - core
   - optional
   - experimental
5. document it in kernel docs and code-reference docs
6. ensure config exposure is honest

## 5. Adding a new element

To add a new element:
1. define its conceptual role
2. define its primitive dependencies
3. define its contribution packet behavior
4. define whether it is:
   - core
   - optional
   - experimental
5. document its expected role in fusion/grouping
6. add honest runtime/test coverage

## 6. Config truthfulness rule

Do not expose parameters that runtime ignores.

Decorative config is a real misalignment.

## 7. Folder and naming rule

Folders and file names should reflect:
- actual responsibility
- actual runtime role
- and actual status

Meaningless names, stale locations, or misleading placement should be cleaned up.

## 8. Legacy rule

Do not keep legacy code as a hidden active alternative.

Legacy code should be:
- archived
- isolated
- or clearly marked inactive

## 9. Extension success criterion

An extension is only successful if:
- it plugs into the existing architecture cleanly
- it preserves the docs → code alignment
- and it does not create a second hidden truth about runtime behavior