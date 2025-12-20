# Task Checklist

**Session ID**: `phase00-session02-migration-script`
**Total Tasks**: 26
**Estimated Duration**: 8-10 hours
**Created**: 2025-12-21

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable (can run with other [P] tasks)
- `[S0002]` = Session reference (Phase 00, Session 02)
- `TNNN` = Task ID

---

## Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup | 3 | 3 | 0 |
| Foundation | 6 | 6 | 0 |
| Implementation | 12 | 12 | 0 |
| Testing | 5 | 5 | 0 |
| **Total** | **26** | **26** | **0** |

---

## Setup (3 tasks)

Initial configuration and environment preparation.

- [x] T001 [S0002] Verify prerequisites: Python 3.10+, models.py exists, target directories exist
- [x] T002 [S0002] Create `scripts/migrate_boilerplates.py` with imports and configuration
- [x] T003 [S0002] Define category ID mapping dictionary (H3 header -> category ID)

---

## Foundation (6 tasks)

Core helper functions and class structure.

- [x] T004 [S0002] [P] Implement `slugify()` helper function for file name generation
- [x] T005 [S0002] [P] Implement `parse_star_count()` helper for normalizing star strings
- [x] T006 [S0002] [P] Implement `sanitize_ascii()` helper for removing non-ASCII characters
- [x] T007 [S0002] Create `BoilerplateMarkdownParser` class with `__init__` and `run()` method
- [x] T008 [S0002] Implement `load_document()` method to read source markdown
- [x] T009 [S0002] Implement `split_by_h2_ecosystems()` to parse H2 header blocks

---

## Implementation (12 tasks)

Main parser and generator implementation.

### Hierarchy Parsers

- [x] T010 [S0002] Implement `parse_ecosystem()` to split H2 blocks by H3 categories
- [x] T011 [S0002] Implement `parse_category()` to split H3 blocks by H4 subcategories
- [x] T012 [S0002] Implement `parse_entry()` to extract data from H5 entry blocks

### Table Extractors

- [x] T013 [S0002] [P] Implement `extract_attribute_table()` for Repository/Stars/License/LastUpdated
- [x] T014 [S0002] [P] Implement `extract_tech_stack_table()` for Component/Technology/Reasoning

### List and Text Extractors

- [x] T015 [S0002] [P] Implement `extract_features_list()` for Key Features bullet points
- [x] T016 [S0002] [P] Implement `extract_pros_cons()` for Pros and Cons sections
- [x] T017 [S0002] [P] Implement `extract_text_sections()` for Use Case/Community/Deployment prose

### File Generation

- [x] T018 [S0002] Implement `generate_yaml_content()` with proper escaping (block scalars)
- [x] T019 [S0002] Implement `write_category_files()` to create category YAML files
- [x] T020 [S0002] Implement `write_entry_files()` to create boilerplate YAML files
- [x] T021 [S0002] Add duplicate detection by URL with skip-and-warn behavior

---

## Testing (5 tasks)

Verification and quality assurance.

- [x] T022 [S0002] Run migration script: `python scripts/migrate_boilerplates.py`
- [x] T023 [S0002] Run schema validation: `make validate` - ensure 100% pass rate
- [x] T024 [S0002] Spot-check 5 random entries against source markdown for accuracy
- [x] T025 [S0002] Verify ASCII encoding on all generated files (no special characters)
- [x] T026 [S0002] Review migration statistics and document any skipped entries

---

## Completion Checklist

Before marking session complete:

- [x] All tasks marked `[x]`
- [x] `make validate` passes 100%
- [x] All files ASCII-encoded (LF line endings)
- [x] 57 boilerplate YAML files generated
- [x] 23 category YAML files generated
- [x] implementation-notes.md updated
- [x] Ready for `/validate`

---

## Notes

### Parallelization
Tasks marked `[P]` can be worked on simultaneously:
- T004, T005, T006 (helper functions)
- T013, T014 (table extractors)
- T015, T016, T017 (list/text extractors)

### Task Timing
Target ~20-25 minutes per task. Implementation tasks (T010-T021) may take longer.

### Dependencies
- T007-T009 depend on T003 (category mapping)
- T010-T012 depend on T008-T009 (document loading)
- T013-T017 depend on T012 (entry parsing)
- T018-T021 depend on T013-T017 (extractors)
- T022-T026 depend on T021 (all implementation complete)

### Key Edge Cases
- Entries with no attribute table -> Extract URL from first link
- Entries with no tech stack table -> Leave field empty
- Inline pros/cons (not bulleted) -> Parse "Pros:" and "Cons:" lines
- Star counts with "~", "k", or "," -> Normalize to integer
- Very long descriptions (>2000 chars) -> Truncate with warning
- Duplicate URLs -> Keep first, skip subsequent with warning

### Source File Statistics
- File: `full-stack_starter_boilerplate_template_kit.md`
- Lines: 2,327
- Expected entries: ~75 (H5 headers)
- Expected categories: ~12-15 (H3 headers)
- Expected ecosystems: ~6 (H2 headers)

---

## Next Steps

Run `/implement` to begin AI-led implementation.
