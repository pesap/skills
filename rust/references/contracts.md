# Public contracts, ownership, and policy

Read for a public API, context/flag change, error source, or ownership decision.
Prefer the project's canonical domain models and error types over new ones.

## A private module and a supported export

This complete library example uses only stdlib and Rust 2021. Put it in
`src/lib.rs`. Consumers import `parse_counts` and `CountImportContext` from the
crate root; the implementation module is private. Rust privacy removes the need
for Python-style underscore names or a second forwarding function.

```rust
mod count_import {
    use std::error::Error;
    use std::fmt;
    use std::num::ParseIntError;

    /// Policy resolved once at the application boundary.
    #[derive(Debug)]
    pub struct CountImportContext {
        pub skip_empty_records: bool,
    }

    /// An invalid count and its original one-based input line.
    #[derive(Debug)]
    pub struct CountImportError {
        pub line: usize,
        pub source: ParseIntError,
    }

    impl fmt::Display for CountImportError {
        fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
            write!(f, "invalid count at line {}", self.line)
        }
    }

    impl Error for CountImportError {
        fn source(&self) -> Option<&(dyn Error + 'static)> {
            Some(&self.source)
        }
    }

    /// Parse one unsigned count per line without trimming whitespace.
    ///
    /// Empty input yields an empty vector. The policy may skip empty lines,
    /// but never whitespace-only lines or malformed/out-of-range counts.
    ///
    /// # Errors
    /// Returns the first invalid count, retaining its line and parsing cause.
    pub fn parse_counts(raw: &str, ctx: &CountImportContext) -> Result<Vec<u32>, CountImportError> {
        let mut counts = Vec::new();
        for (index, line) in raw.lines().enumerate() {
            if ctx.skip_empty_records && line.is_empty() {
                continue;
            }
            let count = line.parse().map_err(|source| CountImportError {
                line: index + 1,
                source,
            })?;
            counts.push(count);
        }
        Ok(counts)
    }
}

pub use crate::count_import::{parse_counts, CountImportContext, CountImportError};
```

The input is borrowed and the vector is owned because the caller retains the
result. The example materializes counts; use streaming only when the consumer
and partial-failure contract need it. A short loop is preferable to a dense chain
when attaching line numbers and applying policy.

## Domain contexts and feature flags

- Require a context only for configured operations, not every pure helper.
  Name the type for the operation, such as `CountImportContext` or
  `DispatchContext`. Rust has no Python-style keyword-only arguments; a named
  context struct makes policy explicit without positional boolean lists.
- Resolve configuration, environment, and flag-provider reads at the application
  boundary. Borrow one immutable snapshot through the operation. `&T` alone does
  not prohibit interior mutation: keep `Cell`, locks, and mutable shared settings
  out of policy snapshots.
- Independent runtime switches use booleans; mutually exclusive behavior uses
  an enum. Add only requested flags, test both settings and supported interactions,
  and never use flags to bypass required validation or retain obsolete behavior.
- Cargo features select compiled capabilities and dependencies. Runtime contexts
  select behavior among available capabilities. Do not use them interchangeably;
  validate unsupported configuration at the boundary. Prefer additive Cargo
  features rather than introducing mutually exclusive dependency combinations.

## Error contracts

Reuse a specific stdlib error when it communicates enough. Use a domain error
when callers need distinctions or boundary context, retaining original errors
through `Error::source()`. Do not flatten causes into strings or log and propagate
at every layer. Return `Ok(())` when successful completion has no useful payload.

Use the existing error stack when it is part of the repository contract;
`thiserror` or `anyhow` is not a mandatory new dependency. Application-level
reports may erase error types, but reusable APIs should preserve distinctions
callers need. `Option` means absence, not a discarded error.

Document escaping failures in rustdoc's `# Errors`, required caller obligations
in `# Safety` for unsafe APIs, and genuine panic preconditions in `# Panics`.
Prefer removing data-driven panics over documenting avoidable crashes. Assertions
in tests diagnose broken expectations; they are not production validation.

## Ownership and abstraction

Use `&str`/slices for read-only views and owned values for storage or transfer.
Introduce generic bounds or trait objects only for required composition, not
hypothetical future implementations. Keep useful methods and trait impls on
stateful types; function-first does not mean avoiding Rust's type system.

A clone can be the correct ownership choice; explain meaningful allocation or
sharing costs instead of banning every clone. Do not replace ownership reasoning
with global state, gratuitous `Arc`, unsafe references, or broad lifetime bounds.
Prefer `crate::` imports and narrow visibility; exposing a module just to let a
test reach its internals weakens the contract. Test the supported crate-root API.
