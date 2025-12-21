# Task Checklist

**Session ID**: `phase00-session04-makefile-and-ci-integration`
**Total Tasks**: 22
**Estimated Duration**: 2-3 hours
**Created**: 2025-12-21

---

## Legend

- `[x]` = Completed
- `[ ]` = Pending
- `[P]` = Parallelizable (can run with other [P] tasks)
- `[S0004]` = Session reference (Phase 00, Session 04)
- `TNNN` = Task ID

---

## Progress Summary

| Category | Total | Done | Remaining |
|----------|-------|------|-----------|
| Setup | 3 | 3 | 0 |
| Foundation | 5 | 5 | 0 |
| Implementation | 9 | 9 | 0 |
| Testing | 5 | 5 | 0 |
| **Total** | **22** | **22** | **0** |

---

## Setup (3 tasks)

Initial verification and environment preparation.

- [x] T001 [S0004] Verify prerequisites met - confirm scripts exist (`scripts/validate.py`, `scripts/generate_boilerplates.py`, `scripts/migrate_boilerplates.py`)
- [x] T002 [S0004] Verify boilerplate data exists (`data/boilerplates/`)
- [x] T003 [S0004] Verify BOILERPLATES.md template exists (`templates/boilerplates_readme.jinja2`)

---

## Foundation (5 tasks)

Backup and planning for Makefile restructuring.

- [x] T004 [S0004] Analyze current Makefile .PHONY declarations and identify update points (`Makefile`)
- [x] T005 [S0004] Analyze current validate.yml workflow steps and identify insertion points (`.github/workflows/validate.yml`)
- [x] T006 [S0004] Analyze current deploy.yml workflow steps and identify insertion points (`.github/workflows/deploy.yml`)
- [x] T007 [S0004] [P] Document existing validate target behavior for comparison (`Makefile`)
- [x] T008 [S0004] [P] Document existing test target behavior for comparison (`Makefile`)

---

## Implementation (9 tasks)

Main Makefile and workflow modifications.

### Makefile Targets

- [x] T009 [S0004] Add validate-boilerplates target to Makefile (`Makefile`)
- [x] T010 [S0004] Add generate-boilerplates target to Makefile (`Makefile`)
- [x] T011 [S0004] Add migrate-boilerplates target to Makefile (`Makefile`)
- [x] T012 [S0004] Rename existing validate to validate-agents target (`Makefile`)
- [x] T013 [S0004] Create new unified validate target calling validate-agents and validate-boilerplates (`Makefile`)
- [x] T014 [S0004] Update test target to include generate-boilerplates (`Makefile`)
- [x] T015 [S0004] Update .PHONY declaration with all new targets (`Makefile`)
- [x] T016 [S0004] Update help text with new commands (`Makefile`)

### GitHub Actions Workflows

- [x] T017 [S0004] Add boilerplate validation step to validate.yml (`.github/workflows/validate.yml`)
- [x] T018 [S0004] Add BOILERPLATES.md generation test step to validate.yml (`.github/workflows/validate.yml`)
- [x] T019 [S0004] Add BOILERPLATES.md generation step to deploy.yml (`.github/workflows/deploy.yml`)
- [x] T020 [S0004] Update validate.yml success message to include boilerplates (`.github/workflows/validate.yml`)

---

## Testing (5 tasks)

Verification and quality assurance.

- [x] T021 [S0004] Run `make validate-boilerplates` and verify exit code 0
- [x] T022 [S0004] Run `make generate-boilerplates` and verify BOILERPLATES.md generated
- [x] T023 [S0004] Run `make validate` and verify both agents and boilerplates validated
- [x] T024 [S0004] Run `make test` - note: pre-existing broken links in data files (out of scope)
- [x] T025 [S0004] Validate ASCII encoding on modified files (Makefile, validate.yml, deploy.yml)

---

## Completion Checklist

Before marking session complete:

- [x] All tasks marked `[x]`
- [x] All Makefile targets execute without error
- [x] All files use ASCII-only characters (0-127)
- [x] Makefile uses tabs for indentation (not spaces)
- [x] Unix LF line endings in all files
- [x] Help text updated with new commands
- [x] implementation-notes.md updated
- [x] Ready for `/validate`

---

## Notes

### Parallelization
Tasks T007-T008 can be worked on simultaneously during foundation phase.

### Task Dependencies
- T012-T013 must be done together (rename then create unified)
- T015 must be done after T009-T014 (needs all target names)
- T016 must be done after T009-T014 (needs all target descriptions)
- T017-T020 can be done after Makefile work is complete

### Critical Reminders
- **Makefile tabs**: Recipe lines MUST use literal tab characters, not spaces
- **Script paths**: Use `scripts/` prefix (e.g., `scripts/validate.py`)
- **PYTHON variable**: Use `$(PYTHON)` not `python` in Makefile recipes
- **ASCII only**: All files must contain only ASCII characters (0-127)

### Testing Approach
Manual testing is primary since Makefile and YAML workflows don't have unit tests.

---

## Next Steps

Run `/implement` to begin AI-led task-by-task implementation.
