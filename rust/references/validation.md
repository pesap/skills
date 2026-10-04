# Validation without policy churn

Read for workspaces, feature/target matrices, MSRV, stricter Clippy, unsafe code,
or performance work. Repository commands and supported configurations come first.
Use installed tools; do not bootstrap a toolchain, add components, or rewrite
lockfiles merely to make a check run.

## Choose the relevant scope

1. Read workspace members/default-members, `rust-version`, edition,
   `rust-toolchain.toml`, Cargo configuration, CI, and supported targets/features.
2. Run the focused regression test first, selecting the affected package/test.
   Use public integration tests for cross-module behavior and local tests for
   local logic. Do not expose private modules just for a test.
3. Run the core format/test/Clippy recipe, then the repository's required broader
   checks. Formatting validation uses `--check`, not an in-place format or fix.
4. Report commands, selected packages/features/targets, versions, exit statuses,
   and skipped checks. Verify the baseline before calling findings pre-existing.

## Cargo decisions

| Situation | Action |
| --- | --- |
| Workspace | Cargo defaults may select only default-members. Select affected packages with `-p`; use `--workspace` when the repository requires all members. |
| Lockfile | Use `--locked` for an existing current lockfile. A missing/stale lockfile is a real prerequisite failure; do not silently drop the flag. Generate/update only when needed for the authorized task. |
| Offline checks | Add `--offline` only when dependencies are already cached or there are none. It is not a substitute for a current lockfile. |
| Cargo features | Test default and documented supported combinations. `--all-features` is appropriate only when that combination is supported. Do not introduce exclusive features just to match a test fixture. |
| No-default mode | Use `--no-default-features` only when that mode is supported, with any required explicit features. |
| Doctests | Ordinary `cargo test` includes applicable doctests. `--all-targets` does not; run `cargo test --doc` separately when target selectors or nextest omit them. Preserve package/feature/lock selections. |
| MSRV | Validate with an already installed supported toolchain when available. Do not adopt newer syntax, APIs, lint attributes, or edition changes without checking the crate's MSRV. |
| Cross-target | Use configured targets/runners, including `cargo xwin` only where supported. Compilation or Clippy for a target is not proof that target tests ran. |

`cargo nextest` and snapshot tools are options only when already part of the
project. Do not install them as routine validation prerequisites. Cargo checks
can create build artifacts; non-mutating here means no source or lockfile edits,
not a read-only filesystem sandbox.

## Strict Clippy

The default gate is the configured lint policy plus `-D warnings`, not every
possible lint. Keep existing coherent lint settings and fix relevant findings.
Clippy is not a proof of panic freedom, memory safety, or functional correctness.

For a requested pedantic review, inspect the pinned toolchain's lint documentation
and run a scoped diagnostic sweep. Triage deliberate trade-offs separately from
required failures. Do not blanket-enable `clippy::restriction`: its lints can
conflict. Do not adopt pedantic/nursery findings wholesale or use `cargo clippy
--fix` in a read-only review.

A suppression needs a specific lint, narrow scope, and a sound reason. Prefer
`#[expect(...)]` when the MSRV supports it, so a stale expectation is visible.
Do not upgrade the toolchain merely to use it, add blanket allows, or silently
relax the project's lint policy. Check actual installed help before using flags.

## Safety, async, and performance

- For unsafe changes, state and inspect the safety obligations first. Add tests
  for affected boundaries; use Miri or sanitizers only with supported installed
  tooling and report limitations. Passing them is evidence, not a soundness proof.
- For async changes, test cancellation, cleanup, and contention when relevant.
  Do not hide blocking work behind `async fn` or introduce a new runtime casually.
- For hot paths, compare the same workload, build profile, inputs, and environment.
  Release/benchmark profiles are justified for performance measurement, not every
  normal validation run. Preserve results and correctness checks; do not call
  fewer clones, allocations, or a shorter iterator chain faster without evidence.
