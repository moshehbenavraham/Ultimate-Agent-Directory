# Session Specification

**Session ID**: `phase00-session01-schema-and-structure`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-20

---

## 1. Session Overview

This session establishes the foundational data architecture for integrating a Full-Stack Boilerplate Directory into the existing Ultimate AI Agent Directory system. The goal is to create Pydantic models and validation infrastructure that mirror the existing agent data architecture, enabling a parallel structure where boilerplates and AI agents coexist with shared tooling.

The boilerplate system requires richer metadata than AI agents, including technical stack breakdowns, pros/cons evaluations, and community information. This session defines the schema to capture all this information while maintaining validation consistency with the existing codebase.

Upon completion, all subsequent sessions (migration, generation, CI, website) will build upon the models and validation functions created here. This is the critical foundation - no other work can proceed until this session is complete.

---

## 2. Objectives

1. **Define Pydantic models** for boilerplate entries, technical stacks, and categories that capture all required metadata from the source material
2. **Create directory structure** for boilerplate YAML files that mirrors the existing `data/agents/` pattern
3. **Extend validation script** with functions to load and validate boilerplate data alongside existing agent validation
4. **Validate with samples** by creating at least one working boilerplate entry and category to prove the schema works

---

## 3. Prerequisites

### Required Sessions
- None (this is the first session)

### Required Tools/Knowledge
- Python 3.x with Pydantic v2
- Understanding of existing `scripts/models.py` structure
- Understanding of existing `scripts/validate.py` patterns
- Familiarity with YAML syntax

### Environment Requirements
- Python virtual environment with `pydantic` and `pyyaml` installed
- Access to `data/` directory structure
- Source file `full-stack_starter_boilerplate_template_kit.md` for reference

---

## 4. Scope

### In Scope (MVP)
- Add `TechStackComponent` nested model to `scripts/models.py`
- Add `BoilerplateEntry` model with all required/optional fields
- Add `BoilerplateCategory` model with ecosystem support
- Create `data/boilerplates/` directory with 12 ecosystem subdirectories
- Create `data/boilerplate-categories/` directory
- Add `validate_boilerplate_file()` function to `scripts/validate.py`
- Add `validate_boilerplate_category_file()` function
- Add `load_boilerplates()` helper function
- Add `load_boilerplate_categories()` helper function
- Integrate boilerplate validation into main() pipeline
- Create 1 sample category YAML (`data/boilerplate-categories/nextjs.yml`)
- Create 1 sample entry YAML (`data/boilerplates/nextjs/create-t3-app.yml`)

### Out of Scope (Deferred)
- **Bulk migration** of all entries - *Reason: Session 02 scope*
- **README generation** for boilerplates - *Reason: Session 03 scope*
- **Makefile targets** for boilerplates - *Reason: Session 04 scope*
- **Website pages** for boilerplates - *Reason: Session 05 scope*
- **CLI argument --boilerplates** - *Reason: Session 04 scope*

---

## 5. Technical Approach

### Architecture

The boilerplate system follows a **Parallel Structure** pattern:

```
data/
+-- agents/                    # EXISTING (277 entries)
|   +-- open-source-frameworks/
|   +-- ...
+-- categories/                # EXISTING (10 files)
+-- boilerplates/              # NEW
|   +-- nextjs/
|   +-- django/
|   +-- ...
+-- boilerplate-categories/    # NEW
```

### Design Patterns

- **Pydantic Strict Mode**: `extra = "forbid"` to reject unknown fields
- **Field Validators**: Custom validators for github_repo format, lowercase tags
- **Nested Models**: TechStackComponent as a reusable nested model
- **Optional Rich Metadata**: Most fields optional to handle varying source data quality

### Technology Stack

- Python 3.x
- Pydantic v2 (BaseModel, Field, field_validator, HttpUrl)
- PyYAML for YAML parsing
- pathlib for file system operations

---

## 6. Deliverables

### Files to Create

| File | Purpose | Est. Lines |
|------|---------|------------|
| `data/boilerplates/.gitkeep` | Placeholder for boilerplates root | 0 |
| `data/boilerplates/nextjs/.gitkeep` | Placeholder for nextjs category | 0 |
| `data/boilerplates/nextjs/create-t3-app.yml` | Sample boilerplate entry | ~50 |
| `data/boilerplate-categories/nextjs.yml` | Sample category definition | ~15 |

### Directories to Create

| Directory | Purpose |
|-----------|---------|
| `data/boilerplates/` | Root for boilerplate YAML files |
| `data/boilerplates/nextjs/` | Next.js ecosystem entries |
| `data/boilerplates/remix/` | Remix entries |
| `data/boilerplates/nuxt/` | Vue/Nuxt entries |
| `data/boilerplates/sveltekit/` | Svelte/SvelteKit entries |
| `data/boilerplates/astro/` | Astro entries |
| `data/boilerplates/django/` | Django entries |
| `data/boilerplates/fastapi/` | FastAPI entries |
| `data/boilerplates/laravel/` | Laravel entries |
| `data/boilerplates/rails/` | Rails entries |
| `data/boilerplates/go/` | Go entries |
| `data/boilerplates/rust/` | Rust entries |
| `data/boilerplates/dotnet/` | .NET entries |
| `data/boilerplate-categories/` | Category definitions |

### Files to Modify

| File | Changes | Est. Lines Added |
|------|---------|------------------|
| `scripts/models.py` | Add TechStackComponent, BoilerplateEntry, BoilerplateCategory | ~120 |
| `scripts/validate.py` | Add boilerplate validation functions and integrate into main() | ~60 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] `TechStackComponent` model importable and validates component/technology/reasoning
- [ ] `BoilerplateEntry` model validates all required fields (name, url, description, category)
- [ ] `BoilerplateEntry` model accepts all optional fields without error
- [ ] `BoilerplateCategory` model validates id, title, emoji, description, ecosystem
- [ ] `validate_boilerplate_file()` returns True for valid YAML
- [ ] `validate_boilerplate_file()` returns False with error for invalid YAML
- [ ] Sample `create-t3-app.yml` passes validation
- [ ] Sample `nextjs.yml` category passes validation

### Testing Requirements
- [ ] Run `python scripts/validate.py` - all existing agent files still pass
- [ ] Run `python scripts/validate.py` - new boilerplate files validate
- [ ] Run `make validate` - command completes without error
- [ ] Import test: `from models import BoilerplateEntry` succeeds

### Quality Gates
- [ ] All files ASCII-encoded (no special characters)
- [ ] Unix LF line endings
- [ ] Code follows existing project conventions (4-space indent, docstrings)
- [ ] No new linting warnings
- [ ] Extra fields rejected by schema

---

## 8. Implementation Notes

### Key Considerations

1. **Description length**: Boilerplates have longer descriptions (up to 2000 chars vs 1000 for agents)
2. **Ecosystem field**: Categories have an `ecosystem` field to group by language family
3. **Technical stack**: Nested list of TechStackComponent for structured tech breakdown
4. **Pricing model**: Added `open-core` option beyond agent pricing types
5. **Stars field**: Integer field for GitHub stars (will be migrated from source)

### Potential Challenges

- **Field naming consistency**: Ensure fields match PRD spec exactly
- **Validator reuse**: May want to extract common validators (github_repo, tags) to shared functions
- **Category validation**: Currently no cross-validation that `category` field matches existing category ID

### ASCII Reminder

All output files must use ASCII-only characters (0-127). This is critical for:
- YAML field values (descriptions, use_case, community)
- Python docstrings and comments
- Sample data content

---

## 9. Testing Strategy

### Unit Tests (Manual)

```python
# Test model import
from models import TechStackComponent, BoilerplateEntry, BoilerplateCategory

# Test valid entry
entry = BoilerplateEntry(
    name="test",
    url="https://github.com/test/test",
    description="A test boilerplate for testing purposes only",
    category="nextjs"
)

# Test invalid entry (should raise ValidationError)
entry = BoilerplateEntry(name="x")  # Missing required fields
```

### Integration Tests

- Run `make validate` - must pass with no errors
- Verify agent validation still works (no regression)
- Verify boilerplate validation catches schema errors

### Manual Testing

1. Create invalid YAML (missing required field) - verify validation fails
2. Create YAML with unknown field - verify validation fails (extra="forbid")
3. Create YAML with invalid github_repo format - verify validation fails

### Edge Cases

- Empty `technical_stack` list (allowed)
- Very long description (truncated at 2000 chars)
- Tags with spaces (auto-converted to lowercase-hyphenated)
- Missing optional fields (all should default gracefully)

---

## 10. Dependencies

### External Libraries

- `pydantic`: v2.x (already in requirements.txt)
- `pyyaml`: (already in requirements.txt)

### Other Sessions

- **Depends on**: None
- **Depended by**: Session 02, 03, 04, 05, 06 (all subsequent sessions)

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.
