# pesap skills

Personal and domain-specific skills for coding agents. Each skill is a
standalone directory with its own `SKILL.md` and optional references, scripts,
and evaluations.

## Quick start

Clone the collection and inspect the available skills:

```bash
git clone git@github.com:pesap/skills.git
cd skills
find . -maxdepth 1 -mindepth 1 -type d | sort
```

Copy the skill directories you want into the skills directory used by your
agent.

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
