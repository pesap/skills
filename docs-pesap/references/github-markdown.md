# GitHub Markdown

Use GitHub-flavored elements to improve scanning, navigation, and comprehension,
not as decoration. The source should remain understandable when advanced
rendering is unavailable.

## Contents

- [Element chooser](#element-chooser)
- [Structure and navigation](#structure-and-navigation)
- [Alerts](#alerts)
- [Collapsed sections](#collapsed-sections)
- [Tables and task lists](#tables-and-task-lists)
- [Code and command examples](#code-and-command-examples)
- [Diagrams, images, and badges](#diagrams-images-and-badges)
- [Validation checklist](#validation-checklist)
- [Official references](#official-references)

## Element chooser

| Reader need | Prefer | Avoid |
|---|---|---|
| Find a section | Descriptive headings and GitHub's page outline | Manual contents list on a short page |
| Compare compact facts | A small table | Paragraphs forced into wide cells |
| Notice critical context | One concise alert | Consecutive or decorative alerts |
| Defer optional detail | `<details>` with a descriptive summary | Hiding required steps |
| Track short-lived work | Markdown task list | Using README checkboxes as a durable issue tracker |
| Explain a simple flow | Mermaid plus a text summary | A diagram that is unreadable in source |
| Show project status | A few linked badges | A wall of badges or unlabeled images |

## Structure and navigation

- Use one descriptive H1 followed by a logical heading hierarchy; do not skip
  levels.
- Write headings that identify reader goals. Renaming a heading changes its
  generated anchor, so verify inbound links after edits.
- Let GitHub's page outline handle navigation for short documents. Add a manual
  contents section only when a long reference benefits from visible routing.
- Prefer relative links for repository files and directories. Use descriptive
  link text instead of `here`, raw URLs, or repeated filenames without context.
- Keep paragraphs short and place the primary action before background detail.

## Alerts

Use alerts only for information that should interrupt the normal reading flow.
Keep them short and generally limit a page to one or two.

```markdown
> [!NOTE]
> Background the reader needs before continuing.

> [!TIP]
> An optional improvement or shortcut.

> [!IMPORTANT]
> Information required for success.

> [!WARNING]
> A risk that can cause failure or data loss.

> [!CAUTION]
> A severe or irreversible consequence.
```

Do not place alerts consecutively. Promote long, list-heavy, or procedural
content to a normal section instead.

## Collapsed sections

Use `<details>` for optional diagnostics, alternate implementations, or verbose
output. Required setup, commands, and validation must remain visible.

```html
<details>
<summary><strong>Show troubleshooting details</strong></summary>

Optional Markdown content goes here.

</details>
```

Use a specific summary that tells the reader what opening the section reveals.
Keep blank lines around Markdown inside the HTML block so GitHub renders it
correctly.

## Tables and task lists

- Use tables for short, comparable values. Keep cells concise and move
  procedures or multi-paragraph explanations into normal sections.
- Put a blank line before a table and include a clear header row.
- Use task lists for small, active checklists in issues or pull requests. Use
  sub-issues or a project for durable work tracking; legacy tasklist blocks are
  retired.
- Do not use disabled-looking task lists as ordinary bullets in reference docs.

## Code and command examples

- Label every fenced block with its language.
- Keep shell examples copy-pasteable. If expected output shares a shell block,
  prefix it with `#` so pasting the block cannot execute it.
- Separate commands from long output, and truncate logs to the lines needed for
  diagnosis.
- State placeholders consistently and never put secrets or realistic tokens in
  examples.

## Diagrams, images, and badges

- Use Mermaid for a small flow, sequence, state, or relationship diagram only
  when it communicates faster than prose. Add a nearby text summary and verify
  that labels remain useful in source.
- Give every meaningful image concise alt text. Do not encode essential
  instructions only in screenshots.
- Check diagrams, images, and badges in both light and dark themes.
- Link badges to the status or service they summarize. Keep only badges that
  help readers make a decision.
- Avoid centered hero HTML, decorative emoji, animation, and layout tricks that
  reduce source readability or accessibility.

## Validation checklist

- [ ] Heading levels and generated anchors are correct.
- [ ] Relative links resolve from the document's location.
- [ ] Tables remain readable on a narrow viewport.
- [ ] Alerts and collapsed sections render as intended.
- [ ] Commands are safe to copy and code fences have languages.
- [ ] Images have useful alt text and work in light and dark themes.
- [ ] The source remains understandable without GitHub-specific rendering.

## Official references

- [Basic writing and formatting syntax](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax)
- [Organizing information with tables](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-tables)
- [Organizing information with collapsed sections](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/organizing-information-with-collapsed-sections)
- [Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)
- [About task lists](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/about-task-lists)
- [About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
