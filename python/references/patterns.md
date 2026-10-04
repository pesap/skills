# Contracts and patterns

Read for a public facade, domain context, feature flag, structured return, or
cross-package error boundary. Reuse the project's canonical models before
introducing a new record. Examples require Python 3.11+ and `rust-ok`.

## A public facade and a domain context

Use a supported public function that delegates to an internal implementation.
Neither function has a leading underscore. Keep the boundary small, not a new
service class or layer hierarchy.

```python
import csv
from dataclasses import dataclass
from io import StringIO

from rust_ok import Err, Ok, Result


@dataclass(frozen=True, kw_only=True)
class CsvImportContext:
    """Control CSV import policy for one operation."""

    skip_empty_records: bool = False


def parse_csv(
    raw: str, /, *, ctx: CsvImportContext
) -> Result[list[list[str]], csv.Error]:
    """Parse CSV with an explicit import policy, retaining parser errors."""
    return parse_csv_impl(raw, ctx=ctx)


def parse_csv_impl(
    raw: str, /, *, ctx: CsvImportContext
) -> Result[list[list[str]], csv.Error]:
    """Read CSV records and apply the selected import policy."""
    try:
        with StringIO(raw, newline="") as source:
            rows = list(csv.reader(source, strict=True))
    except csv.Error as error:
        return Err(error)
    if ctx.skip_empty_records:
        rows = [row for row in rows if row]
    return Ok(rows)
```

In a package, re-export `parse_csv` and `CsvImportContext` from `__init__.py`, not
`parse_csv_impl`. Document and test the supported import path. `__all__` controls
wildcard imports, not access restrictions: implementation modules remain
importable. Do not treat this facade as a legacy compatibility shim or promise
that changed behavior cannot break callers.

The flag removes only empty records (`[]`), not quoted empty fields or
whitespace-containing fields. Both settings still use strict CSV parsing.
Column/schema validation is a separate boundary contract. This small example
materializes records; stream them when the consumer and error contract allow it.
For file-backed input, use the contract's encoding and `newline=""`.

## Context ownership and feature flags

- Name the type for its domain: `CsvImportContext`, `DispatchContext`, or another
  actual bounded operation. Do not invent a generic `Context` or global settings
  bag. Keep `ctx` as the keyword-only parameter name.
- Require the context for configured operations. No `ctx=Context()` or hidden
  environment reads inside computation. Do not add empty contexts to pure helpers.
- Resolve and validate configuration at the application boundary. Pass one
  immutable snapshot through the facade and implementation. `frozen=True` is
  shallow; nested values also need appropriate immutable ownership.
- Put independent switches in typed boolean fields. Model mutually exclusive
  behavior with an enum or union, not combinations of contradictory flags.
- Check a flag where its behavior is implemented, not throughout unrelated
  helpers. Do not put per-record data into configuration.
- Flags must not bypass required validation, conceal failures, or retain an
  obsolete implementation as a compatibility path. Add only requested flags.
- Test both settings and supported interactions. Required injection and the
  stable public behavior matter more than testing internal call order.

## Result boundaries

| Operation | Return contract |
| --- | --- |
| Ordinary computation | Its useful value `T` |
| Expected recoverable failure | `Result[T, E]` with a specific error type |
| Fallible command without a payload | `Result[None, E]`, with `Ok(None)` on success |

Preserve original exceptions in `Err` or use a domain error that retains their
cause and context. Do not turn errors into strings merely to fit a loose type.
Handle a Result with the public `is_ok`/`is_err` guards, then consume the selected
variant or propagate it. A Result must not be discarded, bare-unwrapped, or
converted into a successful default. Python does not enforce exhaustive Result
handling automatically.

Translate every documented expected failure at the chosen boundary, including
schema validation after decoding. Keep unrelated programming defects visible.
A function's annotations do not prevent underlying code from raising; inspect
the actual APIs instead of claiming Rust's static guarantees.

## Data models

Reuse a model that owns the data. For a new named record, use a stdlib dataclass;
prefer keyword-only fields. Use `TypedDict` when the contract is genuinely a
mapping. Distinguish meaningful alternatives with concrete types and a union.
Do not replace every scalar or ordinary pair with a wrapper class.

Validate untrusted values before constructing trusted domain data. Type hints
and dataclasses alone do not validate values. Do not repeat validation at every
internal call, or use casts to disguise a boundary that has not been checked.
For arrays, document dtype, domain-shaped dimensions, axis meaning, and ownership
using the [docstring guidance](docstrings.md).

## Logging and CLI boundaries

Use Loguru directly. Library initialization can disable its own namespace with
`logger.disable("package_name")`; users opt in with `logger.enable("package_name")`.
A library must not remove or reconfigure application sinks or disable other
packages' namespaces. Configure sinks at the application boundary and keep
stdout reserved for CLI data. Log an error at the layer that handles it rather
than logging and propagating it repeatedly.

Keep argument parsing, environment/configuration resolution, printing, and
process exit at the application boundary. A conventional `main()` is fine;
reusable computation should return typed values. Do not wrap Loguru in a custom
logging API or introduce classes simply to carry configuration.
