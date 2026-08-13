# Contracts and boundaries

Read this reference when adding or reviewing public helpers, types, return or
error behavior, dependencies, logging, CLI scripts, Pydantic models, dataclasses,
or schema boundaries. Follow a stronger repository contract when one exists.

## Contents

- [Add dependencies deliberately](#add-dependencies-deliberately)
- [Make type and return contracts explicit](#make-type-and-return-contracts-explicit)
- [Handle failures at narrow boundaries](#handle-failures-at-narrow-boundaries)
- [Preserve public pathways](#preserve-public-pathways)
- [Keep logging and output intentional](#keep-logging-and-output-intentional)
- [Keep CLI boundaries thin](#keep-cli-boundaries-thin)
- [Review data-model handoffs](#review-data-model-handoffs)

## Add dependencies deliberately

- Try the standard library before adding a dependency.
- Add a dependency only when the standard-library option is impossible, unsafe,
  or materially worse for the project contract. State why it is needed.
- Preserve the project's environment manager, dependency declarations, and
  lockfile. Do not introduce a second package-management flow.

## Make type and return contracts explicit

- Add explicit type hints to new or materially changed code.
- Prefer a domain model, semantic alias, `Protocol`, generic, concrete union,
  `TypedDict`, or named dataclass over `object`, loose `dict[str, Any]`, a long
  positional tuple, or `typing.cast`.
- Use the strongest local type for semantic fields such as units, IDs, component
  references, solver names, datasets, and model entities.
- Identify the data owner before adding a dataclass or Pydantic model. Reuse
  canonical package models or infrasys `System` components when they own the
  contract.
- Return a useful value: a validated input, mutated object, summary, result,
  written path, count, predicate, or domain model. Do not obscure a meaningful
  result behind success-by-`None`.
- When no payload is the only sensible success value, use the project's result
  contract, such as `rust_ok.Result[None, E]` where `rust_ok` is established.
- Keep signatures compact. Use keyword-only arguments once a function has more
  than one or two non-obvious positional parameters.
- Name boolean predicates `is_*` or `has_*`. Reserve `validate_*` for functions
  that raise detailed validation errors; return the validated value when useful.
- See [patterns](patterns.md) for concrete type, return, and NumPy examples.

## Handle failures at narrow boundaries

- Use the project's established error contract at recoverable boundaries. In
  repositories using `rust_ok`, return `Result[T, E]` when callers branch on
  success or failure.
- Never bare-unwrap `rust_ok` results in live code. Branch explicitly,
  propagate the result, or add useful context.
- Keep `try` blocks to one or two statements where practical. Catch specific,
  documented exceptions or library status codes.
- Do not turn unknown failures into generic errors, broad suppression, or a
  fallback that hides the cause. Preserve context in raised errors or `Err(...)`
  payloads.
- Fail fast at input, I/O, and integration boundaries with actionable errors.

## Preserve public pathways

- Use public APIs from dependencies and sibling packages. Do not call private
  APIs or build alternate paths around an existing clean public interface.
- Keep visibility intentional. Use a leading underscore only for implementation
  details with no expected reuse, or when a framework protocol requires it.
- Prefer explicit, action-first names such as `list_*`, `get_*`, `build_*`, and
  `run_*` so behavior is clear at the call site.

## Keep logging and output intentional

- Follow the project's existing logging convention first.
- If no coherent convention exists, use the pesap `loguru` fallback and disable
  package logging by default so library users opt in.
- Use structured or consistent operational messages instead of ad-hoc debugging
  output. Reserve `print(...)` for CLI stdout contracts, examples, tests, and
  concise script output.
- Give probes, benchmarks, and smoke scripts concise operational output. Emit
  full JSON only for `--json`, `--verbose`, or diagnostics.

## Keep CLI boundaries thin

- Keep `argparse` or `sys.argv` parsing and process exit behavior directly in
  `if __name__ == "__main__":` unless the repository's CLI framework defines a
  different boundary.
- Put reusable business logic in typed functions that return summaries or domain
  values. Do not make `run_*` functions print as their primary behavior.
- Separate input parsing, domain input construction, core computation, result
  validation, and boundary serialization or printing in benchmark and
  experiment scripts.

## Review data-model handoffs

Treat model shape, Pydantic fields, optional fields, units, component references,
and schema evolution as design-review triggers.

- `Field(description=...)` does not strengthen a weak type.
- Review every new `bool` or optional field for its semantics, defaults, and
  compatibility impact.
- Reuse canonical package or domain models before creating a local copy.
- Document dtype, shape, axis meaning, and ownership for public NumPy arrays.
  Do not expose a long positional tuple of arrays; return a named object instead.
