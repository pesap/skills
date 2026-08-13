# Python patterns

Read this reference only when a concrete good/bad pattern would remove
ambiguity. Apply the repository's established pattern when it differs.

## Contents

- [Function signatures](#function-signatures)
- [Structured returns](#structured-returns)
- [Exception handling](#exception-handling)
- [Async code](#async-code)
- [Logging and output](#logging-and-output)
- [Naming and entrypoints](#naming-and-entrypoints)
- [NumPy array bundles](#numpy-array-bundles)
- [JSON and table rows](#json-and-table-rows)
- [Useful helper returns](#useful-helper-returns)
- [Benchmark scripts](#benchmark-scripts)
- [Memory measurement](#memory-measurement)
- [`rust_ok` results](#rust_ok-results)
- [Type boundaries](#type-boundaries)

## Function signatures

```python
# ✅ Do
from pathlib import Path

def resolve_path(
    path: Path,
    *,
    base_folder: Path,
    must_exist: bool = True,
) -> Path:
    ...

# ❌ Don't
# unclear subject + too many positional params
def resolve_path(raw_path: Path, folder_path: Path, must_exist: bool = True):
    ...
```

## Structured returns

```python
# ✅ Do
from dataclasses import dataclass

@dataclass(slots=True)
class ParseResult:
    records: list[str]
    rejected: int


def parse_records(raw: str, *, strict: bool = True) -> ParseResult:
    records = [line.strip() for line in raw.splitlines() if line.strip()]
    if strict and not records:
        raise ValueError("no records parsed")
    return ParseResult(records=records, rejected=0)

# ❌ Don't
# loose tuple return without semantics
def parse_records(raw: str):
    ...
    return records, rejected
```

## Exception handling

```python
# ✅ Do
import json

try:
    payload = json.loads(raw)
except json.JSONDecodeError as exc:
    raise ValueError("invalid JSON payload") from exc

# ✅ Do at Result boundaries
from rust_ok import Err, Ok, Result


def parse_payload(raw: str) -> Result[Payload, ValueError]:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        return Err(ValueError("invalid JSON payload"))
    return Ok(Payload.model_validate(payload))

# ❌ Don't
# catch-all hides root cause; success-by-None hides the contract
try:
    payload = json.loads(raw)
    validated = Payload.model_validate(payload)
    cache_payload(validated)
except Exception:
    return None
```

## Async code

```python
# ✅ Do
import asyncio

await asyncio.sleep(0.1)

# ❌ Don't
import time

time.sleep(0.1)
```

## Logging and output

```python
# ✅ Do
from loguru import logger

logger.disable("my_package")  # users opt in with logger.enable("my_package")
logger.bind(command="run", model="dense-lp").info("command started")
logger.bind(exit_code=1).error("command failed")

# ❌ Don't
if result.returncode == 0:
    print("  ✓ ok")
    continue

failures += 1
print(f"  ✗ failed (exit {result.returncode})")
```

## Naming and entrypoints

```python
# ✅ Do
import argparse


def parse_examples_csv(raw: str) -> list[str]:
    return [item.strip() for item in raw.split(",") if item.strip()]


def run_example_cli_smoke(items: list[str]) -> SmokeSummary:
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--examples", required=True)
    args = parser.parse_args()
    summary = run_example_cli_smoke(parse_examples_csv(args.examples))
    print(summary.model_dump_json())

# ❌ Don't

def _parse_examples_csv(raw: str):
    ...


def main() -> None:
    ...


if __name__ == "__main__":
    main()
```

## NumPy array bundles

```python
# ✅ Do
from dataclasses import dataclass

import numpy as np
import numpy.typing as npt

FloatArray = npt.NDArray[np.float64]
IntArray = npt.NDArray[np.int64]


@dataclass(frozen=True)
class NetworkArrays:
    buses: list[str]
    branches: list[str]
    from_bus: IntArray  # shape: (n_branches,)
    to_bus: IntArray  # shape: (n_branches,)
    weights: FloatArray  # shape: (n_branches,)
    diagonal: FloatArray  # shape: (n_buses - 1,)


def arrays_from_system(system: System) -> NetworkArrays:
    ...
    return NetworkArrays(
        buses=buses,
        branches=branches,
        from_bus=from_bus,
        to_bus=to_bus,
        weights=weights,
        diagonal=diagonal,
    )

# ❌ Don't
# impossible to know what each array means from the signature
def arrays_from_system(system: System) -> tuple[
    list[str],
    list[str],
    np.ndarray,
    np.ndarray,
    np.ndarray,
    np.ndarray,
]:
    ...
```

## JSON and table rows

```python
# ✅ Do
from typing import TypedDict


class ResultRow(TypedDict):
    implementation: str
    n: int
    converged: bool
    runtime_ms: float | None


RowsByCase = dict[tuple[int, float], list[ResultRow]]


def build_rows(path: Path) -> list[ResultRow]:
    ...

# ❌ Don't
from typing import Any


def build_rows(path: Path) -> list[dict[str, Any]]:
    ...
```

## Useful helper returns

```python
# ✅ Do
from rust_ok import Ok, Result


def validate_inputs(inputs: Inputs) -> Inputs:
    if inputs.count < 1:
        raise ValueError("count must be positive")
    return inputs


def write_summary(path: Path, rows: list[ResultRow]) -> Path:
    ...
    return path


def prepare_cache(cache: Cache) -> Result[None, CacheError]:
    cache.reserve()
    return Ok(None)

# ❌ Don't

def validate_inputs(inputs: Inputs) -> None:
    if inputs.count < 1:
        raise ValueError("count must be positive")


def write_summary(path: Path, rows: list[ResultRow]) -> None:
    ...
```

## Benchmark scripts

```python
# ✅ Do
@dataclass(frozen=True)
class BenchmarkSummary:
    converged_rows: int
    query_lines: int
    checksum: float


def compute_rows(arrays: NetworkArrays, *, query_lines: int) -> BenchmarkComputation:
    ...


def run_benchmark(*, n: int, k: float, query_lines: int) -> BenchmarkSummary:
    arrays = arrays_from_system(build_system(n, k))
    computation = compute_rows(arrays, query_lines=query_lines)
    return computation.summary


if __name__ == "__main__":
    inputs = parse_inputs()
    print(summary_json(run_benchmark(...)))

# ❌ Don't

def run_benchmark(...) -> None:
    ...
    print(json.dumps(summary))
```

## Memory measurement

Use the repository's reproducible benchmark harness for memory claims.

```bash
# ✅ Do: invoke the project-defined runner with a bounded command
<project-memory-runner> -- uv run --locked python <benchmark-script>

# ❌ Don't
python -m memory_profiler my_script.py
python - <<'PY'
import tracemalloc
# in-process memory probes do not produce benchmark memory numbers
PY
```

## `rust_ok` results

```python
# ✅ Do
from rust_ok import is_err

result = parse_payload(raw)
if is_err(result):
    return result
payload = result.ok()

# ❌ Don't
payload = parse_payload(raw).unwrap()
```

## Type boundaries

```python
# ✅ Do
from typing import Protocol


class HasName(Protocol):
    name: str


def component_name(component: HasName) -> str:
    return component.name

# ❌ Don't
from typing import cast


def component_name(component: object) -> str:
    return cast("Component", component).name
```
