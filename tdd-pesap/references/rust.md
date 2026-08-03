# Rust testing

Apply the core behavior-first doctrine through public crate, module, or CLI
interfaces.

- Prefer integration tests when behavior crosses module boundaries; use unit
  tests for genuinely local logic.
- Model expected outcomes with explicit values and typed `Result`/error cases.
- Test invariants and properties for tricky transformations where examples are
  not enough.
- Avoid mocking internal Rust code. Use explicit seams for external services,
  processes, clocks, and randomness.
- Do not add end-to-end tests unless the user or project requires them.
- Run focused `cargo test` cycles, then the repository's required formatting,
  Clippy, and broader test checks before completion.

Typical validation:

```bash
cargo fmt --all
cargo test
cargo clippy --workspace --all-targets --all-features --locked -- -D warnings
```
