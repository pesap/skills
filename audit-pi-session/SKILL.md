---
name: audit-pi-session
description: Decode and audit Pi coding-agent HTML session exports with branch-aware metrics, tool-call correlation, and entry-level evidence. Use when a user provides or references a Pi `/export` HTML file and asks to analyze, review, summarize, debug, compare branches, evaluate agent behavior, investigate tool failures or inefficiency, verify completion claims, or improve prompts, skills, and coding workflows from the recorded session.
---

# Audit Pi Session

Analyze the structured session embedded in a Pi HTML export. Prefer decoded session data over scraping rendered HTML.

## Workflow

1. Confirm the target `.html` file. Treat it as sensitive: exports can contain source code, prompts, local paths, images, credentials, and tool output.
2. Resolve this skill's directory and run the bundled extractor locally:

```bash
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> summary
```

3. Read [references/session-schema.md](references/session-schema.md) when interpreting Pi entry types, branches, or extractor output.
4. Choose the smallest useful evidence view:

```bash
# Entries on the active branch; thinking text is omitted by default
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> active-path

# Branch leaves and their sizes
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> branches

# Tool calls correlated with results across the full tree
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> tools

# Inspect one abandoned or selected branch
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> active-path --leaf-id <entry-id>
uv run <skill-dir>/scripts/extract_pi_session.py <export.html> tools --leaf-id <entry-id>
```

5. Increase `--max-text-chars` only when truncated evidence matters. Use `raw` only for fields unavailable in the bounded views; it emits the complete decoded payload.
6. Read [references/audit-rubric.md](references/audit-rubric.md), apply only dimensions relevant to the user's question, and cite entry IDs, tool-call IDs, timestamps, or exact bounded excerpts.
7. Separate direct observation, reasoned inference, and facts requiring repository inspection.

## Scope Rules

- Use active-path metrics for the work Pi would continue from. Do not describe global tree totals as active-branch behavior.
- Inspect abandoned branches only when they explain retries, alternatives, useful discoveries, or wasted effort.
- Correlate assistant tool calls with `toolResult` entries before judging success. A call without a result is pending or interrupted, not successful.
- Treat command output and exit status as evidence of execution, not proof that the resulting code is correct.
- Treat final assistant claims as claims until supported by tool output or repository evidence.
- Do not grade or reproduce private reasoning. Evaluate observable prompts, responses, tool use, branch choices, and validation. The extractor reports thinking size but omits thinking text unless `--include-thinking` is explicitly requested.
- Preserve unknown entry types as evidence rather than assuming they are irrelevant.

## Reporting

Default to a concise report:

```markdown
# Pi Session Audit

## Executive summary
## Requested and claimed outcome
## Material findings
- Severity: high | medium | low
  Evidence: entry/tool ID and timestamp
  Observation: directly recorded behavior
  Impact: why it matters
  Improvement: concrete alternative
## Validation evidence and gaps
## Better workflow
## Metrics
```

Report only material findings. Avoid generic praise, checklist dumping, unsupported intent attribution, and precise duration claims unless timestamps establish them.

## Privacy

Keep extraction local. Do not upload or web-search export contents unless the user explicitly requests it. Never repeat suspected secrets in the report; identify their location by entry ID and recommend rotation or redaction instead.
