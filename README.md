# pesap skills

[![Browse on skills.sh](https://skills.sh/b/pesap/skills)](https://skills.sh/pesap/skills)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A curated collection of reusable, domain-specific
[Agent Skills](https://agentskills.io) for coding agents. Every skill uses a
lean `SKILL.md` entry point with optional references, scripts, assets, and
evaluations loaded only when needed.

> [!TIP]
> Browse the collection on [skills.sh](https://skills.sh/pesap/skills), or run
> `npx skills add pesap/skills --list` from the terminal.

## Quick start

### Skills CLI

```bash
# Install one skill globally
npx skills add pesap/skills --skill cli-ux --global

# Install every skill for every detected agent
npx skills add pesap/skills --all
```

### GitHub CLI

```bash
# Install one skill
gh skill install pesap/skills cli-ux

# Install the complete collection
gh skill install pesap/skills --all
```

## Update

Use the same tool that installed the skills.

| Installed with | Update all | Update one |
|---|---|---|
| GitHub CLI | `gh skill update --all` | `gh skill update cli-ux` |
| Skills CLI | `npx skills update` | `npx skills update cli-ux` |

## Skill catalog

### Agent and forge workflows

| Skill | Best for |
|---|---|
| [`audit-pi-session`](audit-pi-session/) | Auditing Pi HTML session exports with branch-aware evidence |
| [`code-quality-gate`](code-quality-gate/) | Checking changes against project guidance and quality gates |
| [`external-review`](external-review/) | Running a bounded review in a fresh agent process |
| [`github`](github/) | Operating PRs, issues, runs, and GitHub Actions with `gh` |
| [`gitlab`](gitlab/) | Operating MRs, issues, pipelines, and GitLab CI with `glab` |

### Engineering practices

| Skill | Best for |
|---|---|
| [`bash-script`](bash-script/) | Writing and hardening reliable Bash automation |
| [`cli-ux`](cli-ux/) | Designing accessible, composable command-line interfaces |
| [`data-model`](data-model/) | Designing typed dataclass, Pydantic, and infrasys contracts |
| [`docs-pesap`](docs-pesap/) | Writing source-grounded technical documentation |
| [`good-api`](good-api/) | Reviewing APIs with the flexible/gradual/convenient learning ladder |
| [`prek`](prek/) | Running and optimizing pre-commit-compatible hooks with `prek` |
| [`python`](python/) | Function-first Python with explicit Result and domain-context contracts (candidate; evaluation pending) |
| [`rust`](rust/) | Function-first Rust with explicit ownership, Result, and domain contexts (candidate; evaluation pending) |
| [`tdd-pesap`](tdd-pesap/) | Working test-first in small, behavior-focused slices |
| [`uv`](uv/) | Running reproducible standalone Python scripts with uv |

### Domain workflows

| Skill | Best for |
|---|---|
| [`arco-optimization`](arco-optimization/) | Debugging and optimizing Arco models |
| [`infrasys`](infrasys/) | Working with typed infrasys systems and persistence |
| [`r2x-core`](r2x-core/) | Building r2x translators, plugins, rules, and data stores |
| [`sdom`](sdom/) | Running and extending the Storage Deployment Optimization Model |
| [`sienna-platform`](sienna-platform/) | Routing work across the Sienna Julia ecosystem |
| [`torc`](torc/) | Designing and operating local, remote, and Slurm Torc workflows |

<details>
<summary><strong>How agents navigate this repository</strong></summary>

1. The `name` and `description` in `SKILL.md` select the skill.
2. The `SKILL.md` body provides the mental model, critical constraints, and core
   workflow.
3. Task routers link directly to optional references; agents load only the file
   relevant to the current task.
4. Scripts encode repeated deterministic work without requiring their source in
   the context window.
5. Evaluation files support trigger tuning and output grading, not normal task
   execution.

Entry points stay concise, trigger lists live in metadata, and obsolete
monoliths are removed when focused references replace them.

</details>

## License

Distributed under the [MIT License](LICENSE).
