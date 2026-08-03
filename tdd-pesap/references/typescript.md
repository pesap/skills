# TypeScript testing

Apply the core behavior-first doctrine through the repository's existing test
runner (for example Vitest, Jest, or a project-specific runner). Do not impose a
new framework.

- Test exported functions, public classes, HTTP/CLI boundaries, or user-visible
  behavior rather than private helpers.
- Keep test data typed and explicit; use builders only when they reduce real
  setup duplication without hiding the behavior under test.
- Prefer independent expected values and meaningful error assertions over
  snapshots that merely mirror implementation output.
- Mock network, time, randomness, processes, and other external boundaries, but
  prefer real internal modules.
- Keep type-checking separate from runtime tests and run the repository's
  `tsc --noEmit` or equivalent gate when the project requires it.
- Use focused test commands during each cycle, then the project's full test and
  type-check commands before completion.
