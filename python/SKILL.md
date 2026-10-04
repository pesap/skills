---
name: python
description: >
  Write and review Python using pesap's function-first, standard-library-first
  style, rust-ok errors, and loguru logging. Use for Python implementation,
  debugging, refactoring, tests, and API design, including requests identified
  by .py paths or Python repository context rather than the word Python.
  Not for non-Python tasks or purely conceptual explanations.
license: MIT
---

# Python

## First

Read local instructions, metadata, public APIs, callers, and relevant tests.
Follow explicit repository requirements, not accidental nearby style. Ask about
conflicting requirements before editing. Preserve configured tooling; use `uv`
for new or unconfigured projects. Change only what the task requires.

## Default decisions

| Decision | Use |
| --- | --- |
| Dependency | Stdlib when it meets the task's correctness and operational requirements. `rust-ok` and `loguru` are explicit exceptions. Reuse canonical public APIs, not dependency-removal rewrites. |
| Computation | Typed functions with explicit inputs and returned values. Separate I/O and logging. No stateless manager classes, one-use factories, or inheritance frameworks. |
| Data | Existing domain models first; stdlib dataclasses for new named records. Use distinct types for meaningful states, not wrappers for every scalar. Classes may own real state or resources. |
| Return | Ordinary computation: `T`. Expected recoverable failure: `Result[T, E]`. Fallible command with no payload: `Result[None, E]`. Do not invent success payloads. |
| Parameters | Primary data operands positional-only (`/`); everything else keyword-only (`*`). Configuration-only APIs need no positional operand. Respect framework-mandated signatures. |
| Public API | Export supported operations through `__init__.py`; each delegates to an underscore-free implementation. No leading-underscore function names except required protocols. Exports define support, not access control. |
| Configuration | Require a domain-named context such as `ctx: CsvImportContext` for configured operations. Inject typed immutable snapshots, not generic `Context` bags, default instances, or environment lookups. Independent flags use booleans; exclusive behaviors use modes. Flags never bypass validation. |
| Logging | Loguru, not a fallback. Configure sinks at the application boundary; library logging is opt-in and never reconfigures application sinks. Keep CLI stdout for data. |

## Working pattern

This internal helper demonstrates a Result boundary, not a package export.
Copy the contract, not its domain. Do not wrap a sufficient direct stdlib call.

```python
from rust_ok import Err, Ok, Result


def parse_integer(raw: str, /, *, base: int = 10) -> Result[int, ValueError]:
    """Parse an integer, retaining expected conversion errors as values."""
    try:
        value = int(raw, base=base)
    except ValueError as error:
        return Err(error)
    return Ok(value)
```

## Guardrails

- Handle or propagate every Result. Catch specific documented exceptions at
  the failing operation. Preserve error context; no bare unwrap, swallowed
  error, broad suppression, or success-shaped fallback. Programming defects
  remain visible, not ordinary failure values.
- Validate external input explicitly; annotations and removable assertions
  are not runtime validation. Use `zip(strict=True)` for equal lengths and
  unpacking for required cardinality. Do not revalidate trusted data everywhere.
- Keep meaningful types; do not hide uncertain contracts behind `Any` or casts.
  Use context managers for resources and readable loops over clever chains.
  Do not block an async event loop. Measure performance claims.
- Reuse public APIs and fixtures. No legacy compatibility wrappers, unrelated
  dependency churn, generated-file edits, logging wrappers, or print debugging.

## Finish

Test public success, failures, and supported flag combinations. Reproduce bugs
when practical. Run configured format, lint, type, and behavior checks, starting
narrowly. Do not silence findings with blanket ignores, casts, or disabled rules.
Pedantic sweeps are diagnostic, not automatic policy changes. Report results and gaps.

## Read only when needed

- Public facades, domain contexts, flags, structured returns, or cross-package
  error translation: [patterns](references/patterns.md).
- Public docstrings or array shape/dtype/axis contracts: [docstrings](references/docstrings.md).
- Requested strict sweep: inspect [Ruff](scripts/check_pedantic_ruff.sh) or
  [ty](scripts/check_pedantic_ty.sh); these use installed tools, not installers.

Do not preload references or evaluation files.
