# GitLab command behavior

`glab <command> --help` is authoritative for flags. Pass `--repo
GROUP/PROJECT` when outside the target repository.

## Authentication and context

```bash
glab auth status
glab auth login
```

Set `GITLAB_HOST` for self-managed instances and `GITLAB_TOKEN` for
non-interactive authentication. Never print token values.

## Merge requests

```bash
glab mr list
glab mr view <id>
glab mr diff <id>
glab mr checkout <id>
glab mr create --fill --yes
glab mr approve <id>
glab mr merge <id>
```

Before creating an MR, inspect existing MRs for the current source branch.
Prefer explicit title, description, target branch, reviewers, and labels when
the request or repository conventions define them. Verify the resulting remote
MR instead of treating command success as proof that all metadata is correct.

`glab mr merge` changes remote state. Confirm the MR, target branch, approvals,
checks, and requested merge method first.

## Issues

```bash
glab issue list
glab issue view <id>
glab issue create --title "<title>" --description "<body>"
glab issue close <id>
```

Inspect labels, milestones, assignees, and issue templates before creating or
updating an issue. Verify close relationships from durable issue or MR context;
do not infer them from topic similarity alone.

## Releases

```bash
glab release list
glab release create <tag>
glab changelog generate
```

Release creation publishes remote state immediately. Verify the tag, ref,
assets, notes, and project before running it.

## Repository operations

```bash
glab repo clone <group/project>
glab repo view
glab api <endpoint>
```

Use `glab api` only when a standard subcommand does not expose the required
state. Request bounded fields or filter output rather than loading large
payloads.
