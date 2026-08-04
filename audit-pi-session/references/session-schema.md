# Pi HTML Export and Extractor Schema

## HTML envelope

Current Pi HTML exports embed structured data as base64-encoded UTF-8 JSON:

```html
<script id="session-data" type="application/json">BASE64</script>
```

The decoded root contains:

- `header`: session ID, format version, timestamp, cwd, and optional parent session.
- `entries`: every entry in the session tree, including abandoned branches.
- `leafId`: active entry at export time.
- `systemPrompt` and `tools`: present when exported from an active TUI session; potentially absent when exported from a JSONL file.
- `renderedTools`: optional presentation HTML for custom tools. Do not use it as the primary audit source.

Pi currently emits session version 3, but the extractor preserves unknown entry types and does not require one exact version.

## Tree semantics

Every entry has an `id` and a nullable `parentId`. Follow `parentId` from a selected leaf to reconstruct a branch, then reverse the result. The active branch ends at `leafId`. Older exports without `leafId` follow Pi's HTML behavior and use the final entry.

A tree can contain multiple leaves. Global metrics count all branches; active-path metrics count only entries leading to the active leaf. These values answer different questions and must not be conflated.

## Important entry types

- `message`: wraps a user, assistant, tool-result, or Bash-execution message.
- `model_change`: records a provider/model switch.
- `thinking_level_change`: records a reasoning-level switch.
- `compaction`: records summarized context and token count before compaction.
- `branch_summary`: preserves context from an abandoned branch.
- `custom_message`: extension-injected context that participates in the conversation.
- `custom`: extension state that does not participate in model context.
- `label`: attaches a human label to another entry.
- `session_info`: records session metadata such as its display name.

Assistant content blocks can contain `text`, `thinking`, and `toolCall`. Tool results are separate messages linked by `toolCallId`.

## Extractor modes

- `summary`: session identity, source size, active leaf, global and active metrics, and branch leaves.
- `active-path`: bounded normalized evidence records from root to active or selected leaf.
- `branches`: branch leaf metadata without message bodies.
- `tools`: assistant tool calls correlated with results. With `--leaf-id`, restrict results to that selected path.
- `raw`: complete decoded root payload; use sparingly because it can be large and sensitive.

Each bounded text field defaults to 4,000 characters. Truncation is explicit. `--max-text-chars N` changes that limit.

## Metric cautions

- Token and cost totals come from persisted assistant usage records. Missing provider usage remains missing rather than estimated.
- Tool errors use `toolResult.isError`; a successful tool result does not establish semantic correctness.
- Pending tool calls have no correlated result.
- Entry timestamps support ordering. Do not infer precise model or tool latency without stronger timing data.
- Compactions and branch summaries can add cost while not appearing as ordinary assistant messages.
