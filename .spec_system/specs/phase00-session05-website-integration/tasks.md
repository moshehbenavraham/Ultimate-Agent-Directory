# Task Checklist

**Session ID**: `phase00-session05-website-integration`
**Total Tasks**: 24
**Estimated Duration**: 8-10 hours
**Created**: 2025-12-21

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable (can run with other [P] tasks)
- `[S0005]` = Session reference (Phase 00, Session 05)
- `TNNN` = Task ID

---

## Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup | 3 | 3 | 0 |
| Foundation | 6 | 6 | 0 |
| Implementation | 10 | 10 | 0 |
| Testing | 5 | 5 | 0 |
| **Total** | **24** | **24** | **0** |

---

## Setup (3 tasks)

Initial verification and environment preparation.

- [x] T001 [S0005] Verify prerequisites: run `make validate` to confirm all 57 boilerplates and 23 categories are valid
- [x] T002 [S0005] Verify existing website generation works: run `make site` to confirm baseline functionality
- [x] T003 [S0005] Create output directory structure placeholder: `_site/boilerplates/` (generated, for verification)

---

## Foundation (6 tasks)

Core data loading functions and template scaffolds.

- [x] T004 [S0005] Import BoilerplateEntry and BoilerplateCategory models in `generate_site.py` (`scripts/generate_site.py`)
- [x] T005 [S0005] [P] Implement `load_boilerplate_categories()` function (`scripts/generate_site.py`)
- [x] T006 [S0005] [P] Implement `load_boilerplates()` function (`scripts/generate_site.py`)
- [x] T007 [S0005] Implement `group_boilerplates_by_category()` function (`scripts/generate_site.py`)
- [x] T008 [S0005] Implement `group_boilerplates_by_ecosystem()` function for index page grouping (`scripts/generate_site.py`)
- [x] T009 [S0005] Create boilerplate index template scaffold extending base (`templates/boilerplate_index.html.jinja2`)

---

## Implementation (10 tasks)

Main feature implementation for templates, navigation, and generation.

- [x] T010 [S0005] Implement boilerplate index hero section with stats (`templates/boilerplate_index.html.jinja2`)
- [x] T011 [S0005] Implement ecosystem-grouped category cards on index page (`templates/boilerplate_index.html.jinja2`)
- [x] T012 [S0005] Create boilerplate category template scaffold extending base (`templates/boilerplate_category.html.jinja2`)
- [x] T013 [S0005] Implement category header with breadcrumb and metadata badges (`templates/boilerplate_category.html.jinja2`)
- [x] T014 [S0005] Implement boilerplate entry cards with tech stack summary (`templates/boilerplate_category.html.jinja2`)
- [x] T015 [S0005] Add "Boilerplates" navigation link to header and footer (`templates/base.html.jinja2`)
- [x] T016 [S0005] Add boilerplate section/link to homepage hero area (`templates/index.html.jinja2`)
- [x] T017 [S0005] Implement `generate_boilerplate_pages()` function to generate all pages (`scripts/generate_site.py`)
- [x] T018 [S0005] Update `generate_sitemap()` to include boilerplate URLs (`scripts/generate_site.py`)
- [x] T019 [S0005] Implement `create_boilerplate_search_index()` and integrate into main search index (`scripts/generate_site.py`)

---

## Testing (5 tasks)

Verification and quality assurance.

- [x] T020 [S0005] Run `make site` and verify all 24 boilerplate HTML files generated (1 index + 23 categories)
- [x] T021 [S0005] [P] Validate ASCII encoding on all new/modified files (no special characters)
- [x] T022 [S0005] [P] Verify sitemap.xml contains boilerplate URLs (24 new entries)
- [x] T023 [S0005] [P] Verify search-index.json contains boilerplate entries (57 entries)
- [x] T024 [S0005] Run `make serve` and perform manual testing: navigation, category pages, mobile responsiveness

---

## Completion Checklist

Before marking session complete:

- [x] All tasks marked `[x]`
- [x] `make site` completes successfully
- [x] All 24 boilerplate HTML files generated in `_site/boilerplates/`
- [x] All files ASCII-encoded (no special characters)
- [x] Navigation works between AI Agents and Boilerplates sections
- [x] sitemap.xml includes boilerplate URLs
- [x] search-index.json includes boilerplate entries
- [x] Mobile responsiveness verified
- [x] implementation-notes.md updated
- [x] Ready for `/validate`

---

## Notes

### Parallelization
Tasks marked `[P]` can be worked on simultaneously:
- T005, T006: Independent data loading functions
- T021, T022, T023: Independent verification tasks

### Task Dependencies
1. T001-T003 must complete before Foundation tasks
2. T004 must complete before T005-T008
3. T005-T008 must complete before T017
4. T009 must complete before T010-T011
5. T012 must complete before T013-T014
6. All Implementation tasks must complete before Testing tasks

### Key Files Summary
| File | Action | Tasks |
|------|--------|-------|
| `scripts/generate_site.py` | Modify | T004-T008, T017-T019 |
| `templates/boilerplate_index.html.jinja2` | Create | T009-T011 |
| `templates/boilerplate_category.html.jinja2` | Create | T012-T014 |
| `templates/base.html.jinja2` | Modify | T015 |
| `templates/index.html.jinja2` | Modify | T016 |

### Ecosystem Groupings
The index page should group categories by ecosystem:
- **JavaScript/TypeScript**: Next.js, Nuxt, SvelteKit, Remix, Astro, Blitz, Redwood, Meteor, Node.js, HTMX, Wasp
- **Python**: Django, FastAPI, Flask
- **Ruby**: Rails
- **PHP**: Laravel
- **Go**: Go
- **Rust**: Rust
- **.NET**: .NET
- **Elixir**: Phoenix
- **Mobile**: React Native, Expo, Cross-Platform

### ASCII Compliance
Watch for these common issues:
- Curly quotes in YAML descriptions -> use straight quotes
- Em dashes -> use regular hyphens
- Non-ASCII emoji in templates -> use Font Awesome icons or HTML entities

---

## Next Steps

Run `/implement` to begin AI-led implementation.
