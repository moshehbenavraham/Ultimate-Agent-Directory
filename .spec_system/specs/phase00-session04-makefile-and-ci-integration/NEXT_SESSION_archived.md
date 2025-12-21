# NEXT_SESSION.md

## Session Recommendation

**Generated**: 2025-12-21
**Project State**: Phase 00 - Feature Addition
**Completed Sessions**: 3

---

## Recommended Next Session

**Session ID**: `phase00-session04-makefile-and-ci-integration`
**Session Name**: Makefile & CI Integration
**Estimated Duration**: 2-3 hours
**Estimated Tasks**: 15-20

---

## Why This Session Next?

### Prerequisites Met
- [x] Session 01 completed (schema and validation functions exist in models.py)
- [x] Session 02 completed (migration script exists and boilerplate YAML files generated)
- [x] Session 03 completed (generation script and BOILERPLATES.md template working)

### Dependencies
- **Builds on**: Sessions 01-03 (schema, migration, generation scripts)
- **Enables**: Session 05 (website integration) and Session 06 (polish & verification)

### Project Progression

Session 4 is the natural integration point after completing the core tooling. With the schema (Session 01), migration (Session 02), and README generation (Session 03) complete, the next logical step is integrating these into the build system:

1. **Foundation laid**: The scripts exist and work individually
2. **Integration needed**: Makefile targets provide unified interface for all operations
3. **CI/CD critical**: Automated validation ensures data quality on every PR
4. **P0 priority**: This is on the critical path - Sessions 05-06 depend on it

---

## Session Overview

### Objective

Integrate boilerplate validation and generation into the project's build system and CI/CD pipeline, ensuring automated quality checks and seamless deployment.

### Key Deliverables

1. **Makefile targets**: `validate-boilerplates`, `generate-boilerplates`, `migrate-boilerplates`
2. **Updated unified targets**: `make validate` and `make test` include boilerplates
3. **CI workflow updates**: `.github/workflows/validate.yml` validates boilerplates on PRs
4. **Documentation**: Updated CLAUDE.md with boilerplate commands

### Scope Summary
- **In Scope (MVP)**: Makefile targets, CI validation, documentation updates
- **Out of Scope**: Website deployment (Session 05), link checking automation (Session 06)

---

## Technical Considerations

### Technologies/Patterns
- GNU Make (build automation)
- GitHub Actions (CI/CD pipeline)
- Python venv integration
- YAML schema validation

### Potential Challenges
- **Makefile syntax**: Ensure proper tab indentation and variable expansion
- **CI caching**: May need to adjust dependency caching for boilerplate validation
- **Error messaging**: Make validation errors clear and actionable

### Implementation Approach

```makefile
# New targets
validate-boilerplates:
	@echo "Validating boilerplate YAML files..."
	$(VENV)/bin/python scripts/validate.py --boilerplates

generate-boilerplates:
	@echo "Generating BOILERPLATES.md..."
	$(VENV)/bin/python scripts/generate_boilerplates.py

# Updated unified targets
validate: validate-agents validate-boilerplates
test: validate generate generate-boilerplates
```

---

## Alternative Sessions

If this session is blocked:
1. **Session 05 (Website Integration)** - Could start HTML templates while CI work is unblocked, but would need manual testing without CI
2. **Session 06 (Polish)** - Not recommended; depends on Session 05

**Note**: Session 4 has no blockers. All prerequisites are complete.

---

## Next Steps

Run `/sessionspec` to generate the formal specification.
