---
name: external-review
description:
  Run an independent, context-rich second opinion by launching a fresh Pi,
  Codex, or Claude process with a configured frontier-level model and a bounded
  review packet. Use when the user asks for an external review, independent review,
  second opinion, fresh eyes, high-thinking review, or a separate reviewer pass
  before committing, opening, updating, or merging a change.
---

# External Review

Use a separate Pi, Codex, or Claude process as an independent, frontier-level
reviewer. Ask for a clear opinion grounded in the change's intent, surrounding
context, trade-offs, and evidence—not a generic checklist. The external
reviewer is advisory:
verify its claims locally before changing code or reporting them as facts.

## Use when

- The user wants a separate, high-capability opinion on a change or design.
- The change has meaningful architectural, API, security, correctness, or
  scope trade-offs.
- A fresh context is valuable because the primary agent may be anchored to its
  implementation.

## Avoid when

- The user only needs ordinary local validation or formatting checks.
- The review target cannot be bounded without exposing unrelated or sensitive
  context.
- The request is for a final merge decision without local verification.

## Workflow

1. Scope the review target: current diff, staged diff, branch, PR, issue, file,
   or user-provided artifact. If the target is ambiguous, choose the smallest
   obvious current change and state that assumption.
2. Build a bounded review packet for the external reviewer. Prefer:
   - User request and intended behavior.
   - Changed-file list and diffstat.
   - Focused diff or relevant excerpts, not the whole repository.
   - Validation already run and known failures.
   - Specific concerns the user asked about.
3. Launch a fresh process with a configured frontier-level model. Use the
user's requested runner and model when provided; otherwise choose a configured
runner and require `EXTERNAL_REVIEW_MODEL`. Do not silently downgrade to a
weaker or stale model.

```bash
: "${EXTERNAL_REVIEW_MODEL:?Set EXTERNAL_REVIEW_MODEL to the requested frontier model}"

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
    printf 'Unsupported external reviewer: %s\\n' "$EXTERNAL_REVIEW_AGENT" >&2
    exit 2
    ;;
esac
```

Keep tools disabled, or read-only where the runner requires tools, unless the
user explicitly requests otherwise. Read-only packet review is the default.

4. Ask the external reviewer for structured output:
   - A concise overall opinion on whether the change achieves its intent.
   - Material findings only, ordered by severity.
   - File/line or excerpt-backed evidence and confidence.
   - Why each issue matters and the relevant trade-off.
   - Suggested fix direction or a justified alternative.
   - Validation gaps and open questions.
   - Final verdict: pass, revise, or blocked.
5. Synthesize the result. Inspect the local code before accepting any finding.
   Classify each external finding as must-fix, optional/deferred, false
   positive, or needs human decision. Explain rejected findings briefly.
6. If implementing fixes, keep them scoped to confirmed must-fix findings and
   rerun focused validation afterward.

## Prompt Template

Use this shape for `$REVIEW_PROMPT`:

```text
You are an external reviewer running in a fresh context.

Review target:
<scope and intent>

Review posture:
- Read-only. Do not ask to mutate files or run tools.
- Give a clear, independent opinion about the intent, design, trade-offs, and
  likely failure modes.
- Report only material correctness, security, maintainability, API, test, or
  scope risks that should change the work before it is considered done.
- Do not give generic checklist advice or empty praise.

Context:
<user request, intended behavior, constraints, architecture, alternatives, and validation already run>

Changed files and diffstat:
<bounded file list and stats>

Diff or excerpts:
<focused patch/excerpts>

Output format:
Opinion:
<clear overall assessment, including important trade-offs>

Findings:
- Severity: blocker|major|minor
  Confidence: high|medium|low
  Evidence: <file/line or quoted excerpt>
  Issue: <problem>
  Why it matters: <impact and trade-off>
  Suggested fix: <direction or alternative>

Validation gaps:
- <gap or "none">

Open questions:
- <question or "none">

Verdict: pass|revise|blocked
```

## Guardrails

- Do not use external review as a substitute for local understanding.
- Do not paste the external review verbatim as the final answer unless the user
  explicitly asks for raw output.
- Do not send secrets, private tokens, credentials, or unrelated proprietary
  context in the review packet.
- If the packet is too large for one prompt, split by subsystem or risk area and
  run multiple focused external reviews.
