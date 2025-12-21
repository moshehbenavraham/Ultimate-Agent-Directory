# Session 02: Migration Script

**Session ID**: `phase00-session02-migration-script`
**Status**: Not Started
**Estimated Tasks**: ~25-30
**Estimated Duration**: 3-4 hours
**Priority**: P0

---

## Objective

Create a robust migration script that parses the source markdown file and generates validated YAML files for all ~100+ boilerplate entries.

---

## Scope

### In Scope (MVP)
- Create `scripts/migrate_boilerplates.py` migration script
- Parse markdown headers to determine ecosystem/category hierarchy
- Extract repository tables (name, URL, stars, license)
- Extract technical stack tables into structured format
- Extract key features as list items
- Extract pros and cons as separate lists
- Extract use case, deployment, and community text
- Generate valid YAML files with proper escaping
- Create category YAML files based on parsed structure
- Handle edge cases (missing fields, malformed tables)

### Out of Scope
- README generation (Session 03)
- Makefile integration (Session 04)
- Manual curation and verification (Session 06)

---

## Prerequisites

- [ ] Session 01 completed (schema and structure in place)
- [ ] Source markdown file analyzed and understood
- [ ] Pydantic models tested and working

---

## Deliverables

1. **`scripts/migrate_boilerplates.py`** with:
   - `BoilerplateMarkdownParser` class
   - Markdown section parsing by header level
   - Table extraction and parsing
   - List extraction for features, pros, cons
   - Text extraction for use case, deployment, community
   - YAML generation with proper escaping

2. **Generated YAML Files**:
   - ~100+ boilerplate entry files in `data/boilerplates/{category}/`
   - ~20 category definition files in `data/boilerplate-categories/`

3. **Migration Report**:
   - Count of successfully migrated entries
   - List of any skipped entries with reasons
   - Validation status

---

## Technical Details

### Parsing Strategy

```
## Ecosystem Header (H2)
  -> determines ecosystem field

### Category Header (H3)
  -> determines category id and creates category file

#### Subcategory Header (H4)
  -> determines subcategory field

##### Entry Header (H5)
  -> individual boilerplate entry
```

### Table Parsing

Two table types to parse:
1. **Attribute table**: Repository, Stars, License, Last Updated
2. **Technical stack table**: Component, Technology, Reasoning

### Edge Case Handling

| Edge Case | Strategy |
|-----------|----------|
| Missing repository URL | Skip entry, log warning |
| Missing description | Use first paragraph of section |
| Malformed table | Attempt regex fallback, then skip |
| Special characters in YAML | Use block scalars (`>` or `\|`) |
| Very long descriptions | Truncate to 2000 chars |
| Duplicate entries | Deduplicate by URL |
| Non-ASCII characters | Convert or remove |

---

## Success Criteria

- [ ] All parseable entries migrated to YAML files
- [ ] All generated YAML files pass schema validation
- [ ] Category YAML files created for each category
- [ ] Migration script runs without errors
- [ ] Edge cases handled gracefully with logging
- [ ] No data loss from source material (except intentionally skipped)
