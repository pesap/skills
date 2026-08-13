# Delivery and validation

Read this reference for Python implementation, debugging, refactoring,
hardening, test, benchmark, or validation work. Follow local project guidance
when it conflicts with these fallback practices.

## Contents

- [Work in small vertical slices](#work-in-small-vertical-slices)
- [Use the established toolchain](#use-the-established-toolchain)
- [Test the behavior](#test-the-behavior)
- [Handle async and performance deliberately](#handle-async-and-performance-deliberately)
- [Document the public contract](#document-the-public-contract)
- [Run quality gates proportionately](#run-quality-gates-proportionately)
- [Use strict checks deliberately](#use-strict-checks-deliberately)

## Work in small vertical slices

1. Reproduce the reported behavior or establish the smallest behavior to add.
2. Identify the public seam, relevant domain terms, and error/data contract.
3. Change one observable behavior at a time. For test-first work, make the test
   fail for the intended reason, implement only enough to pass, then refactor.
4. Validate the changed behavior before expanding scope.
5. Record unverified assumptions instead of presenting them as facts.

Avoid broad cleanup while fixing a narrow defect. When a task crosses API,
schema, CLI, or integration boundaries, validate the complete affected path
rather than only a helper in isolation.

## Use the established toolchain

- Read `pyproject.toml`, inline script metadata, lockfiles, task-runner
  configuration, CI, and nearby commands before choosing an invocation.
- Preserve an existing environment manager and run its configured commands. For
  a new package, use `uv` with `pyproject.toml`; for a repeatable standalone
  script, use reproducible `uv` script metadata where suitable. Use `uv sync` for
  setup when needed and `uv run` for managed tools.
- Prefer repository-managed commands (`uv run`, `just`, scripts, or the project
  task runner) over bare `python` or `python3`.
- Put reusable build, release, probe, or workflow logic in a script rather than
  duplicating it in shell fragments or CI YAML.
- Do not edit generated files directly. Change the source configuration,
  generator, or input that owns them.
- Use the standard library first and add a dependency only when it materially
  improves the project contract. See [contracts and boundaries](contracts.md)
  before adding one.

## Test the behavior

- Use the repository's test runner and conventions. Use function-based pytest
  tests and fixtures when the project provides no stronger pattern.
- Cover each new or materially changed behavior directly or through its public
  interface. Add a regression test for a bug fix when the project supports it.
- Place reusable fixtures in `conftest.py` or project fixture plugins; do not
  copy private helpers into individual tests.
- Run the exact failing command supplied by the user, or the smallest faithful
  equivalent, before reporting success.
- Start with targeted tests for touched paths. Run broader tests only when
  required by local guidance, dependency reach, or the user's request.
- Do not add pytest tests to benchmark or experiment folders when the project
  or user does not expect them. Use an artifact-appropriate check instead.

When fixture architecture, plugins, property tests, snapshots, or test strategy
become the main problem, apply the repository's test guidance and `tdd-pesap`.

## Handle async and performance deliberately

- Use async only for I/O-bound paths that are already async-aware. Do not block
  the event loop.
- Keep hot paths simple before optimizing. Inspect materialization, copies,
  sorting, repeated conversions, and model-building loops before proposing a
  performance change.
- Prefer project iterators and generators when building constraints, mappings,
  or model inputs.
- Use the project's benchmark or profiling harness for performance and memory
  claims. In pesap benchmark workflows, use Torc rather than in-process memory
  probes such as `tracemalloc` or `memory_profiler`.
- Avoid clever NumPy constructs such as `np.einsum` unless they are clearly the
  simplest option and their shape and axis semantics are documented.

## Document the public contract

- Follow local documentation and docstring conventions first.
- Add runnable examples for contracts that are public, non-obvious,
  user-facing, or easy to misuse.
- Explain non-obvious rationale, invariants, units, generated boundaries,
  compatibility constraints, operational gotchas, and algorithm choices.
- Use [docstrings](docstrings.md) when applying the NumPy-style fallback or
  documenting NumPy arrays.

## Run quality gates proportionately

- Use the repository's formatter, linter, type checker, and test commands as
  the normal gate.
- For scripts and benchmarks, choose explicit non-pytest validation such as
  `ruff`, `py_compile`, doctest, a bounded smoke run, a workflow dry-run, or a
  full benchmark run when warranted.
- Validate a changed public interface, error path, and CLI boundary when one is
  in scope. Do not infer correctness solely from formatting or type checking.

## Use strict checks deliberately

Write new code to survive strict review even when a local configuration is
looser. Use the pedantic scripts for strict sweeps, recent hardening work, or
investigating permissive local settings. Treat their results as evidence to
triage, not a reason to override deliberate project policy.

| Script | Purpose |
| --- | --- |
| [`../scripts/check_pedantic_ruff.sh`](../scripts/check_pedantic_ruff.sh) | Run Ruff with preview rules and `ALL` enabled. |
| [`../scripts/check_pedantic_ty.sh`](../scripts/check_pedantic_ty.sh) | Run ty with all rules elevated to errors. |
