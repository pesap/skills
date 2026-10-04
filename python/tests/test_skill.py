"""Check the skill's discoverable identity and executable contracts."""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]


def python_blocks(path: Path) -> list[str]:
    return re.findall(r"^```python\n(.*?)^```$", path.read_text(), re.M | re.S)


def run_example(source: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-I", "-B", "-c", source],
        capture_output=True,
        text=True,
        check=False,
    )


def test_skill_name_matches_directory() -> None:
    frontmatter = (SKILL / "SKILL.md").read_text().split("---", 2)[1]
    assert "name: python\n" in frontmatter
    assert SKILL.name == "python"
    assert not (SKILL.parent / "python-pesap").exists()


@pytest.mark.parametrize(
    ("tool", "arguments"),
    [
        (
            "ruff",
            [
                "check",
                "--preview",
                "--select",
                "ALL",
                "--no-fix",
                "--no-fix-only",
                "--no-unsafe-fixes",
                "--output-format",
                "full",
            ],
        ),
        ("ty", ["check", "--error-on-warning", "--output-format", "full"]),
    ],
)
@pytest.mark.parametrize("paths", [[], ["with spaces.py", "-report.py"]])
def test_audit_preserves_paths_cwd_and_exit_status(
    tmp_path: Path, tool: str, arguments: list[str], paths: list[str]
) -> None:
    tools = tmp_path / "tools"
    tools.mkdir()
    for name in ("ruff", "ty", "uv", "uvx"):
        executable = tools / name
        executable.write_text(
            f"#!{sys.executable}\n"
            "import json, os, sys\n"
            'print(json.dumps({"args": sys.argv[1:], "cwd": os.getcwd()}))\n'
            f"sys.exit({7 if name == tool else 99})\n"
        )
        executable.chmod(0o755)
    subprocess.run(["git", "init", "--quiet", str(tmp_path)], check=True)
    working = tmp_path / "nested"
    working.mkdir()
    environment = dict(os.environ, PATH=str(tools) + os.pathsep + os.environ["PATH"])

    result = subprocess.run(
        ["bash", str(SKILL / "scripts" / f"check_pedantic_{tool}.sh"), *paths],
        cwd=working,
        env=environment,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 7, result.stderr
    assert json.loads(result.stdout) == {
        "args": [*arguments, "--", *(paths or ["."])],
        "cwd": str(working),
    }


@pytest.mark.parametrize(
    "document", ["SKILL.md", "references/patterns.md", "references/docstrings.md"]
)
def test_document_examples_and_doctests_execute(document: str) -> None:
    blocks = python_blocks(SKILL / document)
    assert blocks, document
    for source in blocks:
        result = run_example(
            source + "\nimport doctest\nassert doctest.testmod().failed == 0\n"
        )
        assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(
    ("raw", "base", "expected"),
    [("42", 10, 42), ("-3", 10, -3), ("2a", 16, 42), ("", 10, None), ("2", 2, None)],
)
def test_integer_result_preserves_success_and_conversion_errors(
    raw: str, base: int, expected: int | None
) -> None:
    source = python_blocks(SKILL / "SKILL.md")[0]
    assertion = (
        "assert is_err(result) and isinstance(result.err(), ValueError)"
        if expected is None
        else f"assert is_ok(result) and result.ok() == {expected!r}"
    )
    result = run_example(
        source
        + "\nfrom rust_ok import is_err, is_ok\n"
        + f"result = parse_integer({raw!r}, base={base!r})\n{assertion}\n"
    )
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("skip_empty", [False, True])
@pytest.mark.parametrize(
    ("raw", "kept", "filtered"),
    [
        ("name\n\nalice\n", [["name"], [], ["alice"]], [["name"], ["alice"]]),
        ('""\n\n', [[""], []], [[""]]),
        (" \n\n", [[" "], []], [[" "]]),
        ("", [], []),
    ],
)
def test_csv_flag_preserves_meaningful_records(
    raw: str, kept: list[list[str]], filtered: list[list[str]], skip_empty: bool
) -> None:
    source = python_blocks(SKILL / "references/patterns.md")[0]
    expected = filtered if skip_empty else kept
    checks = (
        "\nfrom rust_ok import is_ok\n"
        f"result = parse_csv({raw!r}, ctx=CsvImportContext(skip_empty_records={skip_empty!r}))\n"
        f"assert is_ok(result) and result.ok() == {expected!r}\n"
    )
    result = run_example(source + checks)
    assert result.returncode == 0, result.stdout + result.stderr


def test_csv_context_is_required_keyword_only_and_immutable() -> None:
    source = python_blocks(SKILL / "references/patterns.md")[0]
    checks = """
from dataclasses import FrozenInstanceError
from inspect import Parameter, signature

parameters = signature(parse_csv).parameters
assert parameters["raw"].kind is Parameter.POSITIONAL_ONLY
assert parameters["ctx"].kind is Parameter.KEYWORD_ONLY
assert parameters["ctx"].default is Parameter.empty
for args, kwargs in [(("a",), {}), (("a", CsvImportContext()), {}), ((), {"raw": "a", "ctx": CsvImportContext()})]:
    try:
        parse_csv(*args, **kwargs)
    except TypeError:
        pass
    else:
        raise AssertionError("invalid call accepted")
ctx = CsvImportContext()
try:
    ctx.skip_empty_records = True
except FrozenInstanceError:
    pass
else:
    raise AssertionError("context mutation accepted")
"""
    result = run_example(source + checks)
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize("skip_empty", [False, True])
def test_csv_flag_never_bypasses_parse_errors(skip_empty: bool) -> None:
    source = python_blocks(SKILL / "references/patterns.md")[0]
    checks = (
        "\nfrom rust_ok import is_err\n"
        f"result = parse_csv('\"unterminated', ctx=CsvImportContext(skip_empty_records={skip_empty!r}))\n"
        "assert is_err(result) and isinstance(result.err(), csv.Error)\n"
        "assert result.err().__traceback__ is not None\n"
    )
    result = run_example(source + checks)
    assert result.returncode == 0, result.stdout + result.stderr


def test_development_case_metadata_is_consistent() -> None:
    design = json.loads((SKILL / "evals/evals.json").read_text())
    assert design["skill_name"] == "python"
    assert design["status"] == "case-designs-not-executed"
    triggers = json.loads((SKILL / "evals/trigger-prompts.json").read_text())
    for cases in (design["evals"], triggers):
        assert len({case["id"] for case in cases}) == len(cases)
    assert all(isinstance(case["should_trigger"], bool) for case in triggers)


def test_local_reference_links_resolve() -> None:
    for path in [SKILL / "SKILL.md", *sorted((SKILL / "references").glob("*.md"))]:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not target.startswith(("https://", "http://", "#")):
                assert (path.parent / target.split("#", 1)[0]).is_file(), (path, target)
