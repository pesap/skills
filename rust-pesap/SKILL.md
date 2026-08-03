---
name: rust-pesap
description:
  pesap's opinionated Rust engineering standard for feature work, bug fixes,
  refactors, performance changes, and hardening. Use when implementing or
  reviewing Rust code, reducing panic or unsafe risk, strengthening types and
  error contracts, or validating Cargo projects. Project conventions take
  precedence over this fallback standard.
license: MIT
---

# Rust pesap

Apply the repository's established conventions first. When the repository does
not define a convention, use the standards below.

## Non-negotiable defaults

- Prefer `crate::` paths over `super::` for clarity.
- Do not use `unwrap`, `expect`, or panic-prone paths in production code.
- Use strong domain types, enums, and newtypes instead of stringly-typed state.
- Avoid global mutable state; pass context explicitly.
- Treat warnings as errors and fix them rather than hiding them.
- Keep `unsafe` isolated, minimal, and documented with the invariants that make
  it sound. Explain why safe Rust is insufficient and how tests cover the risk.
- Do not add end-to-end tests unless the user or repository explicitly requires
  them.
- Do not broaden dependency or lockfile changes unnecessarily.
- Do not use release-profile builds unless requested or needed to investigate a
  performance issue.

## Workflow

1. Inspect the crate, workspace, nearby tests, Cargo configuration, and local
   instructions before editing.
2. Clarify the behavior and contract. Model domain types before implementing
   logic.
3. Implement the smallest change that preserves the contract.
4. Add focused tests for observable behavior and error paths. Prefer integration
   tests when behavior crosses module or CLI boundaries.
5. Validate with the narrowest relevant commands, then run the repository's
   broader required checks.
6. For performance-sensitive changes, benchmark or profile the hot path and
   report the comparison and trade-offs.

## Error and failure handling

- Use `Result` with typed, contextual errors such as `thiserror` where suitable.
- Prefer `?`, `if let`, and let-chains for explicit fallibility.
- Do not hide failures behind fallbacks, ignored results, broad suppression, or
  panic-prone shortcuts.
- Preserve useful context when mapping errors.

## Testing and validation defaults

Use repository-defined commands first. If none exist, the fallback commands are:

```bash
cargo fmt --all
cargo test
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
```

Additional defaults:

- Use `cargo nextest run` for focused execution when the repository supports it.
- Use snapshots such as `insta` only when nearby tests already use them.
- For Unix-hosted Windows-target changes, run the appropriate `cargo xwin
  clippy ...` validation when available.
- Never assume warnings or Clippy findings are pre-existing; verify them.

## Style and maintenance

- Read nearby code and match its established test and module patterns.
- Prefer top-level imports and descriptive names.
- Keep `mod tests {}` at the bottom of a module when tests are colocated and the
  repository follows that convention.
- Prefer `#[expect(...)]` over `#[allow(...)]` when a lint suppression is truly
  necessary, and document why.
- Use linked Rust doc references such as [`TypeName`] where appropriate.
- Question assumptions at boundaries and make ownership, lifetime, and safety
  reasoning visible.

## Output

- Summary of code and test changes.
- Validation commands and exact results.
- Performance notes for hot paths.
- Risks, assumptions, and unresolved gaps.
