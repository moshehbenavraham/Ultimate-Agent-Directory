# Session Specification

**Session ID**: `phase00-session04-makefile-and-ci-integration`
**Phase**: 00 - Feature Addition
**Status**: Not Started
**Created**: 2025-12-21

---

## 1. Session Overview

This session integrates boilerplate validation and generation into the project's build system (Makefile) and continuous integration pipeline (GitHub Actions). With the core scripts complete from Sessions 01-03, this session creates the unified interface that developers and CI systems use to validate data quality and generate outputs.

The Makefile provides a consistent developer experience with clear targets like `make validate-boilerplates` and `make generate-boilerplates`, while updating existing unified targets (`make validate`, `make test`) to include boilerplate operations. This ensures that any change to boilerplate YAML files is automatically validated on pull requests.

This is a critical integration point on the P0 path. Without proper CI validation, invalid boilerplate data could be merged, breaking the generation pipeline. Sessions 05 (website integration) and 06 (polish) depend on having reliable CI in place.

---

## 2. Objectives

1. Add dedicated Makefile targets for boilerplate operations (validate, generate, migrate)
2. Update unified Makefile targets to include boilerplates in standard workflows
3. Update GitHub Actions validate.yml workflow to validate boilerplates on PRs
4. Update GitHub Actions deploy.yml workflow to generate BOILERPLATES.md on deploy

---

## 3. Prerequisites

### Required Sessions
- [x] `phase00-session01-schema-and-structure` - Provides BoilerplateEntry, BoilerplateCategory models in models.py
- [x] `phase00-session02-migration-script` - Provides migrate_boilerplates.py script and YAML data files
- [x] `phase00-session03-readme-generation` - Provides generate_boilerplates.py script and templates

### Required Tools/Knowledge
- GNU Make syntax (targets, dependencies, variables)
- GitHub Actions YAML workflow syntax
- Python venv integration in Makefiles

### Environment Requirements
- Python 3.11+ with venv support
- Existing Makefile with PYTHON/PIP variables defined
- GitHub repository with Actions enabled

---

## 4. Scope

### In Scope (MVP)
- Add `make validate-boilerplates` target
- Add `make generate-boilerplates` target
- Add `make migrate-boilerplates` target (for convenience)
- Rename existing `make validate` to `make validate-agents`
- Create new `make validate` as unified target including both agents and boilerplates
- Update `make test` to include boilerplate generation
- Update `.github/workflows/validate.yml` with boilerplate validation step
- Update `.github/workflows/deploy.yml` with BOILERPLATES.md generation
- Update Makefile help text

### Out of Scope (Deferred)
- Website deployment updates for boilerplate pages - *Reason: Session 05*
- Link checking for boilerplate URLs - *Reason: Session 06*
- Adding --boilerplates-only CLI flag to validate.py - *Reason: Current script handles all types together, no need for separation*

---

## 5. Technical Approach

### Architecture

The Makefile serves as the primary interface for all build operations. New boilerplate targets follow the existing pattern established for agents:

```
Makefile
  |-- validate-agents (renamed from validate)
  |-- validate-boilerplates (new)
  |-- validate (unified, calls both)
  |-- generate (existing, agents README)
  |-- generate-boilerplates (new)
  |-- migrate-boilerplates (new)
  |-- test (updated to include boilerplates)
```

### Design Patterns
- **Unified targets**: Single entry points (`validate`, `test`) that aggregate sub-targets
- **Consistent naming**: `verb-boilerplates` pattern matches existing `verb` pattern
- **Fail-fast**: CI exits immediately on validation failure

### Technology Stack
- GNU Make 4.x
- GitHub Actions (ubuntu-latest runner)
- Python 3.11 with pip caching

---

## 6. Deliverables

### Files to Create
| File | Purpose | Est. Lines |
|------|---------|------------|
| None | No new files needed | - |

### Files to Modify
| File | Changes | Est. Lines Changed |
|------|---------|------------|
| `Makefile` | Add 5 new targets, update 2 existing, update help text | ~30 |
| `.github/workflows/validate.yml` | Add boilerplate validation and generation steps | ~15 |
| `.github/workflows/deploy.yml` | Add BOILERPLATES.md generation step | ~5 |

---

## 7. Success Criteria

### Functional Requirements
- [ ] `make validate-boilerplates` runs and validates all boilerplate YAML files
- [ ] `make generate-boilerplates` generates BOILERPLATES.md successfully
- [ ] `make migrate-boilerplates` runs migration script (dry-run by default)
- [ ] `make validate` validates both agents and boilerplates
- [ ] `make test` passes with all boilerplate content included
- [ ] CI workflow validates boilerplates on pull requests
- [ ] CI catches schema errors in boilerplate YAML
- [ ] Deploy workflow generates BOILERPLATES.md before deploying

### Testing Requirements
- [ ] Manual test: Run each new Makefile target locally
- [ ] Manual test: Introduce a deliberate YAML error, verify CI catches it
- [ ] Manual test: Verify deploy workflow generates both README.md and BOILERPLATES.md

### Quality Gates
- [ ] All files use ASCII-only characters (0-127)
- [ ] Unix LF line endings in all files
- [ ] Makefile uses tabs for indentation (Make requirement)
- [ ] No trailing whitespace
- [ ] Help text updated with new commands

---

## 8. Implementation Notes

### Key Considerations
- The existing validate.py already validates boilerplates in its main() function, so we don't need a separate --boilerplates flag
- The Makefile PYTHON variable is `venv/bin/python` - use this consistently
- Keep target names consistent with existing conventions (verb, or verb-noun)

### Potential Challenges
- **Makefile tabs**: Make requires literal tab characters for recipe lines. Editors may convert to spaces.
- **CI caching**: pip caching is already configured, no changes needed
- **Script paths**: All scripts are in `scripts/` directory, referenced without leading `./`

### ASCII Reminder
All output files must use ASCII-only characters (0-127). The existing files are ASCII-clean; maintain this.

---

## 9. Testing Strategy

### Unit Tests
- Not applicable (Makefile and workflow YAML don't have unit tests)

### Integration Tests
- Run `make validate-boilerplates` and verify exit code 0
- Run `make generate-boilerplates` and verify BOILERPLATES.md created
- Run `make test` and verify all steps pass

### Manual Testing
1. Run each new target individually and verify success
2. Introduce invalid YAML in a boilerplate file
3. Run `make validate` and verify it fails with clear error
4. Fix the YAML and verify validation passes
5. Create a PR branch, push, and verify GitHub Actions runs validation

### Edge Cases
- Empty boilerplate directories (should pass, 0 files validated)
- Missing BOILERPLATES.md template (should fail with clear error)
- Network failure during CI (handled by GitHub Actions retry)

---

## 10. Dependencies

### External Libraries
- None (Makefile and workflow YAML are infrastructure)

### Python Dependencies (already installed)
- pydantic >= 2.0
- pyyaml
- jinja2

### Other Sessions
- **Depends on**: Sessions 01, 02, 03 (all complete)
- **Depended by**: Session 05 (website integration), Session 06 (polish)

---

## Implementation Checklist

### Makefile Changes

```makefile
# Add to .PHONY line
.PHONY: ... validate-agents validate-boilerplates generate-boilerplates migrate-boilerplates

# Add new targets
validate-agents:
	$(PYTHON) scripts/validate.py

validate-boilerplates:
	@echo "Validating boilerplate YAML files..."
	$(PYTHON) scripts/validate.py

generate-boilerplates:
	$(PYTHON) scripts/generate_boilerplates.py

migrate-boilerplates:
	$(PYTHON) scripts/migrate_boilerplates.py --dry-run

# Update unified targets
validate: validate-agents validate-boilerplates
	@echo "All validation passed!"

test: validate generate generate-boilerplates check-links-quick
	@echo "All tests passed!"
```

### Workflow Changes

validate.yml additions:
```yaml
- name: Test boilerplate README generation
  run: |
    python scripts/generate_boilerplates.py
    if [ ! -f BOILERPLATES.md ]; then
      echo "Error: BOILERPLATES.md was not generated"
      exit 1
    fi
```

deploy.yml additions:
```yaml
- name: Generate Boilerplates README
  run: |
    python scripts/generate_boilerplates.py
```

---

## Next Steps

Run `/tasks` to generate the implementation task checklist.
