# Codex Commands

Shared Codex CLI prompt equivalents live in `.codex/prompts/`. The old Claude Code slash commands remain in `.claude/commands/` for compatibility, but new command workflow documentation should point to Codex first.

## Available Prompts

| Prompt | Purpose |
|--------|---------|
| `fixlinks` | Run link checking and research high-confidence replacements for broken YAML entry URLs. |
| `rotatechangelog` | Archive `docs/CHANGELOG.md` into `docs/previous_changelogs/` and reset the changelog from `docs/changelog_template.md`. |

## Running With Codex CLI

Use `codex exec` with the prompt file as stdin for the most reliable project-local workflow:

```bash
codex exec --search -C . - < .codex/prompts/fixlinks.md
codex exec -C . - < .codex/prompts/rotatechangelog.md
```

`fixlinks` benefits from `--search` because replacement URL research usually needs live web context. `rotatechangelog` does not need web access.

For interactive Codex sessions, open `codex` from the repository root and use the same prompt files as the canonical instructions. If your installed Codex build only discovers global custom prompts, link the project prompts into `${CODEX_HOME:-$HOME/.codex}/prompts/`.

## Maintenance

- Keep `.codex/prompts/*.md` as the canonical command definitions.
- Keep `.claude/commands/*.md` only when Claude Code compatibility is useful.
- Update this file when adding, renaming, or removing shared agent commands.
