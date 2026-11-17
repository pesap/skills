# Review and evaluation

Status: review candidate. No agent baseline or held-out evaluation has run.
Do not activate/release it or claim model improvement before the gate below passes.

## What changes and why

Baseline: `rust-pesap/` at repository commit
`ac5f95abcd30dffc3b37209026fab67f5249860e`.

| Previous guidance | Candidate | Reason |
| --- | --- | --- |
| Name `rust-pesap`; mostly explicit Rust triggers | Name `rust`; also .rs, Cargo, compiler, and Clippy cues | Clearer routing intent; whether the rename helps selection is unmeasured. |
| Several rule lists, no Rust example | Decision table, one common recipe, two precisely routed references | Make the common path self-contained; load specialized details only when needed. |
| Context passed explicitly, without a concrete contract | Domain-named borrowed policy snapshots; booleans versus enums; runtime flags versus Cargo features | Avoid generic settings bags and invalid flag combinations. |
| Strong types and contextual Result errors | Keep these; distinguish values, absence, failure, and no-payload commands; show source preservation | Avoid invented return values and flattened errors. |
| No dependency expansion; thiserror mentioned as an example | Explicit stdlib-first rule while preserving canonical existing APIs/error stacks | Avoid unnecessary crates without triggering dependency-removal rewrites. |
| Limited public API and ownership guidance | Private modules and pub use; borrowed views versus ownership; functions with meaningful methods | Use Rust's actual visibility and type system, not Python wrappers or keyword-only syntax. |
| `cargo fmt --all` in validation | Check-only formatting | Validation must not silently rewrite files. |
| Workspace/all-features Clippy fallback | Supported package/feature/target scope and warnings-as-errors | All features can be an unsupported combination; default-members and doctests need explicit coverage. |
| Unqualified lint expectation/let-chain preferences | Respect MSRV and actual installed tooling | New syntax and attributes cannot be assumed safe for every crate. |
| Eight recognition prompts | Expanded development prompts, behavior case designs, and deterministic example tests | Separate discoverability, executable correctness, and model outcomes. |

The candidate is not a blanket transfer of Python rules. Rust already has
`Result` and compiler-enforced privacy. Keep the repository's logging stack,
use private modules plus re-exports instead of redundant forwarding functions,
and use named context structs instead of nonexistent keyword-only parameters.
The core is reorganized, not claimed to use fewer tokens than the old skill.

## Deterministic validation

From the repository root, use an approved existing Python environment with
pytest, plus installed Rust, rustfmt, and Clippy:

```bash
python -I -B -m pytest -q -p no:cacheprovider rust/tests
rustfmt --edition 2021 --check rust/tests/contracts.rs
```

The harness compiles both Markdown examples as separate libraries and exercises
them through external public imports. It tests count boundaries, parse failures,
empty-record policy, original error locations/causes, and inaccessible private
modules. It also checks links/metadata and runs the actual fallback Cargo recipe
against a dependency-free temporary fixture. That fixture proves formatting is
check-only and unsupported combined features are not enabled automatically.
Temporary build artifacts and a fixture lockfile are expected; no repository
lockfile or source is modified. The harness does not install tools or crates.

`trigger-prompts.json` is development recognition data. `evals.json` contains
case designs, not executable agent fixtures or outcomes. Neither is held-out
release evidence. Local compiler and behavior tests cannot grade model quality.

## Model evaluation gate

1. Turn development case designs into versioned repository fixtures with
   independent outcome checks. Tune only on development data; maintain a separate
   held-out set of at least 30 cases. Smaller sets are exploratory.
2. Freeze baseline and candidate revisions. Use the same harness, tools, model,
   prompt, sampling, environment, and ambient skills. Record dataset version,
   sample size, and confidence intervals.
3. Measure explicit loading and automatic selection separately. A name-only
   comparison must hold body/description constant and inspect actual skill reads.
   Report smaller-model results individually, not hidden in pooled averages.
4. Report task success, critical errors, unsupported claims, required-schema
   failures, p50/p95 latency, cost per success, tool calls, and reference reads.
   Grade outcomes/evidence, not style, length, confidence, or model self-grading.
5. Human judging must be blinded, rubric-based, and independently double-scored.
   Keep reproducible redacted failures; validate fixes on new held-out cases.
6. Release only at >=95% held-out success, 0% critical errors, unsupported claims,
   and required-schema failures, with no quality regression greater than one
   percentage point versus baseline. Critical errors include unsafe/destructive
   actions, privacy leaks, fabricated evidence, and ignored explicit instructions.

## Design sources

- [Rust re-exports](https://doc.rust-lang.org/book/ch07-04-bringing-paths-into-scope-with-the-use-keyword.html):
  separate supported imports from the internal module layout.
- [Error sources](https://doc.rust-lang.org/std/error/trait.Error.html):
  preserve typed causes and describe the abstraction boundary.
- [Cargo features](https://doc.rust-lang.org/cargo/reference/features.html):
  prefer additive features, but respect actual supported combinations.
- [Clippy usage](https://doc.rust-lang.org/clippy/usage.html):
  distinguish configured lint policy, pedantic review, and selected restrictions.
- [gh-stack restructuring](https://github.com/github/gh-stack/commit/14fc42ed9b6c376a53b2f999f138d3bd26dac546):
  borrow self-contained common recipes and precise reference triggers, not claims
  that its reported results predict performance for this skill.
