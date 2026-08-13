---
name: python-pesap
description: >
  Apply pesap's Python engineering standard to repository-integrated feature
  work, bug fixes, refactors, code review, tests, type/data-contract changes,
  CLI scripts, benchmarks, and production hardening. Use when implementing,
  debugging, reviewing, testing, or maintaining Python code with uv, pytest,
  Ruff, ty, Pydantic, dataclasses, async code, logging, or NumPy. Prefer
  repository conventions and configured tooling; use uv for new or unconfigured
  projects.
license: MIT
---

# Python pesap

Apply repository instructions, package conventions, and configured commands
first. Use this skill's defaults only when the repository does not decide.

## Workflow

1. Read local instructions, package or script metadata, tool configuration,
   package layout, nearby code, and existing tests before editing.
2. Define the observable behavior, data/error contract, acceptance criteria, and
   smallest meaningful validation target. Reproduce a reported failure first
   when practical.
3. Reuse the package's public APIs, domain models, fixtures, commands, and
   logging conventions. Do not create parallel local abstractions.
4. Implement the smallest root-cause change. Keep generated files, dependency
   changes, lockfile changes, and unrelated cleanup out of scope.
5. Add or update focused public-behavior validation. For a bug fix, add a
   regression test when the repository supports one.
6. Run the narrowest relevant checks first, then required broader checks. Report
   exact commands, results, assumptions, and remaining gaps.

For test-first work, apply one red-green-refactor cycle per observable behavior;
also use `tdd-pesap` when test design is the task's center of gravity.

## Core defaults

- Preserve the project's configured package manager, lockfile, and task runner.
  For a new package, use `uv` with `pyproject.toml`; for a repeatable standalone
  script, use reproducible `uv` script metadata where suitable. Run managed tools
  through `uv run`.
- Add explicit type hints to new or materially changed code. Prefer the
  strongest available domain type, named structured return, `Protocol`, union,
  or generic over loose tuples, `object`, `dict[str, Any]`, or casual casts.
- Make success and failure contracts explicit. At recoverable boundaries, use
  the project's established error model; never bare-unwrap `rust_ok` results.
  Keep `try` blocks small and catch documented, specific exceptions.
- Test public behavior rather than private helpers. Reuse fixture plugins or
  `conftest.py` instead of copying test helpers.
- Keep CLI parsing and process exit at the `__main__` boundary. Put reusable
  business logic in typed helpers that return useful values.
- Follow existing logging first. If no convention exists, use the pesap
  `loguru` fallback and keep library logging opt-in. Reserve `print(...)` for a
  CLI or script's stdout contract.
- Comment non-obvious rationale, invariants, units, compatibility constraints,
  generated boundaries, and operational gotchas; do not narrate obvious code or
  leave breadcrumbs after moves.

## Reference router

Load only the reference that matches the work; do not preload all references.

| Work center | Read |
| --- | --- |
| Implementation, debugging, refactoring, tests, async work, performance, or validation | [delivery and validation](references/delivery.md) |
| Public APIs, return/error contracts, types, dependencies, logging, CLI, or data-model boundaries | [contracts and boundaries](references/contracts.md) |
| A concrete Python pattern would prevent ambiguity | [patterns](references/patterns.md) |
| Public docstrings, doctest-comment examples, or NumPy array contracts | [docstrings](references/docstrings.md) |
| A strict lint or type-hardening sweep | [pedantic Ruff](scripts/check_pedantic_ruff.sh) or [pedantic ty](scripts/check_pedantic_ty.sh) |

## Quality gates

- Prefer repository-configured formatter, linter, type-checker, and test
  commands. Use targeted checks for touched paths unless broader validation is
  requested or required.
- For benchmark or experiment folders, use the validation that matches the
  artifact: lint, `py_compile`, doctest, bounded smoke run, workflow dry-run,
  or the project's benchmark harness. Do not add pytest by default.
- Treat pedantic Ruff and ty scripts as signal generators, not universal
  blockers. Investigate findings and distinguish new defects from deliberate
  project policy.

## Output

- Assumptions and approach.
- Files and public behaviors changed.
- Validation commands and exact results.
- Residual risks, follow-ups, or delegation notes.

## Evals

- Trigger evals: `evals/trigger-prompts.json`.
- Output-quality evals: `evals/evals.json`.
