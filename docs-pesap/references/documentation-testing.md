# Documentation testing

Documentation is a tested product surface, not a prose-only artifact. Use the
repository's own commands first. The practices below are the generalized
pattern from [NatLabRockies/arco](https://github.com/NatLabRockies/arco/tree/main).

## Test executable examples

Keep examples copy-pasteable as well as testable. For command examples, show a
single expected result as a `#`-prefixed comment value inside the command block
(for example, `# created`). Do not place uncommented command output in a block
that users are expected to copy and paste.

- Put runnable examples in explicitly marked doctest fences, such as
  ````markdown
  ```python doctest
  >>> value = 2 + 2
  >>> value
  # 4
  ```
  ````
- Discover those fences across the documentation tree and execute them in a
  controlled test runner.
- Fail when no doctest blocks are found if the documentation contract requires
  executable examples.
- Support comment-prefixed doctest lines only when the project deliberately
  uses that format.
- Keep examples on the normal user path. Put raw, expert, or unstable APIs in a
  clearly marked expert document and allowlist that path explicitly.

## Scripts

Use pytest's doctest plugin for a small, portable baseline. To collect Python
examples from Markdown files:

```bash
python -m pytest --doctest-glob='*.md' docs/
# all documentation doctests passed
```

Run one document while editing:

```bash
python -m pytest --doctest-glob='*.md' docs/tutorials/quickstart.md
# quickstart doctests passed
```

For Python modules, use the module collector instead:

```bash
python -m pytest --doctest-modules src/
# all module doctests passed
```

Keep these commands in a repository script when the project has setup or
fixtures that pytest needs. The accompanying
[`scripts/test_docs_doctest.py`](../scripts/test_docs_doctest.py) is a minimal
copyable example:

```bash
cp docs-pesap/scripts/test_docs_doctest.py scripts/test_docs_doctest.py
python scripts/test_docs_doctest.py docs/
# all documentation doctests passed
```

Adapt the script when the repository needs fixtures, plugins, or a project
environment runner such as `uv run` or `poetry run`. Do not add
`--doctest-modules` to a Markdown docs command, and do not assume pytest will
execute arbitrary fenced code that has no doctest prompts.

## Test documentation policy, not just syntax

Add focused tests for rules that matter to the project:

- canonical API vocabulary and preferred calling conventions;
- forbidden legacy shortcuts or deprecated examples;
- beginner/tutorial pages not using expert-only APIs;
- required links from README and section indexes;
- migration examples matching the supported old-to-new mapping;
- examples that must remain file-backed fixtures rather than large inline
  literals.

Test the guard itself with small fixtures so the guard can prove that it detects
both a forbidden example and an allowed expert example. Keep allowlists narrow
and explain why each exception exists.

## Wire checks into the delivery path

Provide a fast local command such as `just docs-test` or an equivalent script,
then invoke it from the broader repository check and CI aggregate. Use path
filters to run the docs job when documentation, the docs test runner, its
runtime setup, or its command definitions change. This prevents a docs test
from silently going stale when its harness changes.

Run documentation checks at the appropriate levels:

1. focused doctest and policy tests during editing;
2. Markdown formatting, whitespace, spelling, and link checks in hooks;
3. the repository's full docs/CI gate before merge or release.

In Arco, the concrete pattern is:

- runner: `scripts/test_docs_doctest.py`;
- focused command: `just docs-test`;
- aggregate commands: `just check` and `just ci`;
- CI entry point: `just ci-docs-test`;
- supporting hooks include Markdown formatting, trailing whitespace, and typo
  checks.

Use the same shape in other repositories, substituting their actual runner and
commands. Never copy Arco commands into a different project without verifying
the local source of truth.

## Documentation/code coupling

When behavior changes, update the affected docs and their executable examples in
the same change. A feature is not complete when its user, operator, or
contributor documentation is missing. Report skipped docs suites, unavailable
optional dependencies, and known example gaps explicitly.
