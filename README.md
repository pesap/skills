# pesap skills

Personal and domain-specific skills for coding agents. Each skill is a
standalone directory with its own `SKILL.md` and optional references, scripts,
and evaluations.

## Quick start

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

## Skills

- `bash-script` — Bash scripting practices
- `cli-ux` — opinionated CLI and agent-interaction design
- `code-quality-gate` — project-guideline and change-quality checks
- `data-model` — data-modeling practices
- `docs-pesap` — README, API, Diataxis, and GitHub documentation
- `infrasys`, `r2x-core`, `sdom`, `sienna-platform`, `torc-hpc`,
  `arco-optimization` — domain-specific project skills
- `python-pesap` — opinionated Python development
- `rust-pesap` — opinionated Rust development
- `tdd-pesap` — opinionated test-driven development

Use each skill's `SKILL.md` as its entry point. Load references and scripts only
when the task requires their detail.
