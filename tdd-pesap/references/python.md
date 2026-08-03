# Python testing

Use pytest conventions while applying the core TDD Pesap doctrine.

- Prefer public package APIs, CLI entry points, or service boundaries over
  private helpers.
- Use `@pytest.mark.parametrize` for explicit behavior matrices.
- Use Hypothesis for invariants and broad input exploration when examples are
  insufficient.
- Keep fixtures explicit and deterministic. Choose the narrowest useful scope;
  avoid hidden coupling and unjustified `autouse` fixtures.
- Keep shared fixtures in `conftest.py` or project plugins only when they are
  genuinely shared; keep local setup near the tests that use it.
- Mock HTTP, external SDKs, time/randomness, filesystem/process edges, and
  other real boundaries when needed. Do not deep-mock domain modules you own.
- Prefer focused test runs during RED/GREEN cycles, then run the project's
  broader pytest command before completion.

Useful commands, adapted to the repository's toolchain:

```bash
pytest -q -k '<behavior>'
pytest --lf -q
pytest -k '<behavior>' -vv --maxfail=1 --pdb
pytest --cov --cov-report=term-missing
```

Use `uv run pytest ...` when the project manages execution with uv.
