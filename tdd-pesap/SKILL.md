---
name: tdd-pesap
description:
  Pesap's opinionated test-first development discipline for behavior-focused,
  public-interface tests and small vertical slices. Use when implementing a
  feature or bugfix with tests, designing testable interfaces, reviewing test
  quality, or applying red-green-refactor in Python, TypeScript, Rust, C, or
  another language. Read the matching language reference for tool-specific
  guidance.
license: MIT
---

# TDD Pesap

Use tests to discover and protect observable behavior, not to freeze internal
implementation. Work in small vertical slices and keep the feedback loop tight.

## Core doctrine

- Test behavior through the narrowest useful public interface.
- Name tests after capabilities or outcomes, not helpers or implementation
  details.
- Derive expected values independently from the implementation: literals,
  worked examples, specifications, or trusted fixtures.
- Prefer real domain components. Mock only boundaries such as network services,
  processes, clocks, randomness, or other expensive/unsafe external effects.
- Design small, explicit interfaces that make the behavior easy to exercise.
- Prefer deep modules: keep the public surface small and put complexity behind
  it.
- Add regression tests for bugs before fixing them.

## The vertical-slice loop

For each behavior, complete one cycle before starting the next:

1. **RED** — write one test for one observable behavior and confirm it fails for
   the intended reason.
2. **GREEN** — implement only enough production code to pass that test.
3. **REFACTOR** — improve the design while all relevant tests remain green.

Do not write the entire test suite before implementation, anticipate behavior
that has not been requested, or refactor while the test is red.

## Test quality bar

Reject tests that:

- assert private methods, internal call order, or implementation-shaped data;
- mock collaborators owned by the system under test without a boundary reason;
- compute the expected result using the same algorithm as production;
- pass without proving a meaningful behavior;
- break when internals are renamed or reorganized without a behavior change.

When a test is hard to write, first question the interface and seam rather than
adding more mocking or test-only hooks.

## Planning and completion

Before the first test, identify the smallest public behavior and the relevant
project vocabulary. Ask at most one blocking clarification when the next test
would encode a risky assumption.

After each cycle, run the narrowest relevant validation. Before reporting done,
run the broader checks required by the project and report commands, results, and
remaining gaps.

## Language guidance

Read the matching reference before applying tool- or language-specific rules:

- [Python](references/python.md)
- [TypeScript](references/typescript.md)
- [Rust](references/rust.md)
- [C](references/c.md)

For another language, preserve this core doctrine and follow the repository's
native test runner, type checker, formatter, and lint rules.

## Output

- Behavior covered in each cycle.
- Tests and production files changed.
- Validation commands and results.
- Remaining gaps, assumptions, and the next behavior if work continues.
