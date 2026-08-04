# Pi Session Audit Rubric

Apply only dimensions relevant to the user's question. Rank material findings by impact, not by how easy they are to count.

## Evidence standard

For each finding:

1. Cite an entry ID, tool-call ID, timestamp, or bounded excerpt.
2. State what was directly observed.
3. Mark causal explanations as inference unless the session establishes them.
4. State what repository or runtime evidence would be needed to verify unresolved claims.

Use these labels when ambiguity matters:

- **Observed:** directly represented in the export.
- **Inferred:** plausible interpretation supported by multiple observations.
- **Unverified:** cannot be established from the export alone.

## Outcome and correctness

Check whether the final response answers the latest user request and whether its completion claims are supported by recorded validation. Look for ignored failures, incomplete acceptance criteria, tests that did not exercise the changed behavior, and claims made after aborted or missing tool results.

Do not infer that code was correct merely because editing succeeded or a command exited zero.

## Workflow quality

Check whether the agent:

- discovered repository guidance and relevant code before editing;
- clarified risky ambiguity instead of silently choosing semantics;
- used a small, coherent implementation path;
- reacted appropriately to user steering and tool failures;
- validated public behavior rather than only implementation details;
- inspected the final diff or affected files before claiming completion.

Judge the recorded task, not an idealized checklist. Omitted steps are findings only when they created meaningful risk or waste.

## Tool use and efficiency

Look for:

- repeated reads or searches with no new information;
- repeated failed commands without changed hypotheses;
- broad output when a focused query was available;
- edit churn or reversals;
- tool calls lacking results;
- unnecessary branch detours or compactions;
- expensive model use that did not advance the task.

Distinguish necessary iteration from waste. Count repetition only as supporting evidence; explain its impact.

## Branch analysis

Compare the active branch with abandoned leaves when relevant:

- identify the divergence entry;
- summarize what each branch attempted;
- note useful discoveries preserved or discarded;
- explain why one path appears more effective using observable evidence;
- avoid charging abandoned work to the active path when reporting active metrics.

## Collaboration quality

Assess whether user-facing responses were timely, clear, calibrated, and responsive to corrections. Flag excessive narration only when it obscured progress or consumed interaction unnecessarily. Flag missing questions only when ambiguity materially affected the result.

## Prompt and skill evaluation

When evaluating a prompt or skill, separate agent execution failures from instruction defects. Ask:

- Was the relevant instruction actually loaded before the behavior?
- Was it specific enough to determine an action?
- Did repository guidance conflict with it?
- Did the agent follow it but still fail because the instruction was incomplete?
- Does the evidence recur across branches or sessions?

Recommend changing a skill only when the session supports a reusable improvement, not merely a one-off correction.

## Severity

- **High:** likely incorrect outcome, security/privacy exposure, destructive behavior, or unsupported completion of a core requirement.
- **Medium:** meaningful validation gap, avoidable rework, misleading communication, or workflow defect likely to recur.
- **Low:** localized inefficiency or clarity issue with limited effect on the outcome.

Do not inflate severity based solely on token count or session length.
