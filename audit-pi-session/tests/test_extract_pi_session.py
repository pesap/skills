from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parents[1] / "scripts"))

from extract_pi_session import (
    ExportFormatError,
    build_active_path,
    build_entry_records,
    build_path,
    build_summary,
    build_tool_records,
    read_pi_export,
)


def write_export(tmp_path: Path, session_data: dict[str, object]) -> Path:
    encoded = base64.b64encode(json.dumps(session_data).encode()).decode()
    export_path = tmp_path / "session.html"
    export_path.write_text(
        f'<html><script type="application/json" id="session-data">\n{encoded}\n</script></html>',
        encoding="utf-8",
    )
    return export_path


def test_reads_export_and_reconstructs_active_branch(tmp_path: Path) -> None:
    export_path = write_export(
        tmp_path,
        {
            "header": {"type": "session", "version": 3, "id": "session-1", "cwd": "/repo"},
            "entries": [
                {
                    "type": "message",
                    "id": "user0001",
                    "parentId": None,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "message": {"role": "user", "content": "Fix it"},
                },
                {
                    "type": "message",
                    "id": "old00001",
                    "parentId": "user0001",
                    "timestamp": "2026-01-01T00:00:01Z",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "Old approach"}]},
                },
                {
                    "type": "message",
                    "id": "new00001",
                    "parentId": "user0001",
                    "timestamp": "2026-01-01T00:00:02Z",
                    "message": {"role": "assistant", "content": [{"type": "text", "text": "New approach"}]},
                },
            ],
            "leafId": "new00001",
            "systemPrompt": "Be useful",
            "tools": [],
        },
    )

    session = read_pi_export(export_path)

    assert session.header.session_id == "session-1"
    assert session.header.version == 3
    assert [entry.entry_id for entry in build_active_path(session)] == ["user0001", "new00001"]
    assert [entry.entry_id for entry in build_path(session, "old00001")] == ["user0001", "old00001"]
    active_records = build_entry_records(
        build_active_path(session),
        max_text_chars=5,
        include_thinking=False,
    )
    assert active_records[0]["text"] == "Fix i\n[truncated 1 chars]"
    assert active_records[1]["thinkingChars"] == 0
    assert "thinking" not in active_records[1]

    summary = build_summary(session, export_path)
    assert summary["metrics"]["global"]["assistantMessages"] == 2
    assert summary["metrics"]["activePath"]["assistantMessages"] == 1
    assert summary["branches"] == [
        {
            "leafId": "old00001",
            "isActive": False,
            "entryCount": 2,
            "lastTimestamp": "2026-01-01T00:00:01Z",
            "lastEntryType": "message",
        },
        {
            "leafId": "new00001",
            "isActive": True,
            "entryCount": 2,
            "lastTimestamp": "2026-01-01T00:00:02Z",
            "lastEntryType": "message",
        },
    ]


def test_correlates_tool_calls_with_results(tmp_path: Path) -> None:
    export_path = write_export(
        tmp_path,
        {
            "header": {"version": 3, "id": "session-2"},
            "entries": [
                {
                    "type": "message",
                    "id": "assistant1",
                    "parentId": None,
                    "timestamp": "2026-01-01T00:00:00Z",
                    "message": {
                        "role": "assistant",
                        "content": [
                            {"type": "toolCall", "id": "call-1", "name": "bash", "arguments": {"command": "pytest"}},
                            {"type": "toolCall", "id": "call-2", "name": "read", "arguments": {"path": "x.py"}},
                        ],
                    },
                },
                {
                    "type": "message",
                    "id": "result001",
                    "parentId": "assistant1",
                    "timestamp": "2026-01-01T00:00:01Z",
                    "message": {
                        "role": "toolResult",
                        "toolCallId": "call-1",
                        "toolName": "bash",
                        "content": [{"type": "text", "text": "1 failed"}],
                        "isError": True,
                    },
                },
            ],
            "leafId": "result001",
        },
    )

    records = build_tool_records(read_pi_export(export_path))

    assert [record.as_json() for record in records] == [
        {
            "toolCallId": "call-1",
            "toolName": "bash",
            "callEntryId": "assistant1",
            "arguments": {"command": "pytest"},
            "resultEntryId": "result001",
            "isError": True,
            "resultText": "1 failed",
        },
        {
            "toolCallId": "call-2",
            "toolName": "read",
            "callEntryId": "assistant1",
            "arguments": {"path": "x.py"},
            "resultEntryId": None,
            "isError": None,
            "resultText": "",
        },
    ]


def test_rejects_html_without_pi_session_data(tmp_path: Path) -> None:
    export_path = tmp_path / "not-an-export.html"
    export_path.write_text("<html><body>hello</body></html>", encoding="utf-8")

    with pytest.raises(ExportFormatError, match="session-data"):
        read_pi_export(export_path)
