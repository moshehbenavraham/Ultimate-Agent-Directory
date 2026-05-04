---
description: Archive the current changelog and reset it from the template
---

# Rotate Changelog

Archive the current changelog and reset `docs/CHANGELOG.md` from the template.

## Steps

1. Read `docs/CHANGELOG.md`.
2. Determine today's date from the system, using `YYYY-MM-DD` format.
3. Create `docs/previous_changelogs/` if it does not already exist.
4. Archive the current changelog to `docs/previous_changelogs/YYYY-MM-DD_changelog.md`.
   - Preserve the entire current changelog content exactly.
   - If that archive filename already exists, choose the next unique filename by appending a short suffix before `.md`.
5. Read `docs/changelog_template.md`.
6. Replace `docs/CHANGELOG.md` with the template content.
7. Confirm completion with:
   - Archive file path.
   - `docs/CHANGELOG.md` reset status.
   - Any non-standard filename suffix used.

## Constraints

- Use the actual system date, not an example date.
- Do not delete existing archived changelogs.
- Do not lose content from the current changelog.
- Keep files ASCII UTF-8 with LF line endings.
