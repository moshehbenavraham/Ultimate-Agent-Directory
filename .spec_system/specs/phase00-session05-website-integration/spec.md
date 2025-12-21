# Session Specification

**Session ID**: `phase00-session05-website-integration`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-21

---

## 1. Session Overview

This session extends the existing static website to include a complete boilerplate directory section. The Ultimate Agent Directory currently serves AI agents across 10 categories with a polished Tailwind CSS-based interface. This session adds parallel pages for the 57 boilerplate entries across 23 categories that were migrated in Session 02.

The implementation follows the established patterns from the existing AI agents website: a Jinja2 template hierarchy extending `base.html.jinja2`, client-side search/filtering with JavaScript, and GitHub Pages deployment. The key differentiator is that boilerplate entries contain richer metadata (technical stacks, pros/cons, use cases) which requires enhanced display components.

This session is critical because the website is the primary way users discover and evaluate boilerplate starters. Without these pages, the ~57 migrated entries remain inaccessible to most users who won't browse raw YAML files or the markdown README.

---

## 2. Objectives

1. Generate boilerplate index page at `_site/boilerplates/index.html` with ecosystem overview and category navigation
2. Generate category pages at `_site/boilerplates/{category}/index.html` for all 23 boilerplate categories
3. Integrate boilerplate navigation into the existing site header and footer
4. Update sitemap and search index to include boilerplate entries

---

## 3. Prerequisites

### Required Sessions
- [x] `phase00-session01-schema-and-structure` - BoilerplateEntry and BoilerplateCategory models exist
- [x] `phase00-session02-migration-script` - 57 boilerplate YAML files exist in `data/boilerplates/`
- [x] `phase00-session03-readme-generation` - BOILERPLATES.md generation working
- [x] `phase00-session04-makefile-and-ci-integration` - CI/CD pipeline updated

### Required Tools/Knowledge
- Python 3.11+ with Jinja2, PyYAML, Pydantic
- Understanding of existing `generate_site.py` architecture
- Tailwind CSS utility classes (via CDN)

### Environment Requirements
- All 57 boilerplate YAML files validated
- All 23 boilerplate category YAML files validated
- Existing website generation working (`make site`)

---

## 4. Scope

### In Scope (MVP)
- Boilerplate index page with ecosystem grouping
- Category pages with entry cards showing technical details
- Entry cards displaying: name, stars, license, description, tags, technical stack summary
- Navigation links between AI Agents and Boilerplates sections
- Updated sitemap.xml with boilerplate URLs
- Boilerplate entries in search-index.json
- Responsive design matching existing pages

### Out of Scope (Deferred)
- Client-side search filtering for boilerplates - *Reason: Session 06 scope*
- Client-side tag/ecosystem filtering - *Reason: Session 06 scope*
- Full technical stack table expansion - *Reason: Can be enhanced later*
- Pros/cons modal or accordion display - *Reason: MVP shows summary only*

---

## 5. Technical Approach

### Architecture

The implementation extends `generate_site.py` with parallel functions for boilerplate data:

```
generate_site.py
+-- load_boilerplate_categories()     # NEW: Load from data/boilerplate-categories/
+-- load_boilerplates()               # NEW: Load from data/boilerplates/
+-- group_boilerplates_by_category()  # NEW: Group for rendering
+-- group_boilerplates_by_ecosystem() # NEW: For index page
+-- generate_boilerplate_pages()      # NEW: Main generation function
+-- create_boilerplate_search_index() # NEW: Search index entries
```

Page structure:
```
_site/
+-- index.html                 (MODIFY: add boilerplate nav link)
+-- boilerplates/
    +-- index.html             (NEW: boilerplate home)
    +-- nextjs/
    |   +-- index.html         (NEW: Next.js category)
    +-- django/
    |   +-- index.html         (NEW: Django category)
    +-- ... (23 category pages total)
```

### Design Patterns
- **Template Inheritance**: Extend `base.html.jinja2` for consistent header/footer
- **Component Reuse**: Entry cards follow `category.html.jinja2` patterns
- **Progressive Enhancement**: Static HTML first, JavaScript enhancements for search

### Technology Stack
- Python 3.11+ (generation scripts)
- Jinja2 (template rendering)
- Tailwind CSS via CDN (styling)
- Font Awesome via CDN (icons)
- Vanilla JavaScript (mobile menu, search)

---

## 6. Deliverables

### Files to Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `templates/boilerplate_index.html.jinja2` | Boilerplate directory home page | ~150 |
| `templates/boilerplate_category.html.jinja2` | Individual category page template | ~200 |

### Files to Modify

| File | Changes | Est. Lines |
|------|---------|------------|
| `scripts/generate_site.py` | Add boilerplate loading and page generation | ~150 |
| `templates/base.html.jinja2` | Add "Boilerplates" nav link | ~10 |
| `templates/index.html.jinja2` | Add boilerplate section/link in hero | ~20 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] `python scripts/generate_site.py` generates boilerplate pages without errors
- [ ] Boilerplate index page displays all 23 categories grouped by ecosystem
- [ ] Each category page displays all entries for that category
- [ ] Entry cards show: name, description, stars, license, tags, technical stack count
- [ ] Navigation between AI Agents and Boilerplates sections works
- [ ] All internal links resolve correctly
- [ ] sitemap.xml includes boilerplate URLs
- [ ] search-index.json includes boilerplate entries

### Testing Requirements
- [ ] `make site` completes successfully
- [ ] `make serve` displays boilerplate pages at http://localhost:8001/boilerplates/
- [ ] Manual testing of all 23 category pages
- [ ] Mobile responsiveness verified

### Quality Gates
- [ ] All files ASCII-encoded (no special characters)
- [ ] Unix LF line endings
- [ ] Code follows existing patterns in generate_site.py
- [ ] Templates follow existing Jinja2 conventions
- [ ] No console errors in browser

---

## 8. Implementation Notes

### Key Considerations

1. **Ecosystem Grouping**: The boilerplate index should group categories by their `ecosystem` field (JavaScript, Python, Go, etc.) for intuitive navigation

2. **Technical Stack Display**: Each boilerplate has a `technical_stack` list with components. Show a summary (e.g., "5 technologies") in cards, not full tables

3. **Consistent Styling**: Match the existing blue/gray color scheme, card shadows, and hover effects from `category.html.jinja2`

4. **URL Structure**: Use `/boilerplates/{category-id}/index.html` (directory-style) not `/boilerplates/{category-id}.html` for cleaner URLs

5. **Base URL**: All links must use `{{ base_url }}` prefix for GitHub Pages subdirectory deployment

### Potential Challenges

- **Large Entry Cards**: Boilerplates have more metadata than agents. Card design must accommodate without becoming cluttered
  - *Mitigation*: Use progressive disclosure - show key fields, expand for details

- **23 Categories**: More categories than agents (10). Index page layout must scale
  - *Mitigation*: Group by ecosystem with collapsible sections

- **Inconsistent Data**: Some entries may have missing optional fields (pros, cons, community)
  - *Mitigation*: Use Jinja2 conditionals to gracefully handle missing data

### ASCII Reminder

All output files must use ASCII-only characters (0-127). Watch for:
- Curly quotes in descriptions
- Em dashes
- Non-ASCII emoji in template strings (use HTML entities or Font Awesome)

---

## 9. Testing Strategy

### Unit Tests
- Verify `load_boilerplates()` returns 57 entries
- Verify `load_boilerplate_categories()` returns 23 categories
- Verify ecosystem grouping produces expected structure

### Integration Tests
- Run `make site` and verify output directory structure
- Verify all 23 + 1 (index) HTML files generated
- Verify sitemap.xml includes boilerplate URLs

### Manual Testing
- Navigate from homepage to boilerplates
- Click through each category
- Verify entry links open correct external URLs
- Test on mobile viewport (Chrome DevTools)
- Check for broken images/icons

### Edge Cases
- Categories with only 1 entry
- Entries with no tags
- Entries with empty technical_stack
- Very long descriptions (should truncate in cards)

---

## 10. Dependencies

### External Libraries
- Jinja2: 3.1.2+ (already in requirements.txt)
- PyYAML: 6.0+ (already in requirements.txt)
- Pydantic: 2.0+ (already in requirements.txt)

### Other Sessions
- **Depends on**: phase00-session01 through phase00-session04 (all complete)
- **Depended by**: phase00-session06-polish-and-verification

---

## 11. Template Design Specifications

### Boilerplate Index Page (`boilerplate_index.html.jinja2`)

```
Hero Section:
- Title: "Full-Stack Boilerplates Directory"
- Subtitle: Total count badge, ecosystem count
- Search box (placeholder for Session 06)

Stats Section:
- Grid showing top 4 ecosystems with entry counts

Ecosystem Sections (grouped):
- JavaScript/TypeScript (Next.js, Nuxt, Svelte, etc.)
- Python (Django, FastAPI, Flask)
- Other Languages (Go, Rust, .NET, PHP, Ruby, Elixir)
- Mobile & Cross-Platform

Each Category Card:
- Emoji + Title
- Entry count badge
- 1-line description
- "Explore" link
```

### Boilerplate Category Page (`boilerplate_category.html.jinja2`)

```
Breadcrumb:
- Home > Boilerplates > {Category Title}

Category Header:
- Emoji, title, description
- Entry count, ecosystem badge

Entry Cards Grid:
- Name (linked to repo)
- GitHub stars badge
- License badge
- Description (truncated to ~200 chars)
- Tags as pills
- Tech stack summary: "Built with: React, PostgreSQL, +3 more"
- Links: Visit, GitHub, Docs (if available)
```

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.
