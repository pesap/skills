"""Validate the Rust skill's metadata and executable public contracts."""

import json
import re
import shlex
import subprocess
from pathlib import Path

import pytest

SKILL = Path(__file__).resolve().parents[1]


def test_skill_name_matches_directory() -> None:
    frontmatter = (SKILL / "SKILL.md").read_text().split("---", 2)[1]
    assert "name: rust\n" in frontmatter
    assert SKILL.name == "rust"
    assert not (SKILL.parent / "rust-pesap").exists()


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command, cwd=cwd, capture_output=True, text=True, timeout=120, check=False
    )


@pytest.fixture(scope="module")
def examples(tmp_path_factory: pytest.TempPathFactory) -> Path:
    directory = tmp_path_factory.mktemp("rust-examples")
    for crate, document in [
        ("simple_counts", "SKILL.md"),
        ("count_import", "references/contracts.md"),
    ]:
        blocks = re.findall(
            r"^```rust\n(.*?)^```$", (SKILL / document).read_text(), re.M | re.S
        )
        assert len(blocks) == 1, document
        source = directory / f"{crate}.rs"
        source.write_text(blocks[0])
        result = run(
            [
                "rustc",
                "--edition=2021",
                "--crate-type=lib",
                "--crate-name",
                crate,
                "-D",
                "warnings",
                str(source),
                "-o",
                str(directory / f"lib{crate}.rlib"),
            ],
            directory,
        )
        assert result.returncode == 0, result.stdout + result.stderr
    return directory


def test_examples_through_public_imports(examples: Path) -> None:
    executable = examples / "contracts"
    result = run(
        [
            "rustc",
            "--edition=2021",
            "--test",
            "-D",
            "warnings",
            "--extern",
            f"simple_counts={examples / 'libsimple_counts.rlib'}",
            "--extern",
            f"count_import={examples / 'libcount_import.rlib'}",
            str(SKILL / "tests/contracts.rs"),
            "-o",
            str(executable),
        ],
        examples,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    result = run([str(executable)], examples)
    assert result.returncode == 0, result.stdout + result.stderr


def test_implementation_module_is_not_a_public_import(examples: Path) -> None:
    source = examples / "private_import.rs"
    source.write_text("use count_import::count_import::parse_counts;\nfn main() {}\n")
    result = run(
        [
            "rustc",
            "--edition=2021",
            "--extern",
            f"count_import={examples / 'libcount_import.rlib'}",
            str(source),
            "-o",
            str(examples / "private_import"),
        ],
        examples,
    )
    assert result.returncode != 0
    assert "E0603" in result.stderr, result.stderr


def test_fallback_checks_preserve_source_and_default_features(tmp_path: Path) -> None:
    (tmp_path / "Cargo.toml").write_text(
        '[package]\nname = "feature-fixture"\nversion = "0.0.0"\nedition = "2021"\n'
        '[features]\ndefault = ["local"]\nlocal = []\nremote = []\n'
    )
    (tmp_path / "src").mkdir()
    source = tmp_path / "src/lib.rs"
    original = (
        '#[cfg(all(feature = "local", feature = "remote"))]\n'
        'compile_error!("incompatible backends");\n'
        "pub fn count()->u32{2}\n"
    )
    source.write_text(original)
    result = run(["cargo", "generate-lockfile", "--offline"], tmp_path)
    assert result.returncode == 0, result.stderr
    lockfile = (tmp_path / "Cargo.lock").read_bytes()

    result = run(
        ["cargo", "check", "--offline", "--locked", "--all-features"], tmp_path
    )
    assert result.returncode != 0
    assert "incompatible backends" in result.stderr, result.stderr

    blocks = re.findall(
        r"^```bash\n(.*?)^```$", (SKILL / "SKILL.md").read_text(), re.M | re.S
    )
    assert len(blocks) == 1
    commands = [shlex.split(line) for line in blocks[0].splitlines()]
    assert len(commands) == 3
    for command in commands:
        is_format = command[:2] == ["cargo", "fmt"]
        if not is_format:
            command.insert(2, "--offline")
        result = run(command, tmp_path)
        assert result.returncode == (1 if is_format else 0), (
            result.stdout + result.stderr
        )
        assert source.read_text() == original
        assert (tmp_path / "Cargo.lock").read_bytes() == lockfile


def test_development_case_metadata_is_consistent() -> None:
    designs = json.loads((SKILL / "evals/evals.json").read_text())
    assert designs["skill_name"] == "rust"
    assert designs["status"] == "case-designs-not-executed"
    triggers = json.loads((SKILL / "evals/trigger-prompts.json").read_text())
    for cases in (designs["evals"], triggers):
        assert len({case["id"] for case in cases}) == len(cases)
    assert all(isinstance(case["should_trigger"], bool) for case in triggers)


def test_local_reference_links_resolve() -> None:
    documents = [
        SKILL / "SKILL.md",
        *SKILL.glob("references/*.md"),
        *SKILL.glob("evals/*.md"),
    ]
    for path in documents:
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if not target.startswith(("https://", "http://", "#")):
                assert (path.parent / target.split("#", 1)[0]).is_file(), (path, target)
