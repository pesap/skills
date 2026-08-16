---
name: good-api
description:
  "Evaluate or design developer-facing APIs, SDKs, CLIs, libraries, schemas,
  and interfaces with the learning ladder: flexible first, gradual second,
  convenient third. Use for ergonomics, composability, onboarding, layered
  APIs, beginner defaults, expert escape hatches, or enterprise integration.
  Do not use for implementation-only debugging with no interface question."
license: MIT
---

# API design

Assess how users grow from first success to advanced composition without
learning contradictory semantics or ejecting from the API.

## Core method

1. Name the target users: beginner, novice, expert, and
   enterprise/integration-heavy if relevant.
2. Assess the API as a learning ladder:
   - **Flexible**: experts can solve many real problems without hidden
     restrictions or forced eject paths.
   - **Gradual**: novices can learn one stable layer at a time; adding power
     does not contradict earlier semantics.
   - **Convenient**: beginners can solve the common case quickly with defaults,
     examples, or safe packaging.
3. Design or recommend changes in this order: flexible primitives first, gradual
   layers second, convenient wrappers/defaults third.
4. Check for hidden dependencies, restrictive coupling, oversimplified data
   models, and semantic surprises between layers.
5. Treat convenience wrappers as packaging over understandable primitives, not
   substitutes for a flexible model.

## Reference router

- Read [the ladder model](references/ladder-model.md) when the full vocabulary,
  failure modes, or source-derived review questions are needed.
- Use `evals/trigger-prompts.json` only when tuning recognition and
  `evals/evals.json` only when grading non-trivial API reviews.

## Output

- Ladder assessment: flexible / gradual / convenient.
- Top API risks, ranked by user impact.
- Concrete redesign recommendations.
- Tradeoffs and cases where convenience should win.
