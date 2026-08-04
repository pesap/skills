#!/usr/bin/env python3
"""Extract structured, branch-aware data from a Pi HTML session export."""

from __future__ import annotations

import argparse
import base64
import binascii
import json
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import TypeAlias

JsonValue: TypeAlias = None | bool | int | float | str | list["JsonValue"] | dict[str, "JsonValue"]
JsonObject: TypeAlias = dict[str, JsonValue]


class ExportFormatError(ValueError):
    """Report that an input is not a supported Pi HTML session export."""


@dataclass(frozen=True)
class SessionHeader:
    """Identify the exported Pi session."""

    session_id: str
    version: int | None
    timestamp: str | None
    cwd: str | None
    raw: JsonObject


@dataclass(frozen=True)
class SessionEntry:
    """Represent one entry in Pi's session tree."""

    entry_id: str
    parent_id: str | None
    entry_type: str
    timestamp: str | None
    raw: JsonObject


@dataclass(frozen=True)
class PiSession:
    """Contain validated session export data."""

    header: SessionHeader
    entries: tuple[SessionEntry, ...]
    leaf_id: str | None
    raw: JsonObject


@dataclass(frozen=True)
class ToolRecord:
    """Correlate a tool call with its result, when present."""

    tool_call_id: str
    tool_name: str
    call_entry_id: str
    arguments: JsonObject
    result_entry_id: str | None
    is_error: bool | None
    result_text: str

    def as_json(self, *, max_text_chars: int | None = None) -> JsonObject:
        """Return a JSON-compatible tool record."""
        return {
            "toolCallId": self.tool_call_id,
            "toolName": self.tool_name,
            "callEntryId": self.call_entry_id,
            "arguments": _bound_json(self.arguments, max_text_chars),
            "resultEntryId": self.result_entry_id,
            "isError": self.is_error,
            "resultText": _bound_text(self.result_text, max_text_chars),
        }


class _SessionDataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self._is_target = False
        self.fragments: list[str] = []
        self.matches = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        self._is_target = tag.lower() == "script" and attributes.get("id") == "session-data"
        if self._is_target:
            self.matches += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "script":
            self._is_target = False

    def handle_data(self, data: str) -> None:
        if self._is_target:
            self.fragments.append(data)


def read_pi_export(path: Path) -> PiSession:
    """Decode and validate the structured session embedded in a Pi HTML export."""
    try:
        html = path.read_text(encoding="utf-8")
    except OSError as error:
        raise ExportFormatError(f"Cannot read export {path}: {error}") from error

    parser = _SessionDataParser()
    parser.feed(html)
    if parser.matches != 1:
        raise ExportFormatError(
            f"Expected one Pi session-data script, found {parser.matches}; input may not be a Pi HTML export"
        )

    encoded = "".join("".join(parser.fragments).split())
    try:
        decoded = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError) as error:
        raise ExportFormatError("Pi session-data is not valid base64") from error

    try:
        decoded_text = decoded.decode("utf-8")
    except UnicodeDecodeError as error:
        raise ExportFormatError("Decoded Pi session-data is not UTF-8") from error

    try:
        data: JsonValue = json.loads(decoded_text)
    except json.JSONDecodeError as error:
        raise ExportFormatError(f"Decoded Pi session-data is not valid JSON: {error.msg}") from error

    root = _require_object(data, "session-data")
    header_data = _require_object(root.get("header"), "session-data.header")
    entries_data = _require_array(root.get("entries"), "session-data.entries")

    session_id = _require_string(header_data.get("id"), "session-data.header.id")
    version = _optional_int(header_data.get("version"), "session-data.header.version")
    header = SessionHeader(
        session_id=session_id,
        version=version,
        timestamp=_optional_string(header_data.get("timestamp"), "session-data.header.timestamp"),
        cwd=_optional_string(header_data.get("cwd"), "session-data.header.cwd"),
        raw=header_data,
    )

    entries: list[SessionEntry] = []
    known_ids: set[str] = set()
    for index, value in enumerate(entries_data):
        label = f"session-data.entries[{index}]"
        entry_data = _require_object(value, label)
        entry_id = _require_string(entry_data.get("id"), f"{label}.id")
        if entry_id in known_ids:
            raise ExportFormatError(f"Duplicate session entry id: {entry_id}")
        known_ids.add(entry_id)
        entries.append(
            SessionEntry(
                entry_id=entry_id,
                parent_id=_optional_string(entry_data.get("parentId"), f"{label}.parentId"),
                entry_type=_require_string(entry_data.get("type"), f"{label}.type"),
                timestamp=_optional_string(entry_data.get("timestamp"), f"{label}.timestamp"),
                raw=entry_data,
            )
        )

    leaf_id = _optional_string(root.get("leafId"), "session-data.leafId")
    if leaf_id is not None and leaf_id not in known_ids:
        raise ExportFormatError(f"Session leafId references missing entry: {leaf_id}")

    for entry in entries:
        if entry.parent_id is not None and entry.parent_id not in known_ids:
            raise ExportFormatError(
                f"Entry {entry.entry_id} references missing parent: {entry.parent_id}"
            )

    return PiSession(header=header, entries=tuple(entries), leaf_id=leaf_id, raw=root)


def build_active_path(session: PiSession) -> tuple[SessionEntry, ...]:
    """Return entries from the root to Pi's active leaf."""
    if not session.entries:
        return ()

    # Pi's HTML renderer uses the final entry when an older export has no leafId.
    target_id = session.leaf_id or session.entries[-1].entry_id
    by_id = {entry.entry_id: entry for entry in session.entries}
    reverse_path: list[SessionEntry] = []
    visited: set[str] = set()
    current_id: str | None = target_id

    while current_id is not None:
        if current_id in visited:
            raise ExportFormatError(f"Cycle detected in session tree at entry: {current_id}")
        visited.add(current_id)
        entry = by_id[current_id]
        reverse_path.append(entry)
        current_id = entry.parent_id

    return tuple(reversed(reverse_path))


def build_tool_records(
    session: PiSession,
    *,
    entries: tuple[SessionEntry, ...] | None = None,
) -> tuple[ToolRecord, ...]:
    """Correlate assistant tool calls with tool-result entries."""
    selected_entries = session.entries if entries is None else entries
    results: dict[str, SessionEntry] = {}

    for entry in selected_entries:
        message = _message_object(entry)
        if message is None or message.get("role") != "toolResult":
            continue
        tool_call_id = message.get("toolCallId")
        if isinstance(tool_call_id, str):
            results[tool_call_id] = entry

    records: list[ToolRecord] = []
    for entry in selected_entries:
        message = _message_object(entry)
        if message is None or message.get("role") != "assistant":
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue
        for block_value in content:
            if not isinstance(block_value, dict) or block_value.get("type") != "toolCall":
                continue
            call_id = _require_string(block_value.get("id"), f"tool call in {entry.entry_id}.id")
            name = _require_string(block_value.get("name"), f"tool call {call_id}.name")
            arguments_value = block_value.get("arguments")
            arguments = arguments_value if isinstance(arguments_value, dict) else {}
            result_entry = results.get(call_id)
            result_message = _message_object(result_entry) if result_entry is not None else None
            records.append(
                ToolRecord(
                    tool_call_id=call_id,
                    tool_name=name,
                    call_entry_id=entry.entry_id,
                    arguments=arguments,
                    result_entry_id=result_entry.entry_id if result_entry is not None else None,
                    is_error=_optional_bool_from_object(result_message, "isError"),
                    result_text=_extract_text(result_message.get("content")) if result_message is not None else "",
                )
            )

    return tuple(records)


def build_summary(session: PiSession, source_path: Path) -> JsonObject:
    """Build branch-aware metrics for an exported session."""
    active_path = build_active_path(session)
    children_ids = {
        entry.parent_id
        for entry in session.entries
        if entry.parent_id is not None
    }
    branches: list[JsonValue] = []
    effective_leaf_id = active_path[-1].entry_id if active_path else None
    for entry in session.entries:
        if entry.entry_id in children_ids:
            continue
        branch_path = build_path(session, entry.entry_id)
        branches.append(
            {
                "leafId": entry.entry_id,
                "isActive": entry.entry_id == effective_leaf_id,
                "entryCount": len(branch_path),
                "lastTimestamp": entry.timestamp,
                "lastEntryType": entry.entry_type,
            }
        )

    return {
        "schema": "audit-pi-session/v1",
        "source": {"path": str(source_path), "bytes": source_path.stat().st_size},
        "session": {
            "id": session.header.session_id,
            "version": session.header.version,
            "timestamp": session.header.timestamp,
            "cwd": session.header.cwd,
            "entryCount": len(session.entries),
            "activeLeafId": effective_leaf_id,
        },
        "metrics": {
            "global": _build_metrics(session.entries),
            "activePath": _build_metrics(active_path),
        },
        "branches": branches,
    }


def build_entry_records(
    entries: tuple[SessionEntry, ...],
    *,
    max_text_chars: int,
    include_thinking: bool,
) -> list[JsonValue]:
    """Normalize session entries into bounded evidence records."""
    return [
        _entry_as_json(entry, max_text_chars=max_text_chars, include_thinking=include_thinking)
        for entry in entries
    ]


def build_path(session: PiSession, target_id: str) -> tuple[SessionEntry, ...]:
    """Return entries from the root to a selected branch leaf or entry."""
    if target_id not in {entry.entry_id for entry in session.entries}:
        raise ExportFormatError(f"Unknown session entry id: {target_id}")
    branch_session = PiSession(
        header=session.header,
        entries=session.entries,
        leaf_id=target_id,
        raw=session.raw,
    )
    return build_active_path(branch_session)


def _build_metrics(entries: tuple[SessionEntry, ...]) -> JsonObject:
    counts: dict[str, int] = {
        "userMessages": 0,
        "assistantMessages": 0,
        "toolResults": 0,
        "toolCalls": 0,
        "toolErrors": 0,
        "compactions": 0,
        "branchSummaries": 0,
        "customMessages": 0,
        "abortedResponses": 0,
        "errorResponses": 0,
    }
    tokens: dict[str, int | float] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    costs: dict[str, int | float] = {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
    models: set[str] = set()

    for entry in entries:
        if entry.entry_type == "compaction":
            counts["compactions"] += 1
        elif entry.entry_type == "branch_summary":
            counts["branchSummaries"] += 1
        elif entry.entry_type == "custom_message":
            counts["customMessages"] += 1

        message = _message_object(entry)
        if message is None:
            continue
        role = message.get("role")
        if role == "user":
            counts["userMessages"] += 1
        elif role == "toolResult":
            counts["toolResults"] += 1
            if message.get("isError") is True:
                counts["toolErrors"] += 1
        elif role == "assistant":
            counts["assistantMessages"] += 1
            stop_reason = message.get("stopReason")
            if stop_reason == "aborted":
                counts["abortedResponses"] += 1
            elif stop_reason == "error":
                counts["errorResponses"] += 1

            provider = message.get("provider")
            model = message.get("model")
            if isinstance(model, str):
                models.add(f"{provider}/{model}" if isinstance(provider, str) else model)

            content = message.get("content")
            if isinstance(content, list):
                counts["toolCalls"] += sum(
                    1
                    for block in content
                    if isinstance(block, dict) and block.get("type") == "toolCall"
                )

            usage = message.get("usage")
            if isinstance(usage, dict):
                _accumulate_numeric_fields(tokens, usage)
                cost = usage.get("cost")
                if isinstance(cost, dict):
                    _accumulate_numeric_fields(costs, cost)

    total_tokens = sum(tokens.values())
    total_cost = sum(costs.values())
    return {
        **counts,
        "tokens": {**tokens, "total": total_tokens},
        "cost": {**costs, "total": total_cost},
        "models": sorted(models),
    }


def _accumulate_numeric_fields(target: dict[str, int | float], source: JsonObject) -> None:
    for key in target:
        value = source.get(key)
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            target[key] += value


def _entry_as_json(
    entry: SessionEntry,
    *,
    max_text_chars: int,
    include_thinking: bool,
) -> JsonObject:
    record: JsonObject = {
        "id": entry.entry_id,
        "parentId": entry.parent_id,
        "type": entry.entry_type,
        "timestamp": entry.timestamp,
    }
    message = _message_object(entry)
    if message is not None:
        role = message.get("role")
        record["role"] = role if isinstance(role, str) else "unknown"
        record["text"] = _bound_text(_extract_text(message.get("content")), max_text_chars)
        if role == "assistant":
            record["model"] = message.get("model")
            record["provider"] = message.get("provider")
            record["stopReason"] = message.get("stopReason")
            thinking = _extract_block_text(message.get("content"), "thinking", "thinking")
            record["thinkingChars"] = len(thinking)
            if include_thinking:
                record["thinking"] = _bound_text(thinking, max_text_chars)
        elif role == "toolResult":
            record["toolCallId"] = message.get("toolCallId")
            record["toolName"] = message.get("toolName")
            record["isError"] = message.get("isError")
        elif role == "bashExecution":
            record["command"] = _bound_json(message.get("command"), max_text_chars)
            record["output"] = _bound_json(message.get("output"), max_text_chars)
            record["exitCode"] = message.get("exitCode")
        return record

    if entry.entry_type in {"compaction", "branch_summary"}:
        record["summary"] = _bound_json(entry.raw.get("summary"), max_text_chars)
    elif entry.entry_type == "custom_message":
        record["customType"] = entry.raw.get("customType")
        record["text"] = _bound_text(_extract_text(entry.raw.get("content")), max_text_chars)
        record["display"] = entry.raw.get("display")
    elif entry.entry_type == "model_change":
        record["provider"] = entry.raw.get("provider")
        record["modelId"] = entry.raw.get("modelId")
    elif entry.entry_type == "thinking_level_change":
        record["thinkingLevel"] = entry.raw.get("thinkingLevel")
    elif entry.entry_type == "label":
        record["targetId"] = entry.raw.get("targetId")
        record["label"] = entry.raw.get("label")
    else:
        record["data"] = _bound_json(entry.raw, max_text_chars)
    return record


def _message_object(entry: SessionEntry | None) -> JsonObject | None:
    if entry is None or entry.entry_type != "message":
        return None
    value = entry.raw.get("message")
    return value if isinstance(value, dict) else None


def _extract_text(value: JsonValue) -> str:
    if isinstance(value, str):
        return value
    if not isinstance(value, list):
        return ""
    parts: list[str] = []
    for block in value:
        if isinstance(block, dict) and block.get("type") == "text":
            text = block.get("text")
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def _extract_block_text(value: JsonValue, block_type: str, field: str) -> str:
    if not isinstance(value, list):
        return ""
    parts: list[str] = []
    for block in value:
        if isinstance(block, dict) and block.get("type") == block_type:
            text = block.get(field)
            if isinstance(text, str):
                parts.append(text)
    return "\n".join(parts)


def _bound_text(value: str, max_chars: int | None) -> str:
    if max_chars is None or len(value) <= max_chars:
        return value
    omitted = len(value) - max_chars
    return f"{value[:max_chars]}\n[truncated {omitted} chars]"


def _bound_json(value: JsonValue, max_chars: int | None) -> JsonValue:
    if isinstance(value, str):
        return _bound_text(value, max_chars)
    if isinstance(value, list):
        return [_bound_json(item, max_chars) for item in value]
    if isinstance(value, dict):
        return {key: _bound_json(item, max_chars) for key, item in value.items()}
    return value


def _require_object(value: JsonValue, label: str) -> JsonObject:
    if not isinstance(value, dict):
        raise ExportFormatError(f"Expected {label} to be an object")
    return value


def _require_array(value: JsonValue, label: str) -> list[JsonValue]:
    if not isinstance(value, list):
        raise ExportFormatError(f"Expected {label} to be an array")
    return value


def _require_string(value: JsonValue, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise ExportFormatError(f"Expected {label} to be a non-empty string")
    return value


def _optional_string(value: JsonValue, label: str) -> str | None:
    if value is None or isinstance(value, str):
        return value
    raise ExportFormatError(f"Expected {label} to be a string or null")


def _optional_int(value: JsonValue, label: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    raise ExportFormatError(f"Expected {label} to be an integer or null")


def _optional_bool_from_object(value: JsonObject | None, key: str) -> bool | None:
    if value is None:
        return None
    candidate = value.get(key)
    return candidate if isinstance(candidate, bool) else None


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract structured data from a Pi HTML session export.",
    )
    parser.add_argument("export", type=Path, help="Pi HTML export to inspect")
    parser.add_argument(
        "mode",
        nargs="?",
        default="summary",
        choices=("summary", "active-path", "branches", "tools", "raw"),
        help="data view to emit (default: summary)",
    )
    parser.add_argument(
        "--leaf-id",
        help="inspect the path ending at this entry instead of the active leaf",
    )
    parser.add_argument(
        "--max-text-chars",
        type=int,
        default=4000,
        help="maximum characters retained in each text field (default: 4000)",
    )
    parser.add_argument(
        "--include-thinking",
        action="store_true",
        help="include thinking text in active-path output; omitted by default",
    )
    return parser


def _render_mode(
    session: PiSession,
    source_path: Path,
    mode: str,
    *,
    leaf_id: str | None,
    max_text_chars: int,
    include_thinking: bool,
) -> JsonValue:
    if max_text_chars < 1:
        raise ExportFormatError("--max-text-chars must be at least 1")
    if mode == "summary":
        return build_summary(session, source_path)
    selected_path = build_path(session, leaf_id) if leaf_id is not None else build_active_path(session)
    if mode == "active-path":
        return build_entry_records(
            selected_path,
            max_text_chars=max_text_chars,
            include_thinking=include_thinking,
        )
    if mode == "branches":
        return build_summary(session, source_path)["branches"]
    if mode == "tools":
        records = build_tool_records(session, entries=selected_path) if leaf_id is not None else build_tool_records(session)
        return [record.as_json(max_text_chars=max_text_chars) for record in records]
    if mode == "raw":
        return session.raw
    raise ExportFormatError(f"Unsupported output mode: {mode}")


if __name__ == "__main__":
    argument_parser = _build_parser()
    arguments = argument_parser.parse_args()
    try:
        loaded_session = read_pi_export(arguments.export)
        output = _render_mode(
            loaded_session,
            arguments.export,
            arguments.mode,
            leaf_id=arguments.leaf_id,
            max_text_chars=arguments.max_text_chars,
            include_thinking=arguments.include_thinking,
        )
    except ExportFormatError as error:
        argument_parser.exit(2, f"error: {error}\n")
    print(json.dumps(output, indent=2, ensure_ascii=False))
