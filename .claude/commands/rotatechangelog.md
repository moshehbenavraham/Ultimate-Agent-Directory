---
description: Archive current changelog and start fresh
---

# Rotate Changelog

Archive the current changelog and reset it with a fresh template.

**Steps:**

1. Read the current `docs/CHANGELOG.md` file
2. Create a uniquely named archive file using today's date: `YYYY-MM-DD_changelog.md`
3. Write the current changelog content to `docs/previous_changelogs/YYYY-MM-DD_changelog.md`
4. Read the template from `docs/changelog_template.md`
5. Replace `docs/CHANGELOG.md` with the fresh template content
6. Confirm completion with a summary:
   - Archived file location
   - New changelog ready for entries

**Important:**
- Use today's date for the archive filename (format: `2025-11-06_changelog.md`)
- Preserve all content from the current changelog in the archive
- Only use the template to reset the main CHANGELOG.md file
- Create `docs/previous_changelogs/` directory if it doesn't exist
