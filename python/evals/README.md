# Validation and evaluation

Status: candidate for review. Agent baseline/held-out evaluation has not run.
Do not treat the examples or case designs as proof of model improvement, or
activate/release the candidate before the evaluation gate passes.

## Deterministic checks

Use an approved existing environment with Python 3.11+, pytest, and rust-ok.
The test runner does not install dependencies. From the repository root:

```bash
python -B -m pytest -q -p no:cacheprovider python/tests
bash -n python/scripts/check_pedantic_ruff.sh python/scripts/check_pedantic_ty.sh
```

The tests execute the complete Python examples and their doctests, check the
CSV facade's context and flag behavior, validate reference links and metadata,
and exercise audit-wrapper invocation through fake external tools. They do not
measure an agent's ability to produce the desired code.

Run configured formatting, lint, and type checks separately. For a project using
Ruff and ty, the command shapes are `ruff format --check <paths>`,
`ruff check --no-fix --no-fix-only --no-unsafe-fixes <paths>`, and
`ty check --error-on-warning <paths>` through that project's environment runner.
Do not silently replace its toolchain.

The optional shell wrappers execute installed tools from PATH, preserve the
working directory, treat every argument as a path, and default to `.`. They
never install tools or synchronize environments. Run them from the target
project through its configured runner. Ruff's `ALL --preview` is diagnostic;
triage it rather than rewriting project policy. Ty enforces configured rules
and fails on warnings; there is no assumed `all` rule. Rule/version changes
require checking the actual CLI and rerunning the relevant tests.

## Agent evaluation

`trigger-prompts.json` is a development set for recognition.
`evals.json` contains development case designs, not executable task fixtures or
run results. Neither is held-out release evidence.

Before deployment:

1. Turn the case designs into versioned repository fixtures with independent
   behavior checks. Maintain separate development and held-out sets with at
   least 30 held-out cases; smaller sets are exploratory.
2. Compare a frozen baseline against the candidate using the same harness,
   models, tools, sampling, environment, and ambient skills. Record skill and
   prompt revisions, dataset version, sample size, and confidence intervals.
3. Separate body quality under explicit loading from automatic selection.
   To investigate naming, hold the body and description fixed for a name-only
   comparison. Grade actual reads and outcomes, not claims of using a skill.
4. Report task success, critical errors, unsupported claims, required-schema
   failures, p50/p95 latency, cost per success, tool calls, and reference reads.
   Report the intended smaller models separately instead of pooling failures.
5. Use executable outcome/evidence checks. Human judgment must be blinded,
   rubric-based, and independently double-scored. No model self-grading or
   style/length preference scores as release evidence.
6. Release only at >=95% held-out task success, 0% critical errors, unsupported
   claims, and required-schema failures, with no quality regression greater
   than one percentage point versus baseline. Critical errors include unsafe
   actions, privacy leaks, fabricated results, and ignored explicit instructions.
   Preserve redacted failures; validate fixes on new held-out cases.

## Design references

Borrow principles, not every implementation choice:

- [Sorted Containers](https://grantjenks.com/docs/sortedcontainers/implementation.html):
  familiar data structures, explicit invariants, measured performance.
- [Defensive Python](https://www.justinxu.me/blog/post/defensive-python-1):
  strict zip and cardinality checks; required validation must not rely on assert.
- [The csv module](https://www.kdnuggets.com/surprising-things-you-can-do-with-pythons-csv-module):
  standard-library composition; heuristics are not schema guarantees.
- [Python like Rust](https://kobzol.github.io/rust/python/2023/05/20/writing-python-like-its-rust.html):
  meaningful types and invalid-state prevention, not Rust emulation everywhere.
- [Errors as values](https://www.inngest.com/blog/python-errors-as-values):
  explicit failures; this skill chooses rust-ok rather than the article's union.
- [gh-stack restructuring](https://github.com/github/gh-stack/commit/14fc42ed9b6c376a53b2f999f138d3bd26dac546):
  core decisions and recipes with specific reference triggers. Its reported
  results are not evaluation evidence for this skill.
