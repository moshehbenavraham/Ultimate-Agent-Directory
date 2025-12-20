# Session Specification

**Session ID**: `phase00-session02-migration-script`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-21

---

## 1. Session Overview

This session creates the migration script that transforms the unstructured `full-stack_starter_boilerplate_template_kit.md` file (2327 lines, ~75 boilerplate entries) into validated YAML files. The script parses the markdown hierarchy (H2 ecosystems, H3 categories, H4 subcategories, H5 entries) and extracts structured data including attribute tables, technical stack tables, feature lists, pros/cons, and descriptive text.

The migration is the critical path for the entire feature. Without YAML data files, subsequent sessions cannot proceed - the README generator (Session 03) needs entries to render, and the website (Session 05) needs pages to display. This session transforms documentation prose into machine-readable, schema-validated data.

The script uses regex-based parsing with graceful degradation for edge cases. All output is validated against the Pydantic models created in Session 01 before writing to disk, ensuring data quality from the start.

---

## 2. Objectives

1. Create a complete `scripts/migrate_boilerplates.py` script that parses the source markdown and generates validated YAML files
2. Migrate all parseable entries (~75) to individual YAML files in `data/boilerplates/{category}/`
3. Generate category definition files (~12-15) in `data/boilerplate-categories/`
4. Produce a migration report showing success/skip counts and validation status

---

## 3. Prerequisites

### Required Sessions
- [x] `phase00-session01-schema-and-structure` - Provides Pydantic models (`BoilerplateEntry`, `TechStackComponent`, `BoilerplateCategory`) and directory structure

### Required Tools/Knowledge
- Python 3.10+ with regex, PyYAML, Pydantic
- Understanding of markdown table parsing
- YAML escaping rules (colons, quotes, multi-line text)

### Environment Requirements
- Source file: `full-stack_starter_boilerplate_template_kit.md` (exists, 2327 lines)
- Target directories: `data/boilerplates/`, `data/boilerplate-categories/` (exist with subdirectories)
- Models: `scripts/models.py` with all boilerplate models (exists)

---

## 4. Scope

### In Scope (MVP)
- Create `scripts/migrate_boilerplates.py` with `BoilerplateMarkdownParser` class
- Parse markdown headers (H2-H5) to determine ecosystem/category/subcategory/entry hierarchy
- Extract attribute tables (Repository, Stars, License, Last Updated)
- Extract technical stack tables (Component, Technology, Reasoning)
- Extract bullet lists for key features, pros, and cons
- Extract prose text for use_case, community, and deployment
- Generate YAML with proper escaping (block scalars for multi-line text)
- Create category YAML files with ecosystem grouping
- Handle edge cases: missing fields, malformed tables, special characters, duplicates
- Validate all generated entries against Pydantic schemas before writing
- Generate migration report with statistics

### Out of Scope (Deferred)
- README generation - *Reason: Session 03 scope*
- Makefile integration - *Reason: Session 04 scope*
- Manual verification of entries - *Reason: Session 06 scope*
- GitHub API star count updates - *Reason: Future enhancement*
- Website page generation - *Reason: Session 05 scope*

---

## 5. Technical Approach

### Architecture

```
Source Markdown
      |
      v
BoilerplateMarkdownParser
      |
      +-- parse_document() -> splits by H2 ecosystems
      |       |
      |       +-- parse_ecosystem() -> splits by H3 categories
      |               |
      |               +-- parse_category() -> splits by H4 subcategories
      |                       |
      |                       +-- parse_entry() -> extracts H5 entry data
      |
      +-- Table Extractors:
      |       +-- extract_attribute_table() -> repo, stars, license
      |       +-- extract_tech_stack_table() -> component, technology, reasoning
      |
      +-- List Extractors:
      |       +-- extract_features_list() -> key_features[]
      |       +-- extract_pros_cons() -> pros[], cons[]
      |
      +-- Text Extractors:
              +-- extract_use_case() -> use_case
              +-- extract_community() -> community
              +-- extract_deployment() -> deployment
      |
      v
Pydantic Validation (BoilerplateEntry, BoilerplateCategory)
      |
      v
YAML File Generation with ruamel.yaml or PyYAML
      |
      v
data/boilerplates/{category}/{slug}.yml
data/boilerplate-categories/{category}.yml
```

### Design Patterns
- **Parser Pattern**: `BoilerplateMarkdownParser` class encapsulates all parsing logic
- **Builder Pattern**: Incrementally construct entry data from multiple extractions
- **Strategy Pattern**: Different extractors for tables vs lists vs prose
- **Fail-Fast Validation**: Validate with Pydantic before writing any file

### Technology Stack
- Python 3.10+ (standard library: re, pathlib, typing)
- PyYAML 6.0+ for YAML generation
- Pydantic 2.x for validation (already installed via Session 01)
- Optional: ruamel.yaml for block scalar formatting

---

## 6. Deliverables

### Files to Create
| File | Purpose | Est. Lines |
|------|---------|------------|
| `scripts/migrate_boilerplates.py` | Main migration script with parser class | ~400-500 |
| `data/boilerplates/{category}/*.yml` | ~75 boilerplate entry files | ~100 each |
| `data/boilerplate-categories/*.yml` | ~12-15 category definition files | ~20 each |

### Files to Modify
| File | Changes | Est. Lines |
|------|---------|------------|
| None | No modifications needed | 0 |

### Generated Output Summary
- **Boilerplate entries**: ~75 YAML files across ~12-15 category directories
- **Category definitions**: ~12-15 YAML files in `data/boilerplate-categories/`
- **Migration report**: Console output with statistics

---

## 7. Success Criteria

### Functional Requirements
- [ ] Script runs without errors: `python scripts/migrate_boilerplates.py`
- [ ] All parseable entries (~75) migrated to YAML files
- [ ] All generated YAML files pass schema validation: `make validate`
- [ ] Category YAML files created for each unique category
- [ ] Entry data extracted correctly: name, url, description, technical_stack, key_features, pros, cons
- [ ] Duplicate entries (by URL) are deduplicated
- [ ] Missing required fields cause entry skip with warning (not crash)

### Testing Requirements
- [ ] Manual test: Run script and verify file count matches expected
- [ ] Manual test: Spot-check 5 random entries for data accuracy
- [ ] Validation test: Run `make validate` passes 100%

### Quality Gates
- [ ] All files ASCII-encoded (no special characters)
- [ ] Unix LF line endings
- [ ] YAML properly escaped (colons in values, quotes, multi-line)
- [ ] File names are slug-safe (lowercase, hyphens)
- [ ] No empty or malformed YAML files

---

## 8. Implementation Notes

### Key Considerations
- The source markdown uses inconsistent formatting in some sections
- Some entries lack attribute tables or technical stack tables
- Pros/Cons may be inline (single line) or bulleted lists
- Star counts include "~" prefix and "k" suffix (e.g., "~28.3k")
- Some entries reference external links in description text

### Potential Challenges
- **Inconsistent table formats**: Some use `| Attribute | Details |`, others use different headers. Mitigation: Flexible regex patterns with fallbacks
- **Embedded markdown in descriptions**: Links, bold text, code spans. Mitigation: Preserve markdown syntax in YAML strings
- **Star count parsing**: "~28,300" vs "~15.1k" vs "~5,900". Mitigation: Normalize to integer with helper function
- **Category ID generation**: "Next.js & T3 Stack" -> "nextjs". Mitigation: Predefined mapping or slugify function

### ASCII Reminder
All output files must use ASCII-only characters (0-127). Convert or remove any non-ASCII characters (curly quotes, em dashes, etc.).

---

## 9. Testing Strategy

### Unit Tests
- Not required for migration script (one-time use)

### Integration Tests
- Run full migration and validate output with `make validate`

### Manual Testing
- [ ] Verify entry count matches expected (~75)
- [ ] Spot-check 5 entries against source markdown
- [ ] Verify category files match ecosystem structure
- [ ] Check edge cases: entries with missing tables, minimal content

### Edge Cases
- Entry with no attribute table -> Extract URL from first link
- Entry with no technical stack table -> Leave field empty
- Entry with inline pros/cons (not bulleted) -> Parse from "Pros:" and "Cons:" lines
- Entry with very long description (>2000 chars) -> Truncate with warning
- Duplicate URL -> Keep first occurrence, skip subsequent

---

## 10. Dependencies

### External Libraries
- `pyyaml`: 6.0+ (already installed)
- `pydantic`: 2.x (already installed)
- Standard library: `re`, `pathlib`, `typing`, `datetime`

### Other Sessions
- **Depends on**: `phase00-session01-schema-and-structure` (completed)
- **Depended by**: `phase00-session03-readme-generation`, `phase00-session04-makefile-and-ci`, `phase00-session05-website-integration`

---

## 11. Source Analysis Summary

Based on analysis of `full-stack_starter_boilerplate_template_kit.md`:

| Metric | Value |
|--------|-------|
| Total lines | 2,327 |
| H5 headers (entries) | ~75 |
| H2 ecosystems | ~6 (JavaScript/TypeScript, Python, PHP, Ruby, Go, Rust, etc.) |
| H3 categories | ~12-15 |
| H4 subcategories | ~20+ |

### Entry Structure Pattern

```markdown
##### Entry Name
Description paragraph(s)

| Attribute | Details |
|-----------|---------|
| Repository | [owner/repo](url) |
| Stars | ~X,XXX |
| License | MIT |
| Last Updated | Month Year |

**Technical Stack:**
| Component | Technology | Reasoning |
|-----------|------------|-----------|
| Frontend | Next.js | ... |

**Key Features:**
- Feature 1
- Feature 2

**Use Case:** Prose description...

**Pros:** List or inline...
**Cons:** List or inline...

**Community:** Discord info, maintainers...
```

---

## 12. Category Mapping

Predefined category ID mappings based on source analysis:

| Source Header | Category ID | Ecosystem |
|---------------|-------------|-----------|
| Next.js & T3 Stack | nextjs | JavaScript/TypeScript |
| Remix | remix | JavaScript/TypeScript |
| Vue / Nuxt.js | nuxt | JavaScript/TypeScript |
| Svelte / SvelteKit | sveltekit | JavaScript/TypeScript |
| Astro & HTML-First | astro | JavaScript/TypeScript |
| FastAPI | fastapi | Python |
| Django | django | Python |
| Laravel | laravel | PHP |
| Rails | rails | Ruby |
| Go / Golang | go | Go |
| Rust | rust | Rust |
| .NET / C# | dotnet | .NET |
| Elixir / Phoenix | phoenix | Elixir |

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.
