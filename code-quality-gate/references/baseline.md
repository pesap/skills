# Fallback quality baseline

Use this only when the repository does not provide an applicable rule or
canonical check. Project guidance always takes precedence.

- The change is scoped to the requested behavior and does not add unrelated
  churn.
- New or changed behavior has focused tests or an explicit reason tests are not
  meaningful.
- Formatting, linting, type checking, and build validation use the project's
  available tools.
- Errors are handled explicitly; no debug output, ignored failures, or silent
  fallbacks are introduced.
- New inputs are validated at trust boundaries and secrets are not committed or
  printed.
- Public interfaces and serialized/configured contracts remain compatible
  unless the change explicitly requires otherwise.
- Comments explain non-obvious rationale or invariants rather than restating
  code.
- Documentation or examples are updated when user-visible behavior or public
  interfaces change.
- The final validation result is reproducible from the reported commands.
