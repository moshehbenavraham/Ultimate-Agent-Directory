# NEXT_SESSION.md

## Session Recommendation

**Generated**: 2025-12-21
**Project State**: Phase 00 - Feature Addition
**Completed Sessions**: 1

---

## Recommended Next Session

**Session ID**: `phase00-session02-migration-script`
**Session Name**: Migration Script
**Estimated Duration**: 3-4 hours
**Estimated Tasks**: 25-30

---

## Why This Session Next?

### Prerequisites Met
- [x] Session 01 completed (schema and structure in place)
- [x] Source markdown file available (`full-stack_starter_boilerplate_template_kit.md`)
- [x] Pydantic models tested and working (`BoilerplateEntry`, `TechStackComponent`, `BoilerplateCategory`)
- [x] Directory structure created (`data/boilerplates/`, `data/boilerplate-categories/`)
- [x] Sample YAML files validate successfully

### Dependencies
- **Builds on**: Session 01 (Schema & Structure) - uses the Pydantic models and directory structure
- **Enables**: Session 03 (README Generation) - produces the YAML files needed for generation

### Project Progression
This is the core data migration session that transforms ~100+ unstructured markdown entries into validated YAML files. Without this session, no subsequent sessions can proceed - the README generator (Session 03) needs data to render, and the website (Session 05) needs pages to display. This is the critical path for the entire feature.

---

## Session Overview

### Objective
Create a robust migration script that parses the source markdown file and generates validated YAML files for all ~100+ boilerplate entries.

### Key Deliverables
1. **`scripts/migrate_boilerplates.py`** - Complete parsing and generation script
2. **~100+ boilerplate YAML files** - In `data/boilerplates/{category}/`
3. **~20 category YAML files** - In `data/boilerplate-categories/`
4. **Migration report** - Success/skip counts with validation status

### Scope Summary
- **In Scope (MVP)**: Markdown parsing, table extraction, YAML generation, category creation, edge case handling
- **Out of Scope**: README generation, Makefile integration, manual verification

---

## Technical Considerations

### Technologies/Patterns
- Python regex for markdown parsing
- PyYAML for YAML generation with proper escaping
- Pydantic for validation of generated entries
- Block scalars (`>` or `|`) for multi-line text

### Parsing Strategy
```
## Ecosystem Header (H2) -> ecosystem field
### Category Header (H3) -> category ID + category file
#### Subcategory Header (H4) -> subcategory field
##### Entry Header (H5) -> individual boilerplate entry
```

### Potential Challenges
- **Inconsistent markdown formatting** - Source may have variations in table/list structure
- **Special character escaping** - YAML requires proper escaping of colons, quotes
- **Malformed tables** - Some entries may have incomplete or non-standard tables
- **Duplicate entries** - Need deduplication by URL

### Edge Case Handling
| Edge Case | Strategy |
|-----------|----------|
| Missing repository URL | Skip entry, log warning |
| Missing description | Use first paragraph of section |
| Malformed table | Attempt regex fallback, then skip |
| Special characters | Use block scalars |
| Very long descriptions | Truncate to 2000 chars |
| Duplicate entries | Deduplicate by URL |
| Non-ASCII characters | Convert or remove |

---

## Alternative Sessions

If this session is blocked:
1. **phase00-session04-makefile-and-ci** - Could set up make targets with placeholder commands (partial progress)
2. **N/A** - Session 02 has no alternatives; it is the critical path for data migration

---

## Next Steps

Run `/sessionspec` to generate the formal specification for `phase00-session02-migration-script`.
