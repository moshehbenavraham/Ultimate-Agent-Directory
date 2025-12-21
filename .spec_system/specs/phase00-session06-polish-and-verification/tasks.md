# Task Checklist

**Session ID**: `phase00-session06-polish-and-verification`
**Total Tasks**: 24
**Estimated Duration**: 3-4 hours
**Created**: 2025-12-21

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable (can run with other [P] tasks)
- `[S0006]` = Session reference (Phase 00, Session 06)
- `TNNN` = Task ID

---

## Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup | 2 | 2 | 0 |
| Link Checker | 4 | 4 | 0 |
| Search/Filter | 5 | 5 | 0 |
| Featured Curation | 3 | 3 | 0 |
| Template Updates | 4 | 4 | 0 |
| Documentation | 3 | 3 | 0 |
| Testing | 3 | 3 | 0 |
| **Total** | **24** | **24** | **0** |

---

## Setup (2 tasks)

Initial verification and environment preparation.

- [x] T001 [S0006] Verify all prerequisites are met (`make validate`, `make site`)
- [x] T002 [S0006] Read existing JavaScript filtering code (`static/js/category.js`)

---

## Link Checker Extension (4 tasks)

Extend check_links.py to validate boilerplate URLs.

- [x] T003 [S0006] Import BoilerplateEntry model in check_links.py (`scripts/check_links.py`)
- [x] T004 [S0006] Add boilerplate URL extraction to collect_all_urls() (`scripts/check_links.py`)
- [x] T005 [S0006] Test link checker with --yaml-only flag includes boilerplates (`scripts/check_links.py`)
- [x] T006 [S0006] Run full link check and document any broken links (`reports/`)

---

## Search and Filter Implementation (5 tasks)

Add client-side search and filtering for boilerplate pages.

- [x] T007 [S0006] Create boilerplate.js with ecosystem filter logic (`static/js/boilerplate.js`)
- [x] T008 [S0006] Add pricing filter functionality to boilerplate.js (`static/js/boilerplate.js`)
- [x] T009 [S0006] Add tag-based filtering to boilerplate.js (`static/js/boilerplate.js`)
- [x] T010 [S0006] Add combined filter logic with URL state persistence (`static/js/boilerplate.js`)
- [x] T011 [S0006] Add search input handler for boilerplate name/description search (`static/js/boilerplate.js`)

---

## Featured Boilerplate Curation (3 tasks)

Select and mark 10-15 high-quality boilerplates as featured.

- [x] T012 [S0006] [P] Analyze boilerplates by github_stars to identify featured candidates (`data/boilerplates/`)
- [x] T013 [S0006] [P] Update 10-15 YAML files with `featured: true` across ecosystems (`data/boilerplates/**/*.yml`)
- [x] T014 [S0006] Verify featured count and distribution across categories (`data/boilerplates/`)

---

## Template Updates (4 tasks)

Add filter controls and featured section to boilerplate templates.

- [x] T015 [S0006] Add search box to boilerplate_index template (`templates/boilerplate_index.html.jinja2`)
- [x] T016 [S0006] Add featured boilerplates section to index template (`templates/boilerplate_index.html.jinja2`)
- [x] T017 [S0006] Add filter dropdowns (ecosystem, pricing) to category template (`templates/boilerplate_category.html.jinja2`)
- [x] T018 [S0006] Add boilerplate.js script include to both templates (`templates/boilerplate_*.html.jinja2`)

---

## Documentation Updates (3 tasks)

Update project documentation with boilerplate workflow.

- [x] T019 [S0006] [P] Add boilerplate workflow section to GETTING_STARTED.md (`docs/GETTING_STARTED.md`)
- [x] T020 [S0006] [P] Add BoilerplateEntry schema to REFERENCE.md (`docs/REFERENCE.md`)
- [x] T021 [S0006] [P] Add boilerplate commands (make targets) to REFERENCE.md (`docs/REFERENCE.md`)

---

## Testing and Verification (3 tasks)

Validate all changes work correctly.

- [x] T022 [S0006] Run make validate and make site to verify generation (`Makefile`)
- [x] T023 [S0006] Manual test: serve site and verify search/filters work (`make serve`)
- [x] T024 [S0006] Validate all files are ASCII-encoded with LF line endings (`scripts/`)

---

## Completion Checklist

Before marking session complete:

- [x] All tasks marked `[x]`
- [x] `make validate` passes
- [x] `make site` generates without errors
- [x] Search functionality works in browser
- [x] Filters work individually and combined
- [x] Featured section displays on boilerplate index
- [x] All files ASCII-encoded
- [x] Documentation updated
- [x] Ready for `/validate`

---

## Notes

### Parallelization
Tasks marked `[P]` can be worked on simultaneously:
- T012-T013: Featured curation tasks
- T019-T021: Documentation updates

### Task Timing
Target ~20-25 minutes per task.

### Dependencies
- T003-T006: Sequential (link checker extension)
- T007-T011: Sequential (incremental JS development)
- T015-T018: Can start after T011 (templates need JS reference)
- T022-T24: Final validation (must be last)

### Featured Selection Criteria
Based on spec requirements:
- GitHub stars > 5000
- Active maintenance (last update within 12 months)
- Complete documentation
- Representative of category (one featured per major category)

### Key Files
| File | Changes |
|------|---------|
| `scripts/check_links.py` | Add BoilerplateEntry support |
| `static/js/boilerplate.js` | New file: search/filter logic |
| `templates/boilerplate_index.html.jinja2` | Featured section, search box |
| `templates/boilerplate_category.html.jinja2` | Filter controls |
| `data/boilerplates/**/*.yml` | 10-15 files with featured: true |
| `docs/GETTING_STARTED.md` | Boilerplate workflow section |
| `docs/REFERENCE.md` | BoilerplateEntry schema, commands |

---

## Next Steps

Run `/implement` to begin AI-led implementation.
