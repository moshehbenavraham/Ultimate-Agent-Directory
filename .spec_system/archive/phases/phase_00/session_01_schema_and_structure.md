# Session 01: Schema & Structure

**Session ID**: `phase00-session01-schema-and-structure`
**Status**: Not Started
**Estimated Tasks**: ~20-25
**Estimated Duration**: 2-4 hours
**Priority**: P0

---

## Objective

Establish the foundational data models and directory structure for the boilerplate system, enabling all subsequent sessions to build upon a validated schema.

---

## Scope

### In Scope (MVP)
- Add `BoilerplateEntry` Pydantic model to `scripts/models.py`
- Add `TechStackComponent` nested model for technical stack entries
- Add `BoilerplateCategory` model for category definitions
- Create `data/boilerplates/` directory structure with ecosystem subdirectories
- Create `data/boilerplate-categories/` directory
- Update `validate.py` with boilerplate validation functions
- Create sample YAML files for testing validation

### Out of Scope
- Actual migration of boilerplate entries (Session 02)
- README generation (Session 03)
- Website integration (Session 05)

---

## Prerequisites

- [ ] Source markdown file `full-stack_starter_boilerplate_template_kit.md` available
- [ ] Existing `scripts/models.py` understood
- [ ] Existing `scripts/validate.py` understood

---

## Deliverables

1. **Extended `scripts/models.py`** with:
   - `TechStackComponent` model
   - `BoilerplateEntry` model
   - `BoilerplateCategory` model

2. **Directory Structure Created**:
   - `data/boilerplates/` with ecosystem subdirectories (nextjs, django, etc.)
   - `data/boilerplate-categories/`

3. **Extended `scripts/validate.py`** with:
   - `load_boilerplate_categories()` function
   - `load_boilerplates()` function
   - `validate_boilerplate()` function
   - Integration with existing validation pipeline

4. **Sample Files for Testing**:
   - At least 1 sample boilerplate category YAML
   - At least 1 sample boilerplate entry YAML

---

## Technical Details

### BoilerplateEntry Schema

Key fields:
- `name`, `url`, `description`, `category` (required)
- `github_repo`, `stars`, `license`, `last_updated` (repository metadata)
- `technical_stack` (list of TechStackComponent)
- `key_features`, `pros`, `cons` (lists)
- `use_case`, `deployment`, `community` (text)
- `subcategory`, `tags`, `pricing` (classification)
- `featured`, `verified` (editorial flags)
- `added_date`, `last_verified` (tracking)

### Validation Rules
- `github_repo` must be in `owner/repo` format
- `tags` must be lowercase and hyphenated
- `category` must match a valid boilerplate category ID
- `description` must be 20-2000 characters
- Strict validation (`extra = "forbid"`)

---

## Success Criteria

- [ ] All three Pydantic models importable without errors
- [ ] Sample YAML files validate successfully
- [ ] `make validate` continues to work for existing agent entries
- [ ] New validation functions callable and functional
- [ ] Directory structure created with correct hierarchy
