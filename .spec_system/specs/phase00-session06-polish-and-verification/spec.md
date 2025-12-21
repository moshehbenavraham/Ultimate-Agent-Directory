# Session Specification

**Session ID**: `phase00-session06-polish-and-verification`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-21

---

## 1. Session Overview

This is the final session of Phase 00, completing the boilerplate directory integration. With the foundational infrastructure now in place (schema, migration, README generation, CI/CD, and website templates), this session focuses on the polish layer that transforms a functional directory into a production-quality user experience.

The session delivers three critical user-facing capabilities: (1) link validation to ensure all 57+ boilerplate URLs are accessible and accurate, (2) search and filter functionality enabling users to quickly find relevant boilerplates across 20+ categories, and (3) featured entry curation to highlight the best-in-class options for each ecosystem.

Additionally, the documentation will be updated to reflect the new boilerplate workflows, ensuring contributors and maintainers can effectively work with the extended directory. Upon completion, Phase 00 will be 100% complete with all PRD objectives met.

---

## 2. Objectives

1. **Validate all boilerplate URLs** - Extend link checker to verify 57+ boilerplate entries, identify broken links, and update `verified` fields
2. **Enable boilerplate search/filter** - Generate search index for boilerplates and add ecosystem/pricing/tag filtering on boilerplate pages
3. **Curate featured boilerplates** - Select and mark 10-15 high-quality entries as featured, display prominently on index
4. **Update project documentation** - Add boilerplate workflows to GETTING_STARTED.md, REFERENCE.md, and any other affected docs

---

## 3. Prerequisites

### Required Sessions
- [x] `phase00-session01-schema-and-structure` - BoilerplateEntry model defined
- [x] `phase00-session02-migration-script` - 57 boilerplate YAML files created
- [x] `phase00-session03-readme-generation` - BOILERPLATES.md generation working
- [x] `phase00-session04-makefile-and-ci-integration` - Build commands and CI integrated
- [x] `phase00-session05-website-integration` - Website templates and pages exist

### Required Tools/Knowledge
- Python async/aiohttp for link checking
- JavaScript for search/filter client-side logic
- Jinja2 templating for featured section

### Environment Requirements
- Python 3.10+ with venv activated
- Network access for link checking
- Browser for manual testing

---

## 4. Scope

### In Scope (MVP)
- Extend `check_links.py` to handle `BoilerplateEntry` models
- Generate `boilerplate-search-index.json` for client-side search
- Add ecosystem filter dropdown to boilerplate index/category pages
- Add pricing filter dropdown to boilerplate pages
- Add tag-based filtering to boilerplate pages
- Mark 10-15 entries as `featured: true` in YAML files
- Add featured section to `boilerplate_index.html.jinja2`
- Update GETTING_STARTED.md with boilerplate workflow
- Update REFERENCE.md with BoilerplateEntry schema
- Run link check and fix/flag any broken links

### Out of Scope (Deferred)
- GitHub API auto-update for star counts - *Reason: Requires API token, rate limiting complexity*
- Advanced analytics/telemetry - *Reason: Not needed for MVP*
- User submission system - *Reason: Requires backend, authentication*
- Lighthouse performance optimization - *Reason: Polish item beyond MVP*

---

## 5. Technical Approach

### Architecture

**Link Checking Extension:**
The existing `check_links.py` already handles `AgentEntry` models. It needs to be extended to also parse `BoilerplateEntry` models from `data/boilerplates/**/*.yml`. The link checker will validate the `url` field and any optional URL fields (`documentation_url`, `community` URLs if HTTP).

**Search Index Generation:**
The site generator (`generate_site.py`) already creates `search-index.json` for agents. It will be extended to also generate `boilerplate-search-index.json` containing name, description, category, ecosystem, tags, and pricing for each boilerplate entry.

**Client-Side Filtering:**
The existing `category.js` provides filtering for agent category pages. Boilerplate pages need similar functionality. Rather than duplicating code, we'll extend the existing JS or create a minimal `boilerplate.js` that handles ecosystem-specific filtering.

### Design Patterns
- **DRY**: Reuse existing link checker infrastructure, extend rather than duplicate
- **Progressive Enhancement**: Filters work without JS (full page loads), enhance with JS
- **URL State**: Filter state stored in query params for shareability (`?ecosystem=python&pricing=free`)

### Technology Stack
- Python 3.10+ (link checking, index generation)
- aiohttp (async HTTP requests)
- JavaScript ES6 (client-side search/filter)
- Jinja2 (template rendering)

---

## 6. Deliverables

### Files to Create
| File | Purpose | Est. Lines |
|------|---------|------------|
| `static/js/boilerplate.js` | Search/filter for boilerplate pages | ~150 |

### Files to Modify
| File | Changes | Est. Lines |
|------|---------|------------|
| `scripts/check_links.py` | Add BoilerplateEntry support (~30 lines) | ~30 |
| `scripts/generate_site.py` | Generate boilerplate-search-index.json (~40 lines) | ~40 |
| `templates/boilerplate_index.html.jinja2` | Add featured section, search box | ~50 |
| `templates/boilerplate_category.html.jinja2` | Add filter controls, tags | ~40 |
| `data/boilerplates/*/*.yml` | Set featured: true on 10-15 entries | ~15 files |
| `docs/GETTING_STARTED.md` | Add boilerplate workflow section | ~40 |
| `docs/REFERENCE.md` | Add BoilerplateEntry schema, boilerplate commands | ~60 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] Link checker validates all 57 boilerplate URLs without errors
- [ ] Broken links identified and either fixed or removed
- [ ] Search on boilerplate index returns relevant results
- [ ] Ecosystem filter shows only matching categories
- [ ] Pricing filter shows only matching entries
- [ ] Tag filter shows entries with selected tags
- [ ] Multiple filters can be combined
- [ ] Featured boilerplates display prominently on index
- [ ] Documentation includes boilerplate workflow

### Testing Requirements
- [ ] Manual test: run `make check-links` and verify boilerplates checked
- [ ] Manual test: search for "django" returns Django boilerplates
- [ ] Manual test: filter by ecosystem "Python" shows only Python entries
- [ ] Manual test: featured section shows curated entries

### Quality Gates
- [ ] All files ASCII-encoded (0-127 characters only)
- [ ] Unix LF line endings
- [ ] No console errors on website
- [ ] `make validate` passes
- [ ] `make site` generates without errors

---

## 8. Implementation Notes

### Key Considerations

**Link Checker Extension:**
- Import `BoilerplateEntry` from models.py alongside `AgentEntry`
- Add `extract_urls_from_boilerplate_yaml()` function or extend existing `extract_urls_from_yaml()`
- The existing function checks for `"url" in data` to identify agent files; boilerplate files also have `url` but different structure
- Consider checking for `technical_stack` or `ecosystem` fields to distinguish boilerplate files

**Search Index Structure:**
```json
{
  "name": "create-t3-app",
  "description": "The TypeScript standard...",
  "category": "nextjs",
  "category_title": "Next.js & T3 Stack",
  "ecosystem": "JavaScript/TypeScript",
  "tags": ["nextjs", "typescript", "trpc"],
  "pricing": "free",
  "url": "https://github.com/t3-oss/create-t3-app",
  "stars": 28300,
  "featured": true
}
```

**Featured Selection Criteria:**
- GitHub stars > 5000
- Active maintenance (updated within 12 months)
- Complete documentation
- Strong community presence
- Representative of category (one featured per major category)

### Potential Challenges

**Mixed Model Detection:**
- Challenge: Link checker needs to distinguish agent vs boilerplate YAML files
- Mitigation: Check file path (`data/boilerplates/` vs `data/agents/`) rather than content

**Filter State Persistence:**
- Challenge: Complex filter combinations in URL
- Mitigation: Use simple query params: `?ecosystem=python&pricing=free&tags=django,fastapi`

**Large Search Index:**
- Challenge: 57 boilerplates + 277 agents = 334 entries in combined index
- Mitigation: Keep separate indices (`search-index.json`, `boilerplate-search-index.json`) for lazy loading

### ASCII Reminder
All output files must use ASCII-only characters (0-127). Check YAML files for any unicode quotes or special characters introduced during migration.

---

## 9. Testing Strategy

### Unit Tests
- Not required for this session (script modifications are minimal)

### Integration Tests
- Run `make validate` - all YAML files pass validation
- Run `make site` - website generates without errors
- Run `make check-links` - link report generated

### Manual Testing

| Test Case | Steps | Expected Result |
|-----------|-------|-----------------|
| Link check includes boilerplates | Run `python scripts/check_links.py --yaml-only` | Boilerplate URLs appear in output |
| Search finds boilerplate | Go to boilerplate index, search "nextjs" | Next.js entries appear |
| Ecosystem filter | Select "Python" from ecosystem dropdown | Only Django, FastAPI, Flask entries shown |
| Pricing filter | Select "free" from pricing dropdown | Only free entries shown |
| Combined filters | Select Python + free | Only free Python entries shown |
| Featured display | Go to boilerplate index | Featured section shows curated entries |
| URL state | Apply filters, copy URL, open in new tab | Same filters applied |

### Edge Cases
- Empty search query - no results shown, placeholder text displayed
- No matches for filter - "No results" message displayed
- Special characters in search - properly escaped, no XSS
- Very long tag list - wraps gracefully on mobile

---

## 10. Dependencies

### External Libraries
- aiohttp: Already installed (used by check_links.py)
- PyYAML: Already installed
- Pydantic: Already installed
- Jinja2: Already installed

### Other Sessions
- **Depends on**: Sessions 01-05 (all complete)
- **Depended by**: None (this is the final session of Phase 00)

---

## 11. Estimated Scope

| Category | Count |
|----------|-------|
| Files to create | 1 |
| Files to modify | 7+ |
| YAML files to update (featured) | 10-15 |
| Estimated tasks | 15-20 |
| Estimated duration | 2-3 hours |

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.
