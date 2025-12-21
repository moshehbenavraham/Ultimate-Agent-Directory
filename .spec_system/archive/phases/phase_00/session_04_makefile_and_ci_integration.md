# Session 04: Makefile & CI Integration

**Session ID**: `phase00-session04-makefile-and-ci-integration`
**Status**: Not Started
**Estimated Tasks**: ~15-20
**Estimated Duration**: 2-3 hours
**Priority**: P0

---

## Objective

Integrate boilerplate validation and generation into the project's build system and CI/CD pipeline, ensuring automated quality checks and seamless deployment.

---

## Scope

### In Scope (MVP)
- Add `make validate-boilerplates` target
- Add `make generate-boilerplates` target
- Add `make migrate-boilerplates` target
- Update `make validate` to include boilerplates
- Update `make test` to include boilerplate validation
- Update `.github/workflows/validate.yml` for boilerplate validation
- Test CI pipeline with boilerplate changes

### Out of Scope
- Website deployment integration (Session 05)
- Link checking automation (Session 06)

---

## Prerequisites

- [ ] Session 01 completed (validation functions exist)
- [ ] Session 02 completed (migration script exists)
- [ ] Session 03 completed (generation script exists)

---

## Deliverables

1. **Updated `Makefile`** with:
   - `validate-boilerplates` target
   - `generate-boilerplates` target
   - `migrate-boilerplates` target
   - Updated `validate` target to include boilerplates
   - Updated `test` target to include boilerplates

2. **Updated `.github/workflows/validate.yml`** with:
   - Boilerplate validation step
   - Boilerplate README generation test
   - Proper caching for dependencies

3. **Documentation** updates:
   - Updated CLAUDE.md with boilerplate commands
   - Updated README if needed

---

## Technical Details

### New Makefile Targets

```makefile
validate-boilerplates:
	@echo "Validating boilerplate YAML files..."
	$(VENV)/bin/python scripts/validate.py --boilerplates

generate-boilerplates:
	@echo "Generating BOILERPLATES.md..."
	$(VENV)/bin/python scripts/generate_boilerplates.py

migrate-boilerplates:
	@echo "Migrating boilerplates from markdown..."
	$(VENV)/bin/python scripts/migrate_boilerplates.py
```

### Updated Targets

```makefile
validate: validate-agents validate-boilerplates

test: validate generate generate-boilerplates
```

### CI Workflow Updates

Add to `.github/workflows/validate.yml`:
```yaml
- name: Validate boilerplates
  run: make validate-boilerplates

- name: Test boilerplate README generation
  run: make generate-boilerplates
```

---

## Success Criteria

- [ ] `make validate-boilerplates` runs and validates all boilerplate YAML
- [ ] `make generate-boilerplates` generates BOILERPLATES.md
- [ ] `make validate` includes both agents and boilerplates
- [ ] `make test` passes with all boilerplate content
- [ ] CI workflow passes with boilerplate validation
- [ ] CI catches schema errors in boilerplate YAML
