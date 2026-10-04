---
name: rust
description: >
  Write and review Rust using pesap's standard-library-first, function-first
  style, typed errors, explicit ownership, and domain-specific contexts. Use
  for implementation, debugging, refactoring, tests, API design, performance,
  and safety reviews, including tasks identified by .rs paths, Cargo manifests,
  or compiler/Clippy diagnostics. Not for non-Rust tasks, Git-only operations,
  or purely conceptual explanations.
license: MIT
---

# Rust

## First

Read local instructions, Cargo manifests, toolchain/MSRV, callers, tests, and
configured checks. Follow explicit repository requirements, not accidental
nearby style. Ask about conflicting requirements before editing. Preserve the
edition, supported targets/features, dependency policy, and unrelated changes.

## Default decisions

| Decision | Use |
| --- | --- |
| Dependency | Stdlib when it meets correctness and operational requirements; `core`/`alloc` for existing `no_std` crates. Reuse canonical public APIs. Do not add a crate for a sufficient stdlib operation or rewrite existing dependencies without need. |
| Computation | Small typed functions, separate from I/O and logging. Methods belong with real state or invariants; no stateless service objects, speculative traits, or one-use factories. |
| Data | Existing domain types first. Structs for named records, enums for alternatives, newtypes for meaningful invariants. Not every scalar needs a wrapper. |
| Ownership | Borrow read-only inputs (`&str`, `&[T]`); own values when retaining or transferring them. Do not add clones, `Arc<Mutex<_>>`, or lifetime machinery merely to silence the compiler. |
| Return | Useful value `T` for ordinary work; `Option<T>` for absence; `Result<T, E>` for expected failure; `Result<(), E>` for a fallible command without a payload. Propagate with `?` and preserve causes. |
| Public API | Private implementation modules with deliberate `pub use` exports. Use the narrowest visibility and `crate::` paths. No underscore naming convention or duplicate forwarding function is needed for privacy. Respect trait signatures. |
| Configuration | Inject a domain-named borrowed snapshot such as `ctx: &CountImportContext` for configured operations. No generic context bag, empty contexts, or hidden environment reads. Independent flags use booleans; exclusive behavior uses an enum. |
| Logging | Reuse the configured logging/tracing stack. Applications own subscribers, sinks, process exit, and CLI output; libraries return errors and never install global logging configuration. |

## Working pattern

An internal batch parser can reuse the stdlib error without a new error enum.
Empty input yields an empty vector; invalid or overflowing counts return `Err`.

```rust
use std::num::ParseIntError;

/// Parse one unsigned count per line without trimming whitespace.
///
/// # Errors
/// Returns the first invalid or out-of-range count's parsing error.
pub fn parse_counts(raw: &str) -> Result<Vec<u32>, ParseIntError> {
    raw.lines().map(str::parse).collect()
}
```

## Guardrails

- Handle or propagate every Result. No production `unwrap`, `expect`, ignored
  errors, or success-shaped fallbacks. Use checked arithmetic/indexing where
  external data can overflow or exceed bounds; casts must not silently lose data.
- Validate untrusted input once at the boundary. Model invalid states out of the
  domain; flags never bypass required validation or conceal failures. Distinguish
  runtime policy from Cargo's compile-time features.
- Keep `unsafe` minimal and isolated. Explain why safe Rust is insufficient and
  document validity, aliasing, lifetime, and synchronization obligations. Tests
  can find violations; they do not prove soundness.
- Do not hold blocking locks across `.await` or block an async executor. Use the
  existing runtime and test cancellation/resource cleanup when relevant.
- No blanket lint suppression, legacy compatibility layers, speculative
  abstractions, unrelated lockfile churn, or unmeasured performance claims.

## Finish

Test public success, failure, boundaries, and supported flag combinations.
Reproduce bugs when practical. Start with focused checks, then run the project's
required suite. If no commands are defined and the lockfile is current:

```bash
cargo fmt --all -- --check
cargo test --locked
cargo clippy --locked --all-targets -- -D warnings
```

Use only supported feature/target combinations, not automatic `--all-features`.
Report exact results and gaps. Do not add end-to-end tests or release builds
unless requested or needed by the repository/task.

## Read only when needed

- Public exports, domain contexts/flags, error sources, or ownership decisions:
  [contracts](references/contracts.md).
- Workspace/MSRV/feature checks, strict Clippy, unsafe validation, or benchmarks:
  [validation](references/validation.md).

Do not preload references or evaluation files.
