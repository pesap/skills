---
name: docs-pesap
description:
  Pesap's standard for accurate, task-oriented technical documentation. Use
  when creating or revising READMEs, API documentation, tutorials, how-to
  guides, explanations, setup, troubleshooting, migration, release notes, or
  GitHub-rendered Markdown. Apply when documentation must be grounded in the
  repository's actual code and commands, not marketing copy.
license: MIT
---

# Docs Pesap

Write documentation that lets the intended reader complete a real task and
trust the result. Project terminology, source code, configuration, and existing
docs are the source of truth; generic guidance is only a fallback.

## First classify the document

Use the Diataxis shape that matches the reader's need. Do not combine all four
modes into one undifferentiated page:

- **Tutorial** — learning-oriented, guided, and deliberately narrow. Lead the
  reader to a working result; do not make it an exhaustive reference.
- **How-to guide** — task-oriented instructions for a known goal. State
  prerequisites, numbered actions, verification, and recovery paths.
- **Reference** — accurate, complete, and structured information: APIs, flags,
  configuration, schemas, options, defaults, errors, and compatibility notes.
- **Explanation** — concepts, rationale, architecture, trade-offs, and why the
  system behaves as it does. Do not disguise explanation as a procedure.

When a page needs multiple modes, split it into linked pages rather than making
one page serve conflicting purposes.

## Workflow

1. **Identify the reader and outcome.** State who the document is for, what they
   need to accomplish, and what counts as success.
2. **Discover the source of truth.** Inspect the implementation, public APIs,
   configuration, scripts, tests, CI, existing terminology, and related docs.
   Verify every command, flag, path, version, output, and behavior you claim.
3. **Choose the document shape.** Apply the appropriate Diataxis mode and keep
   the page focused on that mode.
4. **Write the shortest complete path.** Put prerequisites before actions,
   include hidden setup explicitly, and show the validation step immediately
   after the action it verifies.
5. **Harden examples.** Use typed fenced blocks, realistic placeholders, exact
   commands, and no invented APIs or filenames. Keep command examples
   copy-pasteable: when showing expected output inline, put it in a single
   `#`-prefixed comment value (for example, `# created`) rather than an
   uncommented line that the user would accidentally execute.
6. **Optimize navigation and rendering.** Use descriptive headings, relative
   repository links, useful navigation, and GitHub-safe Markdown.
7. **Validate before delivery.** Check links, code examples, commands, generated
   API output, Markdown rendering, and repository documentation checks when
   available.

If a claim cannot be verified, label it as an assumption or omit it. Never make
stale or uncertain instructions sound authoritative.

## Documentation testing

If the user asks for documentation testing, read
[references/documentation-testing.md](references/documentation-testing.md) before
planning or implementing the work. Treat documentation examples and vocabulary
as executable contracts when the project supports that pattern. The reference
covers the generalized Arco approach:

- execute marked doctest examples;
- test project-specific API vocabulary and forbidden legacy forms;
- separate beginner examples from expert-only APIs with narrow allowlists;
- test the guard itself with both forbidden and allowed fixtures;
- run fast local docs checks, formatting/spelling/link hooks, and the CI docs
  gate;
- trigger docs CI when docs, the runner, setup, or command definitions change.

Use the repository's real commands and test runner; do not assume Arco's
`just` targets exist elsewhere.

## README standard

A README should provide a learning ladder:

1. What the project is, who it is for, and its key constraint.
2. A 30–90 second quickstart with exact install/run commands.
3. Expected output and a small success check.
4. Core concepts and the normal workflow.
5. Links to tutorials, how-to guides, API reference, explanations, and
   troubleshooting.
6. Advanced configuration, extension points, and limitations.

Keep badges minimal and meaningful. Avoid turning the README into a complete
manual; link to deeper documents.

## API documentation standard

Document the public contract, not the implementation:

- purpose and stability status;
- inputs, types, defaults, constraints, and required fields;
- outputs and state changes;
- errors, failure conditions, and retry/side-effect behavior;
- authentication, permissions, pagination, limits, and versioning where
  applicable;
- one realistic example and one important edge case.

Generate or validate API details from the actual contract when tooling exists.
Do not duplicate a generated reference manually unless the source contract is
also updated.

## GitHub rendering standard

- Use a logical heading hierarchy; do not skip heading levels.
- Prefer short paragraphs, lists, and numbered procedures.
- Use tables for compact comparison or lookup, not for long prose.
- Use relative links for repository files and verify their targets.
- Use GitHub callouts only when they add signal: `[!NOTE]`, `[!TIP]`,
  `[!IMPORTANT]`, `[!WARNING]`, or `[!CAUTION]`.
- Use `<details>` for optional depth, never for required steps.
- Use Mermaid only for simple diagrams that remain useful in source form.
- Keep badges, emoji, decorative HTML, and screenshots purposeful and
  accessible.
- Keep code blocks copy-paste safe and label their language.

## Quality gate

Before delivery, confirm:

- the primary reader can complete the intended task in one pass;
- all claims and examples match current source truth;
- prerequisites, permissions, side effects, and failure recovery are explicit;
- commands and code examples are runnable or clearly marked as pseudocode;
- links, anchors, generated references, and Markdown rendering validate;
- the page uses one clear Diataxis mode or links cleanly to pages with other
  modes;
- no marketing claims, filler, hidden steps, or unsupported certainty remain.

## Output

- Files and sections changed.
- Reader, outcome, and Diataxis mode.
- Source-of-truth files consulted.
- Validation commands and results.
- Assumptions, unverifiable claims, and remaining documentation gaps.
