---
description: Find replacement URLs for broken links using research agents
---

# Fix Broken Links

Run the link checker to identify broken links, then for each broken link:

1. Read the YAML file containing the broken link to understand what the entry is about
2. Launch a general-purpose Task agent to research and find a valid replacement URL for that specific project/tool/resource
3. The agent should search for:
   - Official website moves/redirects
   - New GitHub repo locations (if repo was moved/renamed)
   - Alternative official URLs
   - Archive.org snapshots if the project is defunct
4. Report findings with specific replacement recommendations

Focus on YAML files only (the source of truth). For each broken link, provide:
- Original URL
- Entry name and description (context)
- Recommended replacement URL (if found)
- Rationale for the replacement

If no replacement can be found, recommend whether to mark the entry as archived or remove it.

Use parallel Task agents when possible to speed up research.
