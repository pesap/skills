# Public contracts and docstrings

Read when changing public docstrings or array contracts. Follow an explicit
repository convention; otherwise use NumPy-style sections where they add useful
contract information. Do not repeat an obvious signature in several sections.

## Describe what the caller needs

- A concise imperative summary.
- Input constraints, units, defaults, and relevant context/flag behavior.
- Outputs, mutation, ownership, and any partial-success semantics.
- For Result APIs, describe `Ok` and `Err` payloads under `Returns`. Use `Raises`
  only for exceptions that actually escape, not errors returned inside `Err`.
- A runnable normal example and important edge/error examples for non-obvious
  contracts. Omit inapplicable sections rather than adding filler.

Document the supported public facade; callers should not need implementation
module names to use the API. Explain non-obvious invariants and decisions in
comments, not line-by-line narration.

## Executable example

This ordinary computation returns an `int`, not an unnecessary Result wrapper.

```python
def total_counts(counts: tuple[int, ...], /) -> int:
    """Sum record counts across batches.

    Parameters
    ----------
    counts : tuple[int, ...]
        Record counts for the batches, in batch order.

    Returns
    -------
    int
        Total records; zero for no batches.

    Examples
    --------
    >>> total_counts((2, 3))
    5
    >>> total_counts(())
    0
    """
    return sum(counts)
```

Standard doctest expects bare output after `>>>`, as shown. For copy/paste
scripts, use executable assertions instead. Use comment-prefixed expected output
only when the repository has a verified runner for that syntax; do not tell a
normal doctest runner that `# 5` is the output of an expression returning `5`.

## Arrays and structured results

For each public array input or output, document:

- dtype when it matters;
- shape with domain names, such as `(n_branches,)`;
- the meaning of each axis;
- units, ownership, views/copies, and mutation behavior when relevant.

Return a named domain record rather than a long opaque positional tuple of
arrays. Do not introduce NumPy solely to document data or use an array type
where a simpler existing contract suffices.

## Validation

Run the project's actual documentation checks. For Python module docstrings,
pytest's `--doctest-modules` applies; for Markdown containing doctest prompts,
`--doctest-glob='*.md'` applies. Neither executes arbitrary fenced Python blocks.
This skill's example tests explicitly execute its complete Python fences and
then check their docstrings. Report checks that were not run.
