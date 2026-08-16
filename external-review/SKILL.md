---
name: external-review
description:
  Run an independent, context-rich second opinion in a fresh Pi, Codex, or
  Claude process with a configured frontier model. Use when the user asks for
  external review, a second opinion, fresh eyes, or a separate reviewer pass on
  a bounded change or design before commit, PR, or merge. Do not use as a
  substitute for local validation or as an unverified merge decision.
---

# External review

Use a fresh process to challenge the primary agent's implementation or design.
The result is advisory: verify every finding locally before changing code or
reporting it as fact.

## Core workflow

1. Bound the target to the smallest useful diff, branch, PR, issue, file, or
   artifact. State any scope assumption.
2. Build a review packet with the request and intent, constraints, changed-file
   list and diffstat, focused diff or excerpts, validation already run, known
   failures, and the user's specific concerns. Exclude unrelated context and
   secrets.
3. Use the requested runner and model when provided. Otherwise require
   `EXTERNAL_REVIEW_MODEL` and use `EXTERNAL_REVIEW_AGENT` (default: `pi`). Do
   not silently downgrade the model.
4. Request a concise opinion; material, evidence-backed findings ordered by
   severity; trade-offs and fix direction; validation gaps; open questions; and
   a `pass`, `revise`, or `blocked` verdict.
5. Verify each finding against local code and classify it as must-fix,
   optional/deferred, false positive, or human decision. Explain rejected
   findings briefly.
6. If fixes are requested, implement only confirmed findings and rerun focused
   validation.

## Launch command

```bash
: "${EXTERNAL_REVIEW_MODEL:?Set EXTERNAL_REVIEW_MODEL to a frontier model}"

case "${EXTERNAL_REVIEW_AGENT:-pi}" in
  pi)
    pi --no-session --no-tools --model "$EXTERNAL_REVIEW_MODEL" --thinking high -p "$REVIEW_PROMPT"
    ;;
  codex)
    codex exec --sandbox read-only --ask-for-approval never --model "$EXTERNAL_REVIEW_MODEL" "$REVIEW_PROMPT"
    ;;
  claude)
    claude -p "$REVIEW_PROMPT" --model "$EXTERNAL_REVIEW_MODEL" --permission-mode plan
    ;;
  *)
    printf 'Unsupported external reviewer: %s\n' "$EXTERNAL_REVIEW_AGENT" >&2
    exit 2
    ;;
esac
```

Keep tools disabled or read-only unless the user explicitly requests broader
access.

## Review packet

Use this compact shape for `$REVIEW_PROMPT`:

```text
You are an independent reviewer in a fresh, read-only context.

Target and intent:
<bounded scope, requested behavior, constraints, trade-offs>

Evidence:
<changed files, diffstat, focused diff/excerpts, validation and known failures>

Focus:
<user concerns or "material correctness, security, API, test, and scope risks">

Return:
- Opinion: whether the change achieves its intent
- Findings: blocker|major|minor, confidence, exact evidence, impact, fix direction
- Validation gaps and open questions
- Verdict: pass|revise|blocked
Report only material findings; no generic checklist or empty praise.
```

Split oversized packets by subsystem or risk rather than sending an entire
repository.

## Guardrails

Do not expose credentials or unrelated proprietary context, accept findings
without local verification, paste raw reviewer output as the final answer unless
asked, or treat the reviewer as the final merge authority.
