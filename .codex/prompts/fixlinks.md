---
description: Research replacements for broken repository links
---

# Fix Broken Links

Run the repository link checker, identify broken links, and research high-confidence replacements.

## Steps

1. Run the link checker from the repository root:

   ```bash
   make check-links
   ```

   If the project virtual environment is not installed, run `make install` first.

2. Work from YAML files as the source of truth. For each broken URL reported from `data/**/*.yml`:
   - Read the YAML entry containing the URL.
   - Capture the entry name, category, description, and relevant metadata.
   - Research a replacement that preserves the entry's original meaning.

3. Prefer replacement URLs in this order:
   - Official project website or documentation.
   - Current official GitHub repository if the repo moved or was renamed.
   - Official organization page for the project.
   - Archive.org snapshot only when the project is defunct and no active official source exists.

4. Use live web search when available. Use parallel research or sub-agents only when the active Codex environment supports them and the user/session has permitted delegation.

5. Report findings before editing unless the user explicitly asked you to apply fixes. For each broken link, include:
   - Original URL.
   - YAML file path.
   - Entry name and short context.
   - Recommended replacement URL, if found.
   - Rationale for the recommendation.
   - Recommendation to update, archive, or remove the entry when no replacement exists.

## Constraints

- Do not edit generated files directly.
- Do not use unofficial mirrors when an official source exists.
- Preserve YAML schema validity if edits are requested.
- After any YAML edits, run `make validate` and `make generate`.
