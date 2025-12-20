# NEXT_SESSION.md

## Session Recommendation

**Generated**: 2025-12-20
**Project State**: Phase 00 - Feature Addition
**Completed Sessions**: 0

---

## Recommended Next Session

**Session ID**: `phase00-session01-schema-and-structure`
**Session Name**: Schema & Structure
**Estimated Duration**: 2-4 hours
**Estimated Tasks**: ~20-25
**Priority**: P0

---

## Why This Session Next?

### Prerequisites Met
- [x] Source markdown file `full-stack_starter_boilerplate_template_kit.md` available
- [x] Existing `scripts/models.py` present and understood
- [x] Existing `scripts/validate.py` present and understood

### Dependencies
- **Builds on**: Existing AI agent data architecture
- **Enables**: All subsequent sessions (02-06)

### Project Progression

This is the **foundational session** for Phase 00. Every other session in this phase depends on the data models and directory structure established here:

- **Session 02 (Migration Script)** requires Pydantic models to validate generated YAML
- **Session 03 (README Generation)** requires schema to load boilerplate data
- **Session 04 (CI Integration)** requires validation functions to exist
- **Session 05 (Website Integration)** requires data loading infrastructure
- **Session 06 (Polish)** requires all previous work complete

There is no alternative starting point. Session 01 must be completed first.

---

## Session Overview

### Objective

Establish the foundational data models and directory structure for the boilerplate system, enabling all subsequent sessions to build upon a validated schema.

### Key Deliverables

1. **Extended `scripts/models.py`** with:
   - `TechStackComponent` model (nested)
   - `BoilerplateEntry` model
   - `BoilerplateCategory` model

2. **Directory Structure**:
   - `data/boilerplates/` with ecosystem subdirectories
   - `data/boilerplate-categories/`

3. **Extended `scripts/validate.py`** with:
   - `load_boilerplate_categories()` function
   - `load_boilerplates()` function
   - Boilerplate validation integration

4. **Sample Files for Testing**:
   - At least 1 sample boilerplate category YAML
   - At least 1 sample boilerplate entry YAML

### Scope Summary

- **In Scope (MVP)**: Pydantic models, directory structure, validation functions, sample files
- **Out of Scope**: Actual data migration, README generation, website integration

---

## Technical Considerations

### Technologies/Patterns
- Pydantic v2 with strict validation (`extra = "forbid"`)
- Type hints and field validators
- Parallel data structure (mirrors existing `data/agents/` approach)

### Key Schema Fields

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `name` | str | Yes | 1-100 chars |
| `url` | HttpUrl | Yes | Repository URL |
| `description` | str | Yes | 20-2000 chars |
| `category` | str | Yes | Must match category ID |
| `technical_stack` | List[TechStackComponent] | No | Structured tech breakdown |
| `key_features` | List[str] | No | Feature list |
| `pros` / `cons` | List[str] | No | Evaluation lists |

### Potential Challenges

1. **Description length limits**: Source markdown may have longer descriptions than 2000 chars
2. **Tag validation**: Ensuring lowercase hyphenated format
3. **Category validation**: Cross-referencing with boilerplate-categories

---

## Alternative Sessions

If this session is blocked:

**There are no valid alternatives.** Session 01 is a prerequisite for all other sessions in Phase 00. If blocked, investigate and resolve the blocker before proceeding.

---

## Next Steps

Run `/sessionspec` to generate the formal task specification with 15-30 actionable tasks.
