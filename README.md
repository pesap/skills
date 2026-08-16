# pesap skills

Personal and domain-specific skills for coding agents. Each skill is a
standalone directory with `SKILL.md` as its entry point and optional references,
scripts, assets, and evaluations.

## Install

Use Vercel's [Skills CLI](https://github.com/vercel-labs/skills) to inspect and
install skills:

```bash
npx skills add pesap/skills --list
npx skills add pesap/skills --skill cli-ux --global
```

Install additional skills by repeating `--skill`, or install the complete
collection with:

```bash
npx skills add pesap/skills --all
```

## Skill catalog

### Agent and forge workflows

- `audit-pi-session` — audit Pi HTML session exports with branch-aware evidence
- `code-quality-gate` — check changes against project guidance and quality gates
- `external-review` — run a bounded review in a fresh agent process
- `github` — operate PRs, issues, runs, and GitHub Actions with `gh`
- `gitlab` — operate MRs, issues, pipelines, and GitLab CI with `glab`

### Engineering practices

- `bash-script` — write and harden reliable Bash automation
- `cli-ux` — design accessible, composable command-line interfaces
- `data-model` — design typed dataclass, Pydantic, and infrasys contracts
- `docs-pesap` — write source-grounded technical documentation
- `good-api` — review APIs with the flexible/gradual/convenient learning ladder
- `prek` — run and optimize pre-commit-compatible hooks with `prek`
- `python-pesap` — apply the repository's Python engineering standard
- `rust-pesap` — apply the repository's Rust engineering standard
- `tdd-pesap` — work test-first in small behavior-focused slices
- `uv` — run reproducible standalone Python scripts with uv

### Domain workflows

- `arco-optimization` — debug and optimize Arco models
- `infrasys` — work with typed infrasys systems and persistence
- `r2x-core` — build r2x translators, plugins, rules, and data stores
- `sdom` — run and extend the Storage Deployment Optimization Model
- `sienna-platform` — route work across the Sienna Julia ecosystem
- `torc-hpc` — design and operate local, remote, and Slurm Torc workflows

## Agent navigation model

1. The `name` and `description` in `SKILL.md` select the skill. Descriptions
   include concrete user language and the nearest important exclusion.
2. The `SKILL.md` body contains the mental model, critical constraints, and core
   loop needed for most tasks.
3. A task router links directly to optional references. Load only the reference
   whose trigger matches the current task.
4. Scripts encode repeated deterministic work and can run without loading their
   implementation into context.
5. Evaluation files support trigger tuning or output grading; do not load them
   during normal task execution.

Keep entry points concise, avoid repeating trigger lists in the body, remove
obsolete monoliths when references replace them, and prefer direct reference
links over multi-hop indexes.
